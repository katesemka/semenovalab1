from commands import handle_command
from models import new_state


def main() -> None:
    print("Поиск по каталогу. Команды: help. Выход: exit.")
    state = new_state()

    while True:
        try:
            line = input("search> ")
            if not handle_command(line, state):
                break
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except ValueError as error:
            print(f"Ошибка: {error}")
        except OSError as error:
            if error.filename is not None:
                print(f"Ошибка: не удалось открыть файл {error.filename}")
            else:
                print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
