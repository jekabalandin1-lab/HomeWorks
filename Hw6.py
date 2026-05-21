import colorama

all_attributes = dir(colorama)

important_components = {
    "Fore": "Клас, який містить ANSI-коди для зміни кольору тексту (наприклад: Fore.RED, Fore.GREEN).",
    "Back": "Клас, який містить ANSI-коди для зміни кольору тла (наприклад: Back.YELLOW, Back.BLUE).",
    "Style": "Клас для зміни стилю тексту: яскравий (Style.BRIGHT), тьмяний (Style.DIM), скидання (Style.RESET_ALL).",
    "init": "Функція, яка ініціалізує бібліотеку. Вона перехоплює стандартний вивід і переводить ANSI-коди у зрозумілі для Windows команди.",
    "deinit": "Функція, яка скасовує дію init() і повертає стандартну поведінку терміналу.",
    "just_fix_windows_console": "Сучасна альтернатива init(), яка вмикає підтримку ANSI безпосередньо в консолі Windows."
}

print("=== Базова інтроспекція модуля colorama ===")
print(f"Тип об'єкта: {type(colorama)}")
print(f"Назва модуля: {colorama.__name__}")
print(f"Документація: {colorama.__doc__}\n")

print("=== Найважливіші атрибути та методи ===")
for name, description in important_components.items():
    if hasattr(colorama, name):
        obj = getattr(colorama, name)
        print(f"• Атрибут: '{name}' | Тип: {type(obj)}")
        print(f"  Опис: {description}\n")

print("=== Демонстрація роботи ===")
colorama.init(autoreset=True)

print(colorama.Fore.GREEN + "Цей текст зелений завдяки Fore.GREEN")
print(colorama.Back.BLUE + colorama.Fore.WHITE + "Цей текст білий на синьому тлі завдяки Back.BLUE")
print(colorama.Style.BRIGHT + colorama.Fore.RED + "Цей текст яскраво-червоний завдяки Style.BRIGHT")