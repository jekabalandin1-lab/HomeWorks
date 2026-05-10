import random

class Cat:
    def __init__(self, name):
        self.name, self.hunger, self.energy = name, 50, 50
    def live(self):
        self.hunger += 5; self.energy -= 5 # Витрати за день

class Student:
    def __init__(self, name):
        self.name, self.money, self.progress = name, 100, 0
    def live(self):
        if self.money < 30: self.money += 50
        elif self.progress < 20: self.progress += 1
        else: self.money -= 20

cat, st = Cat("Мурчик"), Student("Денис")

for day in range(1, 366):
    cat.live()
    st.live()

    print(f"День {day}: Кіт(Г:{cat.hunger}/Е:{cat.energy}) | Студент(Гр:{st.money}/Пр:{st.progress})")

print("\n" + "="*30)
print(f"ПІДСУМОК ЗА РІК:")
print(f"Кіт {cat.name}: Голод {cat.hunger}, Енергія {cat.energy}")
print(f"Студент {st.name}: Гроші {st.money}, Прогрес {st.progress}")
print("="*30)