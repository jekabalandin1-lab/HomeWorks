class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        print("sound🎵👂🏿")

class Cat(Animal):

    def __init__(self, name):
        super().__init__(name)

    def make_sound(self):
        super().make_sound()
        print(f"{self.name} meow")
class Dog(Animal):

    def __init__(self, name):
        super().__init__(name)

    def make_sound(self):
        super().make_sound()
        print(f"{self.name} raw")



cat = Cat("British Cat")
cat.make_sound()

dog = Dog("Germany Dog")
dog.make_sound()