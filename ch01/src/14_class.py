class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name}({self.age}살) 강아지가 멍멍!"
    
my_dog = Dog("뽀삐", 3)
print(my_dog.bark())