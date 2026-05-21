print("--- Програма для конвертації введення у ціле число (розширена) ---")

while True:
    try:
        user_input = input("\nВведіть ціле число (або 'вихід' для завершення): ").strip()

        if user_input.lower() in ['вихід', 'exit', 'quit']:
            print("Завершення роботи програми. До побачення!")
            break

        number = int(user_input)
        print(f"🎉 Успішно! Ви ввели число: {number}")
        break

    except ValueError:
        print("❌ Помилка: Введені дані не є цілим числом.")
        print("Спробуйте ще раз! (Наприклад: 42, -10, 0)")

    except KeyboardInterrupt:
        print("\n\nПрограму примусово закрили через Ctrl+C. Па-па!")
        break