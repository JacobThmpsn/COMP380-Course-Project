from metrics import compute_metrics
from ai_client import score_with_ai


def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x


def difficulty_score(m):

    s = (m["avg_sentence_len"] - 12.0) / (28.0 - 12.0)
    s = clamp(s, 0.0, 1.0)

    y = (m["syllables_per_word"] - 1.3) / (2.0 - 1.3)
    y = clamp(y, 0.0, 1.0)

    u = m["uncommon_word_rate"]
    r = m["rare_word_rate"]

    u_norm = (u - 0.10) / (0.35 - 0.10)
    u_norm = clamp(u_norm, 0.0, 1.0)

    r_norm = (r - 0.02) / (0.10 - 0.02)
    r_norm = clamp(r_norm, 0.0, 1.0)

    vocab_score = clamp(0.65 * u_norm + 0.35 * r_norm, 0.0, 1.0)

    raw = 0.40 * s + 0.25 * y + 0.35 * vocab_score

    return round(raw * 100, 1)


def score_band(score):

    if score < 20:
        return "Easy"
    if score < 40:
        return "Low"
    if score < 60:
        return "Medium"
    if score < 80:
        return "High"
    return "Hard"


def reading_expectations(m):

    items = []

    if m["avg_sentence_len"] > 22:
        items.append("Expect long sentences that require slower reading.")

    if m["syllables_per_word"] > 1.8:
        items.append("Expect frequent multi syllable vocabulary.")

    if m["uncommon_word_rate"] > 0.25:
        items.append("Expect uncommon vocabulary and specialized terms.")

    if m["rare_word_rate"] > 0.05:
        items.append("Expect rare or technical terminology.")

    if m["long_word_rate"] > 0.18:
        items.append("Expect frequent long words which slow scanning.")

    if not items:
        items.append("Expect short sentences and familiar vocabulary.")

    return items


def build_report(text):

    metrics = compute_metrics(text)

    score = difficulty_score(metrics)

    ai = score_with_ai(text, metrics)

    report = {
        "score": score,
        "band": score_band(score),
        "reasons": ai["reasons"],
        "complex_words": ai["complex_words"],
        "reading_expectations": reading_expectations(metrics),
        "metrics": metrics
    }

    return report