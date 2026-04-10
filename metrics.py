import re
from collections import Counter
from wordfreq import zipf_frequency


def split_words(text):
    return re.findall(r"[A-Za-z']+", text.lower())


def count_sentences(text):
    sentences = re.split(r"[.!?]+", text)
    return max(1, len([s for s in sentences if s.strip()]))


def estimate_syllables(word):

    vowels = "aeiouy"
    count = 0
    prev = False

    for char in word.lower():
        is_vowel = char in vowels
        if is_vowel and not prev:
            count += 1
        prev = is_vowel

    if word.endswith("e") and count > 1:
        count -= 1

    return max(1, count)


def compute_metrics(text):

    words = split_words(text)

    word_count = max(1, len(words))
    sentence_count = count_sentences(text)

    avg_word_len = sum(len(w) for w in words) / word_count
    avg_sentence_len = word_count / sentence_count

    syllables = sum(estimate_syllables(w) for w in words)
    syllables_per_word = syllables / word_count

    long_words = [w for w in words if len(w) >= 8]
    long_word_rate = len(long_words) / word_count

    uncommon_words = []
    rare_words = []

    for w in words:

        freq = zipf_frequency(w, "en")

        if freq < 4.0:
            uncommon_words.append(w)

        if freq < 3.0:
            rare_words.append(w)

    uncommon_word_rate = len(uncommon_words) / word_count
    rare_word_rate = len(rare_words) / word_count

    long_counts = Counter(long_words)
    uncommon_counts = Counter(uncommon_words)

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_word_len": round(avg_word_len, 2),
        "avg_sentence_len": round(avg_sentence_len, 2),
        "syllables_per_word": round(syllables_per_word, 2),
        "long_word_rate": round(long_word_rate, 3),
        "uncommon_word_rate": round(uncommon_word_rate, 3),
        "rare_word_rate": round(rare_word_rate, 3),
        "top_long_words": [w for w, _ in long_counts.most_common(10)],
        "top_uncommon_words": [w for w, _ in uncommon_counts.most_common(10)]
    }