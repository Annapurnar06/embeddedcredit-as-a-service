"""Tests for ML training pipeline — synthetic data, model training, champion/challenger."""

import pytest

from app.tools.scoring.ml_training import (
    SegmentModelTrainer,
    SyntheticDataGenerator,
    TrainingConfig,
    compare_models,
)


@pytest.fixture
def generator():
    return SyntheticDataGenerator()


@pytest.fixture
def trainer():
    return SegmentModelTrainer()


class TestSyntheticDataGenerator:
    def test_generates_correct_count(self, generator):
        config = TrainingConfig(segment="DAIRY_FARMER", n_samples=100)
        features, labels = generator.generate(config)
        assert len(features) == 100
        assert len(labels) == 100

    def test_labels_are_binary(self, generator):
        config = TrainingConfig(segment="DAIRY_FARMER", n_samples=500)
        _, labels = generator.generate(config)
        assert all(label in (0, 1) for label in labels)

    def test_default_rate_reasonable(self, generator):
        config = TrainingConfig(segment="DAIRY_FARMER", n_samples=2000)
        _, labels = generator.generate(config)
        rate = sum(labels) / len(labels)
        assert 0.02 < rate < 0.50, f"Default rate {rate} outside reasonable range"

    def test_features_match_segment_weights(self, generator):
        from app.tools.scoring.score import SEGMENT_WEIGHTS
        config = TrainingConfig(segment="DAIRY_FARMER", n_samples=10)
        features, _ = generator.generate(config)
        expected_features = set(SEGMENT_WEIGHTS["DAIRY_FARMER"].keys())
        actual_features = set(features[0].keys())
        assert actual_features == expected_features

    def test_features_in_range(self, generator):
        config = TrainingConfig(segment="GIG_WORKER", n_samples=500)
        features, _ = generator.generate(config)
        for row in features:
            for v in row.values():
                assert 0.0 <= v <= 1.0

    def test_different_segments(self, generator):
        for seg in ["DAIRY_FARMER", "GIG_WORKER", "KIRANA_SHOP", "SHG_MEMBER"]:
            config = TrainingConfig(segment=seg, n_samples=50)
            features, labels = generator.generate(config)
            assert len(features) == 50
            assert len(labels) == 50

    def test_deterministic_with_same_seed(self, generator):
        config = TrainingConfig(segment="DAIRY_FARMER", n_samples=100)
        f1, l1 = generator.generate(config)
        f2, l2 = generator.generate(config)
        assert f1 == f2
        assert l1 == l2


class TestSegmentModelTrainer:
    def test_train_dairy_farmer(self, trainer):
        config = TrainingConfig(segment="DAIRY_FARMER", n_samples=500)
        model = trainer.train(config)
        assert model.segment == "DAIRY_FARMER"
        assert model.features
        assert model.metrics.sample_size > 0
        assert model.trained_at

    def test_train_gig_worker(self, trainer):
        config = TrainingConfig(segment="GIG_WORKER", n_samples=500)
        model = trainer.train(config)
        assert model.segment == "GIG_WORKER"

    def test_metrics_reasonable(self, trainer):
        config = TrainingConfig(segment="DAIRY_FARMER", n_samples=2000)
        model = trainer.train(config)
        m = model.metrics
        assert -0.1 <= m.gini <= 1.0, f"Gini {m.gini} out of range"
        assert 0.0 <= m.ks <= 1.0, f"KS {m.ks} out of range"
        assert 0.0 <= m.auc <= 1.0, f"AUC {m.auc} out of range"

    def test_model_version_format(self, trainer):
        config = TrainingConfig(segment="KIRANA_SHOP", n_samples=200)
        model = trainer.train(config)
        assert "kirana_shop" in model.model_version

    def test_to_dict(self, trainer):
        config = TrainingConfig(segment="DAIRY_FARMER", n_samples=200)
        model = trainer.train(config)
        data = model.to_dict()
        assert "gini" in data["metrics"]
        assert "ks" in data["metrics"]
        assert "features" in data

    @pytest.mark.parametrize("segment", [
        "DAIRY_FARMER", "GIG_WORKER", "KIRANA_SHOP", "SHG_MEMBER",
        "STREET_VENDOR", "FISHERY", "EV_FINANCING",
    ])
    def test_all_segments_trainable(self, trainer, segment):
        config = TrainingConfig(segment=segment, n_samples=200)
        model = trainer.train(config)
        assert model.segment == segment
        assert model.metrics.sample_size > 0


class TestChampionChallenger:
    def test_promote_better_model(self, trainer):
        config_a = TrainingConfig(segment="DAIRY_FARMER", n_samples=500)
        config_b = TrainingConfig(segment="DAIRY_FARMER", n_samples=2000)
        champion = trainer.train(config_a)
        challenger = trainer.train(config_b)

        # Force challenger to be better for test
        challenger.metrics.gini = champion.metrics.gini + 0.05
        challenger.metrics.ks = champion.metrics.ks + 0.03

        result = compare_models(champion, challenger)
        assert result["recommendation"] == "PROMOTE_CHALLENGER"

    def test_keep_champion_insufficient_improvement(self, trainer):
        config = TrainingConfig(segment="DAIRY_FARMER", n_samples=500)
        champion = trainer.train(config)
        challenger = trainer.train(config)

        # Same model = no improvement
        challenger.metrics.gini = champion.metrics.gini + 0.005
        challenger.metrics.ks = champion.metrics.ks + 0.005

        result = compare_models(champion, challenger)
        assert result["recommendation"] == "KEEP_CHAMPION"

    def test_comparison_has_all_fields(self, trainer):
        config = TrainingConfig(segment="DAIRY_FARMER", n_samples=200)
        a = trainer.train(config)
        b = trainer.train(config)
        result = compare_models(a, b)
        assert "gini_improvement" in result
        assert "ks_improvement" in result
        assert "recommendation" in result
        assert "reason" in result
