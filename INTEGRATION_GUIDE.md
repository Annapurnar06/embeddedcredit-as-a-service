# Integration Guide: Voice AI, ASR, Decisioning & ML Training

## Overview

This guide covers integrating the four key subsystems built to solve critical production gaps:

1. **Cartesia Voice AI (TTS)** -- text-to-speech in 10 Indian languages
2. **Multi-Provider ASR** -- speech-to-text with Deepgram/Google/Bhashini fallback
3. **Standalone Credit Decisioning** -- local decisioning engine (Sentinel fallback)
4. **ML Training Pipeline** -- XGBoost model training to replace rule-based scoring

---

## 1. Voice AI Pipeline Setup

### Architecture

```
Borrower speaks → [ASR: Deepgram/Google/Bhashini] → text
    → [Intent classifier] → [Agent runtime + tools]
    → response text → [TTS: Cartesia] → audio → Borrower hears
```

### Environment Variables

```bash
# Cartesia TTS (required for voice)
CARTESIA_API_KEY=your_cartesia_key

# ASR providers (at least one required; order = fallback priority)
DEEPGRAM_API_KEY=your_deepgram_key        # Primary: $0.0043/min, lowest latency
GOOGLE_STT_API_KEY=your_google_key        # Fallback 1: $0.024/min, widest language support
BHASHINI_API_KEY=your_bhashini_key        # Fallback 2: Free, government, 22 Indian languages
BHASHINI_USER_ID=your_bhashini_user_id
BHASHINI_PIPELINE_ID=64392f96daac500b55c543cd
```

### Quick Start -- Voice Call

```python
from app.voice.voice_channel import VoiceChannel

channel = VoiceChannel()

# Start call (returns greeting audio)
result = await channel.start_call(
    channel_user_id="9876543210",
    lender_id="LENDER_001",
    language="hi",
    segment="DAIRY_FARMER",
)
# result["greeting_audio"] = base64-encoded PCM audio
# result["greeting_text"] = "Namaste! Main aapka lending assistant hoon..."

# Process borrower audio
turn = await channel.process_audio_turn(
    call_id=result["call_id"],
    audio_bytes=raw_pcm_bytes,  # 16kHz, 16-bit, mono
)
# turn["transcription"] = what borrower said
# turn["response_text"] = agent's reply
# turn["response_audio"] = base64 TTS audio
# turn["tools_called"] = ["compute_segment_score", ...]

# End call
summary = await channel.end_call(result["call_id"])
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/voice/start` | POST | Start voice session, get greeting audio |
| `/api/voice/turn` | POST | Send borrower audio, get agent response audio |
| `/api/voice/end/{call_id}` | POST | End session, get summary |
| `/api/voice/calls/active` | GET | List active calls |

### Audio Format

- **Input (ASR)**: Raw PCM, 16kHz sample rate, 16-bit signed little-endian, mono
- **Output (TTS)**: Raw PCM, 16kHz sample rate, 16-bit signed little-endian, mono
- **Transport**: Base64-encoded in JSON payloads

### Supported Languages

| Code | Language | TTS (Cartesia) | ASR (Deepgram) | ASR (Google) | ASR (Bhashini) |
|------|----------|----------------|----------------|-------------|----------------|
| hi | Hindi | Yes | Yes | Yes | Yes |
| en | English | Yes | Yes (en-IN) | Yes (en-IN) | Yes |
| gu | Gujarati | Yes | Yes | Yes | Yes |
| ta | Tamil | Yes | Yes | Yes | Yes |
| te | Telugu | Yes | Yes | Yes | Yes |
| bn | Bengali | Yes | Yes | Yes | Yes |
| mr | Marathi | Yes | Yes | Yes | Yes |
| kn | Kannada | Yes | Yes | Yes | Yes |
| ml | Malayalam | Yes | Yes | Yes | Yes |
| pa | Punjabi | Yes | Yes | Yes | Yes |

---

## 2. Multi-Provider ASR Integration

### How Fallback Works

