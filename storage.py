import json

from config import FIELD_TYPES
from models import Earthquake


def parse_value(name: str, value: object, line_number: int) -> object:
    field_type = FIELD_TYPES[name]

    if value is None or value == "":
        return None

    if field_type is str:
        if not isinstance(value, str):
            raise ValueError(f"Строка {line_number}: поле {name} должно быть строкой")
        return value

    if field_type is float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Строка {line_number}: поле {name} должно быть числом")
        return float(value)

    if not isinstance(value, bool):
        raise ValueError(
            f"Строка {line_number}: поле {name} должно быть true или false"
        )
    return value


def parse_record(data: dict, line_number: int) -> Earthquake:
    for name in ("id", "title"):
        value = data.get(name)
        if not isinstance(value, str) or value == "":
            raise ValueError(f"Строка {line_number}: нет поля {name}")

    record = {}

    for name in FIELD_TYPES:
        record[name] = parse_value(name, data.get(name), line_number)

    return record


def load_records(path: str) -> list[Earthquake]:
    records = []
    seen_ids = set()

    with open(path, encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            data = json.loads(line)

            if not isinstance(data, dict):
                raise ValueError(f"Строка {line_number}: ожидался объект JSON")

            record = parse_record(data, line_number)

            if record["id"] in seen_ids:
                raise ValueError(f"Строка {line_number}: повторяется id {record['id']}")

            seen_ids.add(record["id"])
            records.append(record)

    return records


def save_result(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)
