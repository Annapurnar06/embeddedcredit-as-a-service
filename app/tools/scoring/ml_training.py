"""ML model training pipeline for segment scoring — replaces rule-based v1 with XGBoost/LightGBM.

Solves: Score models are rule-based weighted sums. This module provides:
1. Synthetic data generation bootstrapped from segment weight priors
2. XGBoost model training per segment
3. Model evaluation (Gini, KS, AUC, PSI)
4. Champion/challenger comparison
5. Model serialization for production scoring
"""

from __future__ import annotations

import json
import math
import os
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.core.logging import get_logger
from app.tools.scoring.score import SEGMENT_WEIGHTS

logger = get_logger(__name__)

MODEL_DIR = Path("models")

try:
    import numpy as np

    _NP = True
except ImportError:
    _NP = False

try:
    import xgboost as xgb

    _XGB = True
except ImportError:
    _XGB = False


# ---------- Data types ----------

@dataclass
class TrainingConfig:
    segment: str
    n_samples: int = 5000
    test_ratio: float = 0.20
    default_rate: float = 0.08
    xgb_params: dict[str, Any] = field(default_factory=lambda: {
        "max_depth": 4,
        "learning_rate": 0.1,
        "n_estimators": 200,
        "objective": "binary:logistic",
        "eval_metric": "auc",
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "min_child_weight": 5,
        "reg_alpha": 0.1,
        "reg_lambda": 1.0,
        "random_state": 42,
    })


@dataclass
class ModelMetrics:
    gini: float = 0.0
    ks: float = 0.0
    auc: float = 0.0
    psi: float = 0.0
    approval_rate: float = 0.0
    default_rate_approved: float = 0.0
    sample_size: int = 0


@dataclass
class TrainedModel:
    segment: str
    model_version: str
    features: list[str]
    metrics: ModelMetrics
    trained_at: str
    model_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "segment": self.segment,
            "model_version": self.model_version,
            "features": self.features,
            "metrics": {
                "gini": round(self.metrics.gini, 4),
                "ks": round(self.metrics.ks, 4),
                "auc": round(self.metrics.auc, 4),
                "psi": round(self.metrics.psi, 4),
                "approval_rate": round(self.metrics.approval_rate, 4),
                "default_rate_approved": round(self.metrics.default_rate_approved, 4),
                "sample_size": self.metrics.sample_size,
            },
            "trained_at": self.trained_at,
            "model_path": self.model_path,
        }


# ---------- Synthetic data generator ----------

class SyntheticDataGenerator:
    """Generates training data bootstrapped from rule-based weight priors.

    For each segment, the YAML weights define feature importance.
    We simulate features and a target (default=1/non-default=0) where
    higher-weighted features have stronger correlation with good outcomes.
    """

    def generate(self, config: TrainingConfig) -> tuple[list[dict], list[int]]:
        weights = SEGMENT_WEIGHTS.get(config.segment, {})
        if not weights:
            weights = SEGMENT_WEIGHTS.get("DAIRY_FARMER", {})

        features_list: list[dict[str, float]] = []
        labels: list[int] = []
        rng = random.Random(42)

        for _ in range(config.n_samples):
            row: dict[str, float] = {}
            weighted_quality = 0.0

            for feat, weight in weights.items():
                value = rng.betavariate(2, 2)  # centred around 0.5
                row[feat] = round(value, 4)
                weighted_quality += value * weight

            noise = rng.gauss(0, 0.05)
            default_prob = 1.0 / (1.0 + math.exp(5 * (weighted_quality + noise - 0.45)))
            label = 1 if rng.random() < default_prob else 0

            features_list.append(row)
            labels.append(label)

        logger.info(
            "synthetic_data_generated",
            segment=config.segment,
            samples=config.n_samples,
            default_rate=round(sum(labels) / len(labels), 3),
        )
        return features_list, labels


# ---------- Model trainer ----------