```
Audio → Deepgram (if key set)
          ↓ (on failure or empty)
        Google Speech (if key set)
          ↓ (on failure or empty)
        Bhashini (if key set)
          ↓ (all failed)
        Error returned (never raises)
```

### Standalone Usage

```python
from app.voice.asr_provider import ASRConfig, MultiProviderASR

asr = MultiProviderASR(ASRConfig(
    deepgram_api_key="...",
    google_api_key="...",       # optional
    bhashini_api_key="...",     # optional
))

result = await asr.transcribe(
    audio_bytes=pcm_audio,
    language="hi",
    sample_rate=16000,
)

print(result.text)            # "Mujhe loan chahiye"
print(result.confidence)      # 0.94
print(result.provider_used)   # "deepgram"
print(result.alternatives)    # ["Mujhe lon chahiye", ...]
```

### Custom Fallback Order

```python
from app.voice.asr_provider import ASRConfig, ASRProvider

config = ASRConfig(
    bhashini_api_key="...",
    deepgram_api_key="...",
    fallback_order=[ASRProvider.BHASHINI, ASRProvider.DEEPGRAM],  # Bhashini first
)
```

---

## 3. Standalone Credit Decisioning

### When to Use

- **Always**: As the local decisioning engine for all credit decisions
- **With Sentinel**: Run both, use `shadow_compare()` to validate alignment
- **Without Sentinel**: Full standalone operation, no external dependency

### Usage

```python
from app.policy.standalone_decisioning import StandaloneDecisionEngine

engine = StandaloneDecisionEngine()

decision = engine.decide(
    borrower_id="B001",
    segment="DAIRY_FARMER",
    score=720,
    grade="A2",
    confidence=0.85,
    fraud_score=0.1,
    requested_amount=95000,
    monthly_income=25000,
    existing_obligations=5000,
    feature_contributions={"pouring_regularity": 0.23, "bureau_score": 0.12},
)

print(decision.decision)         # "APPROVE"
print(decision.approved_amount)  # 95000.0
print(decision.interest_rate)    # 15.0
print(decision.reason_codes)     # ["SCORE_ABOVE_THRESHOLD"]
print(decision.explanation)      # Full explainability
print(decision.audit_trail)      # RBI-compliant audit
```

### Shadow Testing Against Sentinel

```python
# When Sentinel becomes available after enterprise onboarding
sentinel_result = await sentinel_client.trigger_credit_decision(...)

comparison = engine.shadow_compare(local_decision, sentinel_result)
print(comparison["match"])         # True/False
print(comparison["recommendation"])  # Log for analysis
```

### Segment Policies Configured

| Segment | Auto-Approve | Auto-Reject | Max Amount | Rate Grid |
|---------|-------------|-------------|-----------|-----------|
| DAIRY_FARMER | >= 650 | <= 350 | 2,00,000 | 13-20% |
| STREET_VENDOR | >= 600 | <= 300 | 50,000 | 16-22% |
| GIG_WORKER | >= 620 | <= 320 | 1,00,000 | 14-22% |
| KIRANA_SHOP | >= 640 | <= 350 | 3,00,000 | 14-20% |
| SHG_MEMBER | >= 580 | <= 300 | 50,000 | 12-18% |
| FISHERY | >= 620 | <= 350 | 3,00,000 | 14-20% |
| CONSTRUCTION_WORKER | >= 600 | <= 300 | 75,000 | 16-24% |
| EV_FINANCING | >= 650 | <= 380 | 5,00,000 | 10-16% |

---

## 4. ML Training Pipeline

### Training a Segment Model

```python
from app.tools.scoring.ml_training import SegmentModelTrainer, TrainingConfig

trainer = SegmentModelTrainer()

# Train with synthetic data (bootstraps from rule-based weights)
config = TrainingConfig(
    segment="DAIRY_FARMER",
    n_samples=5000,
    test_ratio=0.20,
)
model = trainer.train(config)

print(model.metrics.gini)    # e.g. 0.42
print(model.metrics.ks)      # e.g. 0.34
print(model.metrics.auc)     # e.g. 0.71
print(model.model_path)      # "models/dairy_farmer_xgb_v1.json" (if XGBoost installed)
```

