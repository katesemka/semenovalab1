from config import FIELD_TYPES, FILTER_OPERATORS, SEARCH_FIELDS
from models import Earthquake, Filter, SearchResult


def format_value(value: object) -> str:
    if value is None:
        return "-"
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def format_record(
    record: Earthquake,
    relevance: float | None = None,
    rating: int | None = None,
) -> str:
    lines = [f"[{record['id']}] {format_value(record['title'])}"]

    for name in FIELD_TYPES:
        if name == "id" or name == "title":
            continue
        lines.append(f"  {name}: {format_value(record[name])}")

    if relevance is not None:
        lines.append(f"  Релевантность: {relevance:.2f}")

        if rating is not None:
            lines.append(f"  Оценка: {rating}/5")
        else:
            lines.append("  Оценка: нет")

    return "\n".join(lines)


def format_records(records: list[Earthquake]) -> str:
    lines = [f"Записей: {len(records)}"]
    cards = [format_record(record) for record in records]

    if cards:
        lines.append("")
        lines.append("\n\n".join(cards))

    return "\n".join(lines)


def format_search_results(
    results: list[SearchResult],
    found_count: int,
    elapsed_ms: float,
) -> str:
    lines = [f"Найдено: {found_count}; показано: {len(results)}"]

    cards = [
        format_record(record, relevance, rating)
        for record, relevance, rating in results
    ]

    if cards:
        lines.append("")
        lines.append("\n\n".join(cards))

    lines.append("")
    lines.append(f"Время поиска: {elapsed_ms:.2f} мс")

    return "\n".join(lines)


def format_fields() -> str:
    lines = [
        f"Поиск по полям: {', '.join(SEARCH_FIELDS)}",
        "",
        f"{'Поле':<10}  {'Тип':<5}  Фильтры",
        f"{'-' * 10}  {'-' * 5}  {'-' * 17}",
    ]

    for name, field_type in FIELD_TYPES.items():
        operators = " ".join(FILTER_OPERATORS[field_type])
        lines.append(f"{name:<10}  {field_type.__name__:<5}  {operators}")

    lines.append("")
    lines.append("eq = равно; ne = не равно; contains = содержит текст.")
    lines.append("lt <; le <=; gt >; ge >=. true = да; false = нет.")

    return "\n".join(lines)


def format_filter(condition: Filter) -> str:
    field_name, operator, value = condition
    return f"{field_name} {operator} {format_value(value)}"


def format_filters(conditions: list[Filter]) -> str:
    if not conditions:
        return "Фильтров нет"

    lines = []

    for number, condition in enumerate(conditions, start=1):
        lines.append(f"{number}. {format_filter(condition)}")

    return "\n".join(lines)


def format_ratings(ratings: dict[str, int]) -> str:
    if not ratings:
        return "Оценок нет"

    lines = [f"{record_id}: {value}/5" for record_id, value in ratings.items()]

    return "\n".join(lines)
