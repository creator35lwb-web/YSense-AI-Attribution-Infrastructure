"""
Smoke tests for YSenseAI v4.5-Beta.

Run from the repository root:  pytest v45_beta/tests

These do not call any AI provider. They cover the pieces that must work with
no API key at all: attribution, quality metrics, database, consent records,
and the import names the Streamlit app depends on (the bug class that broke
the documented entry point in earlier releases).
"""

import ast
import importlib
import sys
from pathlib import Path

import pytest

V45 = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(V45))

from attribution.attribution_engine import AttributionEngine  # noqa: E402
from attribution.quality_metrics import QualityMetricsCalculator  # noqa: E402
from database.schema import YSenseDatabase, hash_password, verify_password  # noqa: E402

STORY = (
    "My grandmother taught me to cook rendang when I was twelve. She said the secret "
    "was patience: you cannot rush the coconut paste as it darkens from cream to deep "
    "brown. Eight hours of stirring, and stories of her mother teaching her the same way."
)
LAYERS = {
    "narrative": "The unspoken story is about generational knowledge transfer.",
    "somatic": "Warmth from the fire, reverence in the chest, nostalgia in the heart.",
    "attention": "The paste darkening from cream to deep brown, like memories deepening.",
    "synesthetic": "Patient. Earthy. Sacred.",
    "temporal": "A low, steady hum, like time itself cooking.",
}
ESSENCE = ["Patience", "Tradition", "Alchemy"]


def test_attribution_roundtrip():
    engine = AttributionEngine()
    asset = engine.create_wisdom_asset(
        user_id="user_1", raw_story=STORY, layer_responses=LAYERS,
        distilled_essence=ESSENCE, consent_tier="tier1", quality_scores={"overall": 0.8},
    )
    assert asset["asset_id"].startswith("ysense-")
    assert asset["author_did"].startswith("did:ysense:")
    assert engine.verify_attribution(asset)["valid"] is True

    tampered = dict(asset)
    tampered["training_format"] = dict(asset["training_format"], input="changed")
    assert engine.verify_attribution(tampered)["valid"] is False


def test_quality_metrics_in_range():
    scores = QualityMetricsCalculator().calculate_all_metrics(STORY, LAYERS, ESSENCE)
    assert set(scores) >= {
        "context_efficiency", "reasoning_depth", "cultural_specificity",
        "emotional_richness", "attention_density", "compression_quality", "overall",
    }
    assert all(0.0 <= v <= 1.0 for v in scores.values())


def test_password_hashing_is_salted_and_backward_compatible():
    h1, h2 = hash_password("correct horse"), hash_password("correct horse")
    assert h1 != h2 and h1.startswith("scrypt$")
    assert verify_password("correct horse", h1)
    assert not verify_password("wrong", h1)
    import hashlib
    legacy = hashlib.sha256(b"old-pass").hexdigest()
    assert verify_password("old-pass", legacy)


def test_database_user_consent_and_deletion(tmp_path):
    db = YSenseDatabase(str(tmp_path / "t.db"))
    uid = db.create_user("a@example.com", "password123", "a")
    assert uid and db.create_user("a@example.com", "x", "dup") is None
    assert db.authenticate_user("a@example.com", "password123")["id"] == uid
    assert db.authenticate_user("a@example.com", "nope") is None
    assert db.get_user_by_email("a@example.com")["id"] == uid

    db.record_consent(uid, "privacy_policy", True, "1.0-beta", {"client": "test"})
    db.record_consent(uid, "research_participation", True, "1.0-beta")
    db.record_consent(uid, "research_participation", False, "1.0-beta")
    assert db.has_consent(uid, "privacy_policy")
    assert not db.has_consent(uid, "research_participation")
    assert len(db.get_user_consents(uid)) == 3

    asset = AttributionEngine().create_wisdom_asset(
        user_id=f"user_{uid}", raw_story=STORY, layer_responses=LAYERS,
        distilled_essence=ESSENCE, consent_tier="tier1", quality_scores={"overall": 0.8},
    )
    asset["distillation_dialogue"] = []
    db.create_submission(uid, asset)
    assert db.get_user_stats(uid)["total_submissions"] == 1

    counts = db.delete_user(uid)
    assert counts["users"] == 1 and counts["submissions"] == 1
    assert db.get_user_by_email("a@example.com") is None
    assert db.get_user_consents(uid) == []  # anonymised, no longer linked
    db.close()


def test_config_import_does_not_raise_without_keys(monkeypatch):
    for var in ("ANTHROPIC_API_KEY", "QWEN_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    sys.modules.pop("config", None)
    cfg = importlib.import_module("config")
    assert cfg.ANTHROPIC_MODEL
    assert "claude-3-" not in cfg.ANTHROPIC_MODEL, "retired model family"


def test_anthropic_client_offline_mode(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    sys.modules.pop("config", None)
    sys.modules.pop("agents.anthropic_integration_v45", None)
    mod = importlib.import_module("agents.anthropic_integration_v45")
    client = mod.AnthropicClient()
    assert client.use_fallback is True
    assert "offline" in client.generate_response("hello").lower()


@pytest.mark.parametrize("app", sorted(p.name for p in V45.glob("app_*.py")))
def test_app_imports_resolve(app):
    """Every `from X import a, b` in the app must name things that exist in X."""
    tree = ast.parse((V45 / app).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and (V45 / (node.module.replace(".", "/") + ".py")).exists():
            module = importlib.import_module(node.module)
            missing = [a.name for a in node.names if not hasattr(module, a.name)]
            assert not missing, f"{app}: {node.module} has no {missing}"
