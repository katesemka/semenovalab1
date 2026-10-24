import shlex

import filters
import output
import search
import storage
from config import DEFAULT_THRESHOLD
from models import AppState

COMMANDS = (
    "help",
    "load",
    "show",
    "fields",
    "filter",
    "threshold",
    "search",
    "save",
    "rate",
    "ratings",
    "exit",
)


def parse_command(line: str) -> list[str]:
    return shlex.split(line)


def handle_command(line: str, state: AppState) -> bool:
    parts = parse_command(line)

    if not parts:
        return True

    command = parts[0]
    args = parts[1:]

    if command not in COMMANDS:
        raise ValueError(f"Неизвестная команда: {command}")

    if not state["loaded"] and command not in ("help", "load", "exit"):
        raise ValueError("Сначала загрузите файл: load <файл>")

    if command == "help":
        if args:
            raise ValueError("Использование: help")
        handle_help()

    elif command == "load":
        if len(args) != 1:
            raise ValueError("Использование: load <файл>")
        handle_load(state, args[0])

    elif command == "show":
        if args:
            raise ValueError("Использование: show")
        handle_show(state)

    elif command == "fields":
        if args:
            raise ValueError("Использование: fields")
        handle_fields()

    elif command == "filter":
        if not args:
            raise ValueError("Использование: filter add/list/remove/clear")
        handle_filter(state, args)

    elif command == "threshold":
        if len(args) != 1:
            raise ValueError("Использование: threshold <число>")
        handle_threshold(state, args[0])

    elif command == "search":
        if len(args) != 1:
            raise ValueError('Использование: search "<запрос>"')
        handle_search(state, args[0])

    elif command == "save":
        if len(args) != 1:
            raise ValueError("Использование: save <файл>")
        handle_save(state, args[0])

    elif command == "rate":
        if len(args) != 2:
            raise ValueError("Использование: rate <id> <оценка>")
        handle_rate(state, args[0], args[1])

    elif command == "ratings":
        if args:
            raise ValueError("Использование: ratings")
        handle_ratings(state)

    elif command == "exit":
        if args:
            raise ValueError("Использование: exit")
        return False

    return True


def handle_help() -> None:
    print(
        """Команды:
help
load <файл>
show
fields
filter add <поле> <оператор> <значение>
filter list
filter remove <номер>
filter clear
threshold <число>
search "<запрос>"
save <файл>
rate <id> <оценка от 1 до 5>
ratings
exit"""
    )


def handle_load(state: AppState, path: str) -> None:
    records = storage.load_records(path)

    state["records"] = records
    state["loaded"] = True
    state["filters"].clear()
    state["ratings"].clear()
    state["last_ids"].clear()
    state["last_output"] = None
    state["threshold"] = DEFAULT_THRESHOLD

    print(f"Загружено записей: {len(records)}")


def handle_show(state: AppState) -> None:
    text = output.format_records(state["records"])
    print(text)

    state["last_output"] = text
    state["last_ids"] = {record["id"] for record in state["records"]}


def handle_fields() -> None:
    print(output.format_fields())


def handle_filter(state: AppState, args: list[str]) -> None:
    if not args:
        raise ValueError("Использование: filter add/list/remove/clear")

    action = args[0]

    if action == "add":
        if len(args) != 4:
            raise ValueError("Использование: filter add <поле> <оператор> <значение>")

        condition = filters.parse_filter(args[1], args[2], args[3])
        state["filters"].append(condition)

        number = len(state["filters"])
        print(f"Добавлен фильтр {number}: {output.format_filter(condition)}")

    elif action == "list":
        if len(args) != 1:
            raise ValueError("Использование: filter list")
        print(output.format_filters(state["filters"]))

    elif action == "remove":
        if len(args) != 2:
            raise ValueError("Использование: filter remove <номер>")

        number = int(args[1])

        if number < 1 or number > len(state["filters"]):
            raise ValueError("Фильтра с таким номером нет")

        del state["filters"][number - 1]
        print("Фильтр удалён")

    elif action == "clear":
        if len(args) != 1:
            raise ValueError("Использование: filter clear")
        state["filters"].clear()
        print("Фильтры удалены")

    else:
        raise ValueError(f"Неизвестная подкоманда filter: {action}")


def handle_threshold(state: AppState, value: str) -> None:
    threshold = float(value)

    if not 0 < threshold <= 1:
        raise ValueError("Порог должен быть больше 0 и не больше 1")

    state["threshold"] = threshold
    print(f"Порог: {threshold:g}")


def handle_search(state: AppState, query: str) -> None:
    results, found_count, elapsed_ms = search.search_records(
        state["records"],
        query,
        state["filters"],
        state["threshold"],
        state["ratings"],
    )

    text = output.format_search_results(results, found_count, elapsed_ms)
    print(text)

    state["last_output"] = text
    state["last_ids"] = {record["id"] for record, relevance, rating in results}


def handle_save(state: AppState, path: str) -> None:
    if state["last_output"] is None:
        raise ValueError("Сначала выполните show или search")

    storage.save_result(path, state["last_output"])
    print(f"Сохранено: {path}")


def handle_rate(state: AppState, record_id: str, value: str) -> None:
    rating = int(value)

    if not 1 <= rating <= 5:
        raise ValueError("Оценка должна быть целым числом от 1 до 5")

    if record_id not in state["last_ids"]:
        raise ValueError("Оценивать можно только запись из последней выдачи")

    state["ratings"][record_id] = rating
    print(f"Оценка: {record_id} - {rating}/5")


def handle_ratings(state: AppState) -> None:
    print(output.format_ratings(state["ratings"]))