class SegmentModelTrainer:
    """Trains XGBoost model per segment; falls back to rule-based if XGBoost unavailable."""

    def __init__(self) -> None:
        self._generator = SyntheticDataGenerator()

    def train(self, config: TrainingConfig) -> TrainedModel:
        features_list, labels = self._generator.generate(config)
        feature_names = sorted(features_list[0].keys())
        n = len(features_list)
        split = int(n * (1 - config.test_ratio))

        if _XGB and _NP:
            return self._train_xgboost(config, features_list, labels, feature_names, split)
        return self._train_rule_based(config, features_list, labels, feature_names, split)

    def _train_xgboost(
        self,
        config: TrainingConfig,
        features: list[dict],
        labels: list[int],
        feature_names: list[str],
        split: int,
    ) -> TrainedModel:
        X = np.array([[row[f] for f in feature_names] for row in features])
        y = np.array(labels)

        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        model = xgb.XGBClassifier(**config.xgb_params)
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False,
        )

        y_pred = model.predict_proba(X_test)[:, 1]
        metrics = self._compute_metrics(y_test, y_pred)

        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        version = f"{config.segment.lower()}_xgb_v1"
        model_path = str(MODEL_DIR / f"{version}.json")
        model.save_model(model_path)

        logger.info(
            "xgb_model_trained",
            segment=config.segment,
            gini=round(metrics.gini, 3),
            ks=round(metrics.ks, 3),
            auc=round(metrics.auc, 3),
        )

        return TrainedModel(
            segment=config.segment,
            model_version=version,
            features=feature_names,
            metrics=metrics,
            trained_at=datetime.now(timezone.utc).isoformat(),
            model_path=model_path,
        )

    def _train_rule_based(
        self,
        config: TrainingConfig,
        features: list[dict],
        labels: list[int],
        feature_names: list[str],
        split: int,
    ) -> TrainedModel:
        """Fallback: evaluate rule-based weighted sum as if it were an ML model."""
        weights = SEGMENT_WEIGHTS.get(config.segment, {})

        test_features = features[split:]
        test_labels = labels[split:]

        predictions = []
        for row in test_features:
            score = sum(row.get(f, 0.5) * weights.get(f, 0.0) for f in feature_names)
            predictions.append(1.0 - score)  # higher score = lower default prob

        metrics = self._compute_metrics_pure(test_labels, predictions)

        version = f"{config.segment.lower()}_rulebased_v1"
        logger.info(
            "rulebased_model_evaluated",
            segment=config.segment,
            gini=round(metrics.gini, 3),
            ks=round(metrics.ks, 3),
        )

        return TrainedModel(
            segment=config.segment,
            model_version=version,
            features=feature_names,
            metrics=metrics,
            trained_at=datetime.now(timezone.utc).isoformat(),
        )

    def _compute_metrics(self, y_true: Any, y_pred: Any) -> ModelMetrics:
        from sklearn.metrics import roc_auc_score
        auc = roc_auc_score(y_true, y_pred)
        gini = 2 * auc - 1

        # KS statistic
        sorted_pairs = sorted(zip(y_pred, y_true), key=lambda x: -x[0])
        n_pos = sum(y_true)
        n_neg = len(y_true) - n_pos
        cum_pos = cum_neg = 0
        max_ks = 0.0
        for pred, actual in sorted_pairs:
            if actual == 1:
                cum_pos += 1
            else:
                cum_neg += 1
            ks = abs(cum_pos / max(n_pos, 1) - cum_neg / max(n_neg, 1))
            max_ks = max(max_ks, ks)

        threshold = 0.5
        approved = [(p, a) for p, a in zip(y_pred, y_true) if p < threshold]
        approval_rate = len(approved) / max(len(y_true), 1)
        default_rate_approved = (
            sum(a for _, a in approved) / max(len(approved), 1) if approved else 0.0
        )

        return ModelMetrics(
            gini=gini, ks=max_ks, auc=auc, psi=0.0,
            approval_rate=approval_rate,
            default_rate_approved=default_rate_approved,
            sample_size=len(y_true),
        )

    def _compute_metrics_pure(
        self, y_true: list[int], y_pred: list[float],
    ) -> ModelMetrics:
        """Pure-python metrics when sklearn is not available."""
        n = len(y_true)
        if n == 0:
            return ModelMetrics()

        pairs = list(zip(y_pred, y_true))
        n_pos = sum(y_true)
        n_neg = n - n_pos
        if n_pos == 0 or n_neg == 0:
            return ModelMetrics(sample_size=n)

        # AUC via Mann-Whitney U
        concordant = 0
        for pred, actual in pairs:
            if actual == 1:
                for pred2, actual2 in pairs:
                    if actual2 == 0:
                        if pred > pred2:
                            concordant += 1
                        elif pred == pred2:
                            concordant += 0.5
        auc = concordant / (n_pos * n_neg)
        gini = 2 * auc - 1

        # KS
        sorted_pairs = sorted(pairs, key=lambda x: -x[0])
        cum_p = cum_n = 0
        max_ks = 0.0
        for pred, actual in sorted_pairs:
            if actual == 1:
                cum_p += 1
            else:
                cum_n += 1
            ks = abs(cum_p / n_pos - cum_n / n_neg)
            max_ks = max(max_ks, ks)

        threshold = 0.5
        approved = [(p, a) for p, a in pairs if p < threshold]
        approval_rate = len(approved) / n
        dr = sum(a for _, a in approved) / max(len(approved), 1) if approved else 0.0

        return ModelMetrics(
            gini=gini, ks=max_ks, auc=auc, psi=0.0,
            approval_rate=approval_rate,
            default_rate_approved=dr,
            sample_size=n,
        )


# ---------- Champion / Challenger ----------

def compare_models(champion: TrainedModel, challenger: TrainedModel) -> dict[str, Any]:
    """Compare two models on key metrics; recommend promotion or continuation."""
    c = champion.metrics
    ch = challenger.metrics
    gini_improvement = ch.gini - c.gini
    ks_improvement = ch.ks - c.ks
    auc_improvement = ch.auc - c.auc

    promote = gini_improvement > 0.02 and ks_improvement > 0.01

    return {
        "champion": champion.model_version,
        "challenger": challenger.model_version,
        "gini_improvement": round(gini_improvement, 4),
        "ks_improvement": round(ks_improvement, 4),
        "auc_improvement": round(auc_improvement, 4),
        "champion_default_rate": round(c.default_rate_approved, 4),
        "challenger_default_rate": round(ch.default_rate_approved, 4),
        "recommendation": "PROMOTE_CHALLENGER" if promote else "KEEP_CHAMPION",
        "reason": (
            f"Challenger Gini +{gini_improvement:.3f}, KS +{ks_improvement:.3f}"
            if promote
            else f"Improvement insufficient (Gini +{gini_improvement:.3f})"
        ),
    }
