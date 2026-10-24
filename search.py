import time
import filters
from config import RESULT_LIMIT, SEARCH_FIELDS
from models import Earthquake, Filter, SearchResult


def split_words(text: str) -> list[str]:
    return text.split()


def levenshtein_distance(first: str, second: str) -> int:
    rows = len(first) + 1
    cols = len(second) + 1

    table = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        table[i][0] = i

    for j in range(cols):
        table[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            if first[i - 1] == second[j - 1]:
                cost = 0
            else:
                cost = 1

            table[i][j] = min(
                table[i - 1][j] + 1,
                table[i][j - 1] + 1,
                table[i - 1][j - 1] + cost,
            )

    return table[-1][-1]


def word_similarity(first: str, second: str) -> float:
    longest = max(len(first), len(second))

    if longest == 0:
        return 1.0

    distance = levenshtein_distance(first, second)
    return 1.0 - distance / longest


def get_record_words(record: Earthquake) -> list[str]:
    words = []

    for name in SEARCH_FIELDS:
        value = record[name]

        if value is not None:
            words.extend(split_words(str(value)))

    return words


def match_record(
    record: Earthquake,
    query_words: list[str],
    threshold: float,
) -> float | None:
    if not query_words:
        return 0.0

    record_words = get_record_words(record)
    total = 0.0

    for query_word in query_words:
        best = 0.0

        for record_word in record_words:
            similarity = word_similarity(query_word, record_word)

            if similarity > best:
                best = similarity

        if best < threshold:
            return None

        total += best

    return total / len(query_words)


def get_relevance(result: SearchResult) -> float:
    return result[1]


def search_records(
    records: list[Earthquake],
    query: str,
    conditions: list[Filter],
    threshold: float,
    ratings: dict[str, int],
) -> tuple[list[SearchResult], int, float]:
    start = time.time()
    query_words = split_words(query)
    results = []

    for record in records:
        if not filters.matches_filters(record, conditions):
            continue

        relevance = match_record(record, query_words, threshold)

        if relevance is not None:
            rating = ratings.get(record["id"])
            results.append((record, relevance, rating))

    found_count = len(results)

    results.sort(key=get_relevance, reverse=True)
    results = results[:RESULT_LIMIT]

    elapsed_ms = (time.time() - start) * 1000

    return results, found_count, elapsed_ms
