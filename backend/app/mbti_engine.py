"""Question sampling, scoring, and assembly of the personality analysis.

Scoring model
-------------
Each answer is a 7-point Likert score in [-3, +3]. Multiplying by the item's
`direction` converts it into a signed vote for the dichotomy's first pole
(E, S, T, J). Per dichotomy:

    first_pct = 50 + 50 * sum(score * direction) / (3 * answered)

so all-maximum agreement with first-pole items gives 100%, a neutral set gives
50%. Normalising by the number answered keeps dichotomies comparable when the
sampled counts differ (25 and 75 are not divisible by 4).

An exact tie goes to the second pole (I, N, F, P), the convention used by
the original MBTI scoring manual.
"""

import random
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from .profiles import FUNCTION_DESCRIPTIONS, FUNCTION_NAMES, PROFILES, STACK_POSITIONS
from .questions import DICHOTOMIES, QUESTIONS_BY_DICHOTOMY, QUESTIONS_BY_ID, Dichotomy, Question

ALLOWED_COUNTS = (25, 50, 75, 100)
MAX_SCORE = 3

POLE_NAMES: dict[str, tuple[str, str]] = {
    "E": ("Hướng ngoại", "Extraversion"),
    "I": ("Hướng nội", "Introversion"),
    "S": ("Cảm nhận", "Sensing"),
    "N": ("Trực giác", "Intuition"),
    "T": ("Lý trí", "Thinking"),
    "F": ("Cảm xúc", "Feeling"),
    "J": ("Nguyên tắc", "Judging"),
    "P": ("Linh hoạt", "Perceiving"),
}

# (upper bound of distance from 50, key, Vietnamese label); first match wins.
CLARITY_BANDS: tuple[tuple[int, str, str], ...] = (
    (5, "slight", "nhẹ"),
    (15, "moderate", "vừa phải"),
    (25, "clear", "rõ ràng"),
    (50, "very_clear", "rất rõ ràng"),
)

DISCLAIMER = (
    "Kết quả mang tính tham khảo để tự khám phá bản thân, không phải chẩn đoán tâm lý "
    "hay công cụ đánh giá tuyển dụng. Tính cách là một phổ liên tục và có thể thay đổi "
    "theo thời gian, hoàn cảnh và sự trưởng thành của mỗi người."
)


class ScoringError(ValueError):
    """Answers cannot be scored (unknown IDs, duplicates, or a dichotomy with no answers)."""


@dataclass(frozen=True, slots=True)
class DimensionScore:
    dichotomy: Dichotomy
    letter: str
    first_pct: int
    second_pct: int
    answered: int

    @property
    def clarity(self) -> tuple[str, str]:
        distance = abs(self.first_pct - 50)
        for bound, key, label in CLARITY_BANDS:
            if distance <= bound:
                return key, label
        raise AssertionError("unreachable: distance is at most 50")


# --- sampling -------------------------------------------------------------------


def sample_questions(count: int, rng: random.Random | None = None) -> list[Question]:
    """Pick `count` questions spread evenly across dichotomies and keying directions."""
    if count not in ALLOWED_COUNTS:
        raise ValueError(f"count must be one of {ALLOWED_COUNTS}")
    rng = rng or random.Random()

    per_dim, remainder = divmod(count, len(DICHOTOMIES))
    # Which dichotomies get the extra question when count isn't a multiple of 4 is random,
    # so no dimension is systematically measured with more items.
    dims = list(DICHOTOMIES)
    rng.shuffle(dims)

    picked: list[Question] = []
    for i, dim in enumerate(dims):
        n = per_dim + (1 if i < remainder else 0)
        pool = QUESTIONS_BY_DICHOTOMY[dim]
        pos = [q for q in pool if q.direction == 1]
        neg = [q for q in pool if q.direction == -1]
        n_pos = n // 2 + (rng.randrange(2) if n % 2 else 0)
        picked += rng.sample(pos, n_pos) + rng.sample(neg, n - n_pos)

    rng.shuffle(picked)
    return picked


# --- scoring --------------------------------------------------------------------


def _round_half_up(x: float) -> int:
    return int(x + 0.5)


def score_answers(answers: Iterable[tuple[str, int]]) -> dict[Dichotomy, DimensionScore]:
    totals: dict[Dichotomy, int] = defaultdict(int)
    counts: dict[Dichotomy, int] = defaultdict(int)
    seen: set[str] = set()

    for question_id, score in answers:
        question = QUESTIONS_BY_ID.get(question_id)
        if question is None:
            raise ScoringError(f"unknown question_id: {question_id}")
        if question_id in seen:
            raise ScoringError(f"duplicate question_id: {question_id}")
        if not -MAX_SCORE <= score <= MAX_SCORE:
            raise ScoringError(f"score out of range for {question_id}: {score}")
        seen.add(question_id)
        totals[question.dichotomy] += score * question.direction
        counts[question.dichotomy] += 1

    missing = [d for d in DICHOTOMIES if counts[d] == 0]
    if missing:
        raise ScoringError(f"no answers for dichotomies: {', '.join(missing)}")

    result: dict[Dichotomy, DimensionScore] = {}
    for dim in DICHOTOMIES:
        raw = totals[dim]
        first_pct = _round_half_up(50 + 50 * raw / (MAX_SCORE * counts[dim]))
        # Keep the displayed split consistent with the chosen letter for near-ties.
        if raw > 0 and first_pct == 50:
            first_pct = 51
        elif raw < 0 and first_pct == 50:
            first_pct = 49
        result[dim] = DimensionScore(
            dichotomy=dim,
            letter=dim[0] if raw > 0 else dim[1],
            first_pct=first_pct,
            second_pct=100 - first_pct,
            answered=counts[dim],
        )
    return result