### Champion/Challenger

```python
from app.tools.scoring.ml_training import compare_models

champion = trainer.train(TrainingConfig(segment="DAIRY_FARMER", n_samples=2000))
challenger = trainer.train(TrainingConfig(segment="DAIRY_FARMER", n_samples=5000))

result = compare_models(champion, challenger)
print(result["recommendation"])  # "PROMOTE_CHALLENGER" or "KEEP_CHAMPION"
print(result["gini_improvement"])
```

### Transitioning from Rule-Based to ML

1. **Phase 1** (now): Rule-based scoring in production (`compute_segment_score`)
2. **Phase 2**: Train ML models on synthetic data, run in shadow mode alongside rule-based
3. **Phase 3**: When real loan outcome data available (90+ days), retrain on real outcomes
4. **Phase 4**: Promote ML model when Gini improvement > 0.02 AND KS improvement > 0.01

### Installing XGBoost (optional, falls back to rule-based eval)

```bash
pip install xgboost scikit-learn numpy
```

---

## 5. Running Evaluations

### Voice AI Eval Suite

```python
from app.voice.eval_framework import TTSEvaluator, ASREvaluator, PipelineEvaluator

# TTS only
tts_report = await TTSEvaluator().eval_suite()
print(tts_report.pass_rate)     # e.g. 1.0
print(tts_report.avg_latency_ms)

# ASR only (mock mode for CI)
asr_report = await ASREvaluator().eval_suite_mock()
print(asr_report.pass_rate)

# Full pipeline round-trip
pipeline_report = await PipelineEvaluator().eval_suite()
print(pipeline_report.to_dict())
```

### Eval Cases Covered

| Category | Languages | Segments | Intents |
|----------|-----------|----------|---------|
| Loan inquiry | hi, gu, ta, te, bn, en, mr | DAIRY_FARMER, STREET_VENDOR, FISHERY, KIRANA_SHOP, CONSTRUCTION_WORKER, EV_FINANCING | loan_inquiry |
| Repayment | hi | GIG_WORKER | repayment_status |
| Emergency | hi | DAIRY_FARMER | emergency |
| Complaint | hi | SHG_MEMBER | complaint |

### Adding Custom Eval Cases

```python
from app.voice.eval_framework import EvalCase

custom_cases = [
    EvalCase(
        case_id="custom_01",
        language="hi",
        segment="DAIRY_FARMER",
        input_text="Meri bhens beemar hai, emergency loan chahiye",
        expected_keywords=["bhens", "emergency", "loan"],
        expected_intent="emergency",
        max_tts_latency_ms=1500,
        min_asr_confidence=0.7,
    ),
]

report = await PipelineEvaluator().eval_suite(custom_cases)
```

---

## 6. Production Checklist

### Voice AI
- [ ] Cartesia API key configured and tested
- [ ] At least one ASR provider key configured
- [ ] TTS eval suite passes > 95% across all languages
- [ ] ASR eval suite passes > 90% with real audio samples
- [ ] Pipeline round-trip latency < 3 seconds (P95)
- [ ] Voice recording consent implemented (DPDP compliance)
- [ ] Human escalation working for low-confidence ASR (< 0.5)
- [ ] Segment-specific greetings tested in target languages

### Credit Decisioning
- [ ] Standalone engine tested for all 8 configured segments
- [ ] Fraud gate blocks scores > threshold
- [ ] DTI gate refers high-obligation borrowers
- [ ] Amount calibration caps at segment max
- [ ] Audit trail captures every decision with explainability
- [ ] Shadow comparison ready for Sentinel onboarding

### ML Training
- [ ] Synthetic data generates reasonable default rates (5-45%)
- [ ] Models trainable for all segments without errors
- [ ] Metrics (Gini, KS, AUC) within valid ranges
- [ ] Champion/challenger comparison logic validated
- [ ] Model serialization working (XGBoost .json files)
- [ ] Plan for real outcome data collection (90-day pipeline)
