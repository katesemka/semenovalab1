from config import FIELD_TYPES, FILTER_OPERATORS
from models import Earthquake, Filter


def convert_filter_value(field_name: str, raw_value: str) -> str | float | bool:
    field_type = FIELD_TYPES[field_name]

    if field_type is str:
        try:
            return str(raw_value)
        except ValueError:
            raise ValueError(f"Поле {field_name} должно быть строкой") from None

    if field_type is float:
        try:
            return float(raw_value)
        except ValueError:
            raise ValueError(f"Поле {field_name} должно быть числом") from None

    if raw_value == "true":
        return True
    if raw_value == "false":
        return False

    raise ValueError(f"Поле {field_name} должно быть true или false")


def parse_filter(field_name: str, operator: str, raw_value: str) -> Filter:
    if field_name not in FIELD_TYPES:
        raise ValueError(f"Неизвестное поле: {field_name}")

    field_type = FIELD_TYPES[field_name]

    if operator not in FILTER_OPERATORS[field_type]:
        raise ValueError(f"Оператор {operator} недопустим для поля {field_name}")

    value = convert_filter_value(field_name, raw_value)

    return field_name, operator, value


def matches_filter(record: Earthquake, condition: Filter) -> bool:
    field_name, operator, expected = condition
    value = record[field_name]

    if value is None or value == "":
        return False

    if operator == "eq":
        return value == expected
    elif operator == "ne":
        return value != expected
    elif operator == "lt":
        return value < expected
    elif operator == "le":
        return value <= expected
    elif operator == "gt":
        return value > expected
    elif operator == "ge":
        return value >= expected
    elif operator == "contains":
        return expected in value


def matches_filters(record: Earthquake, conditions: list[Filter]) -> bool:
    for condition in conditions:
        if not matches_filter(record, condition):
            return False

    return True
