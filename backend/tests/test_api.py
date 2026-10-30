import random
from collections import Counter

import pytest
from fastapi.testclient import TestClient

from app import mbti_engine
from app.main import app
from app.profiles import PROFILES
from app.questions import DICHOTOMIES, QUESTIONS, QUESTIONS_BY_DICHOTOMY

client = TestClient(app)


def test_bank_shape():
    assert len(QUESTIONS) >= 100
    assert len({q.id for q in QUESTIONS}) == len(QUESTIONS)
    assert len({q.text for q in QUESTIONS}) == len(QUESTIONS)
    for dim in DICHOTOMIES:
        pool = QUESTIONS_BY_DICHOTOMY[dim]
        assert len(pool) >= 25
        directions = Counter(q.direction for q in pool)
        assert directions[1] == directions[-1]


def test_all_16_profiles_present():
    types = {a + b + c + d for a in "EI" for b in "SN" for c in "TF" for d in "JP"}
    assert set(PROFILES) == types


@pytest.mark.parametrize(
    "mbti_type,stack",
    [
        ("INTJ", ["Ni", "Te", "Fi", "Se"]),
        ("ENFP", ["Ne", "Fi", "Te", "Si"]),
        ("ISTP", ["Ti", "Se", "Ni", "Fe"]),
        ("ESFJ", ["Fe", "Si", "Ne", "Ti"]),
        ("INFJ", ["Ni", "Fe", "Ti", "Se"]),
        ("ESTP", ["Se", "Ti", "Fe", "Ni"]),
    ],
)
def test_cognitive_stack(mbti_type, stack):
    assert mbti_engine.cognitive_stack(mbti_type) == stack


@pytest.mark.parametrize("count", mbti_engine.ALLOWED_COUNTS)
def test_questions_balanced(count):
    res = client.get("/api/questions", params={"count": count})
    assert res.status_code == 200
    items = res.json()
    assert len(items) == count
    assert len({q["id"] for q in items}) == count
    per_dim = Counter(q["dichotomy"] for q in items)
    assert set(per_dim) == set(DICHOTOMIES)
    assert max(per_dim.values()) - min(per_dim.values()) <= 1


def test_questions_rejects_bad_count():
    assert client.get("/api/questions", params={"count": 30}).status_code == 422


def _answers_for(target: str, strength: int = 3) -> list[dict]:
    """Answer every question so as to push toward each letter of `target`."""
    answers = []
    for q in QUESTIONS:
        wants_first = target[DICHOTOMIES.index(q.dichotomy)] == q.dichotomy[0]
        answers.append({"question_id": q.id, "score": strength * q.direction * (1 if wants_first else -1)})
    return answers


@pytest.mark.parametrize("mbti_type", sorted(PROFILES))
def test_submit_recovers_type(mbti_type):
    res = client.post("/api/submit", json={"answers": _answers_for(mbti_type)})
    assert res.status_code == 200
    body = res.json()
    assert body["mbti_type"] == mbti_type
    for letter in mbti_type:
        assert body["percentages"][letter] == 100
    profile = body["psychological_profile"]
    assert set(profile) == {"core_drivers", "cognitive_functions", "strengths_growth", "interpersonal"}
    assert len(profile["cognitive_functions"]["function_stack"]) == 4


def test_percentages_sum_and_ties():
    neutral = [{"question_id": q.id, "score": 0} for q in QUESTIONS]
    body = client.post("/api/submit", json={"answers": neutral}).json()
    assert body["mbti_type"] == "INFP"  # ties go to the second pole
    for a, b in DICHOTOMIES:
        assert body["percentages"][a] + body["percentages"][b] == 100


def test_partial_strength():
    answers = _answers_for("ESTJ", strength=1)
    body = client.post("/api/submit", json={"answers": answers}).json()
    assert body["mbti_type"] == "ESTJ"
    assert body["percentages"]["E"] == 67  # 50 + 50 * 1/3, half-up


def test_submit_validation():
    one_per_dim = [{"question_id": QUESTIONS_BY_DICHOTOMY[d][0].id, "score": 1} for d in DICHOTOMIES]
    assert client.post("/api/submit", json={"answers": one_per_dim}).status_code == 200
    assert client.post("/api/submit", json={"answers": one_per_dim[:3] * 2}).status_code == 422  # dup + missing JP
    bad_id = [*one_per_dim, {"question_id": "q999", "score": 1}]
    assert client.post("/api/submit", json={"answers": bad_id}).status_code == 422
    bad_score = [{**one_per_dim[0], "score": 4}, *one_per_dim[1:]]
    assert client.post("/api/submit", json={"answers": bad_score}).status_code == 422


def test_sampling_never_exceeds_pool():
    rng = random.Random(0)
    for _ in range(200):
        assert len(mbti_engine.sample_questions(100, rng)) == 100


@pytest.mark.parametrize(("env_value", "status"), [(None, 200), ("false", 404)])
def test_api_docs_toggle(monkeypatch, env_value, status):
    import importlib

    import app.main as main_module

    if env_value is None:
        monkeypatch.delenv("ENABLE_API_DOCS", raising=False)
    else:
        monkeypatch.setenv("ENABLE_API_DOCS", env_value)
    try:
        fresh = TestClient(importlib.reload(main_module).app)
        assert fresh.get("/api/docs").status_code == status
        assert fresh.get("/api/openapi.json").status_code == status
    finally:
        monkeypatch.undo()
        importlib.reload(main_module)