# --- analysis -------------------------------------------------------------------


def cognitive_stack(mbti_type: str) -> list[str]:
    """Dominant, auxiliary, tertiary, inferior functions (Myers/Beebe ordering).

    J/P names the function shown to the outer world: J types extravert their
    judging function (T/F), P types their perceiving function (S/N). Extraverts
    lead with that extraverted function, introverts with the introverted one.
    """
    e_i, perceiving, judging, j_p = mbti_type
    if j_p == "J":
        extraverted, introverted = f"{judging}e", f"{perceiving}i"
    else:
        extraverted, introverted = f"{perceiving}e", f"{judging}i"
    dominant, auxiliary = (extraverted, introverted) if e_i == "E" else (introverted, extraverted)

    opposite = {"S": "N", "N": "S", "T": "F", "F": "T"}
    flip = {"e": "i", "i": "e"}
    # Tertiary: opposite of the auxiliary, in the dominant's attitude.
    tertiary = opposite[auxiliary[0]] + dominant[1]
    # Inferior: opposite of the dominant, in the opposite attitude.
    inferior = opposite[dominant[0]] + flip[dominant[1]]
    return [dominant, auxiliary, tertiary, inferior]


def _dimension_insight(dim: DimensionScore) -> dict:
    first, second = dim.dichotomy[0], dim.dichotomy[1]
    clarity_key, clarity_label = dim.clarity
    pole_vi = POLE_NAMES[dim.letter][0]
    pct = dim.first_pct if dim.letter == first else dim.second_pct
    if clarity_key == "slight":
        note = (
            f"Hai xu hướng {POLE_NAMES[first][0]} và {POLE_NAMES[second][0]} của bạn gần như cân bằng "
            f"({pct}% nghiêng về {pole_vi}). Bạn có thể linh hoạt sử dụng cả hai tùy hoàn cảnh, "
            "nên hãy đọc phần mô tả liên quan với tinh thần cởi mở."
        )
    else:
        note = f"Bạn nghiêng về {pole_vi} ở mức {clarity_label} ({pct}%)."
    return {
        "dichotomy": dim.dichotomy,
        "preferred": dim.letter,
        "preferred_name": pole_vi,
        "clarity": clarity_key,
        "clarity_label": clarity_label,
        "answered": dim.answered,
        "note": note,
    }


def build_result(scores: dict[Dichotomy, DimensionScore]) -> dict:
    mbti_type = "".join(scores[d].letter for d in DICHOTOMIES)
    profile = PROFILES[mbti_type]

    percentages: dict[str, int] = {}
    for dim in DICHOTOMIES:
        percentages[dim[0]] = scores[dim].first_pct
        percentages[dim[1]] = scores[dim].second_pct

    stack = [
        {
            "position": position_vi,
            "position_en": position_en,
            "function": fn,
            "name": FUNCTION_NAMES[fn][0],
            "name_en": FUNCTION_NAMES[fn][1],
            "role": role,
            "description": FUNCTION_DESCRIPTIONS[fn],
        }
        for fn, (position_vi, position_en, role) in zip(cognitive_stack(mbti_type), STACK_POSITIONS)
    ]
    stack_summary = " → ".join(f"{s['function']} ({s['name']})" for s in stack)

    return {
        "mbti_type": mbti_type,
        "type_title": f"{profile.title_vi} ({profile.title_en})",
        "type_title_vi": profile.title_vi,
        "type_title_en": profile.title_en,
        "tagline": profile.tagline,
        "percentages": percentages,
        "dimensions": [_dimension_insight(scores[d]) for d in DICHOTOMIES],
        "psychological_profile": {
            "core_drivers": {
                "title": "Động lực tâm lý cốt lõi & Thế giới quan",
                "title_en": "Core Psychological Drivers & Worldview",
                "content": profile.core_drivers,
            },
            "cognitive_functions": {
                "title": "Chức năng nhận thức & Cách xử lý thông tin",
                "title_en": "Cognitive Functions & Information Processing",
                "content": f"{profile.cognitive_processing} Thứ tự chức năng của bạn: {stack_summary}.",
                "function_stack": stack,
            },
            "strengths_growth": {
                "title": "Điểm mạnh & Định hướng phát triển",
                "title_en": "Strengths & Growth Mindset Areas",
                "content": (
                    "Điểm mạnh là những chức năng bạn sử dụng tự nhiên nhất; định hướng phát triển là "
                    "những vùng ít quen thuộc hơn, nơi một chút nỗ lực có ý thức mang lại nhiều cân bằng."
                ),
                "strengths": list(profile.strengths),
                "growth_areas": list(profile.growth_areas),
            },
            "interpersonal": {
                "title": "Tương tác & Phong cách đồng cảm",
                "title_en": "Interpersonal Dynamics & Empathy Style",
                "content": profile.interpersonal,
            },
        },
        "disclaimer": DISCLAIMER,
    }
