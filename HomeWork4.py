
class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Driver(Human):

    def __init__(self, name, age, driving_license):
        super().__init__(name, age)
        self.driving_license = driving_license

name = input("name:")
age = input("age:")
driving_license = input("driving license:")

driver = Driver(name, age, driving_license)



