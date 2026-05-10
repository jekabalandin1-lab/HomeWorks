class Product:
    def __init__(self, name, price):
        self.name, self.price = name, price

class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)
        print(f"Додано: {product.name}")

    def total(self):
        return sum(p.price for p in self.items)

    def show(self):
        print("Кошик:", [p.name for p in self.items])
        print(f"Разом: {self.total()} грн")

p1 = Product("Хліб", 20)
p2 = Product("Молоко", 35)

my_cart = Cart()
my_cart.add(p1)
my_cart.add(p2)
my_cart.show()