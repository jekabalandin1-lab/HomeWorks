import tkinter as tk
from tkinter import messagebox

class CurrencyConverter:
    def __init__(self):
        self.rate = 44.10

    def to_usd(self, uah):
        return uah / self.rate

def convert():
    try:
        uah = float(entry.get())
        if uah < 0:
            raise ValueError
        usd = converter.to_usd(uah)
        result_label.config(text=f"{usd:.2f} $")
    except ValueError:
        messagebox.showerror("Помилка", "Введіть коректне число")

converter = CurrencyConverter()

root = tk.Tk()
root.title("Converter")
root.geometry("250x180")

tk.Label(root, text="Курс: 1$ = 44.10₴").pack(pady=5)
tk.Label(root, text="Сума в ₴:").pack()

entry = tk.Entry(root, justify="center")
entry.pack(pady=5)

tk.Button(root, text="Конвертувати", command=convert).pack(pady=5)

result_label = tk.Label(root, font=("Arial", 12, "bold"))
result_label.pack(pady=5)

root.mainloop()