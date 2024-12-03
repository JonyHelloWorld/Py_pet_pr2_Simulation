class Person:
    pass # pass используем когда в классе нет кода
tom = Person()  # создаем объект класса Person

class Person2:
    # конструктор создания объекта, имя всегда __init__
    # Обычно конструкторы применяются для определения действий, которые должны производиться при создании объекта
    def __init__(self, name, age, surname):
        # self для установки атрибутов внутри класса
        self.name = name  # имя человека
        self.age = age  # возраст человека
        self.__surname = surname  # приватный атрибут начинается с __
        # но к нему всё равно можно будет обратиться из вне указав полное имя
        # self._Person2__surname = ...

    # метод класса
    def display_info(self):
        print(f"Name: {self.name}  Age: {self.age}")

    # первый параметр метода представляет ссылку на текущий объект,
    # и называется self
    def say_hello(self, message):
        print(message)
# вызов метода
tom.say_hello("hello world")    # Hello
tom = Person("Tom", 22)
# обращение к атрибутам
# получение значений
print(tom.name)  # Tom
print(tom.age)  # 22
# изменение значения
tom.age = 37
print(tom.age)  # 37

# для обращения к приватным атрибутам используем спец.методы
# которые называются геттеры и сеттеры. Геттер позволяет получить значение атрибута, а сеттер установить его.
class Person3:
    def __init__(self, name, age):
        self.__name = name  # устанавливаем имя
        self.__age = age  # устанавливаем возраст

    # сеттер для установки возраста
    def set_age(self, age):
        if 0 < age < 110:
            self.__age = age
        else:
            print("Недопустимый возраст")

    # геттер для получения возраста
    def get_age(self):
        return self.__age

    # геттер для получения имени
    def get_name(self):
        return self.__name

    def print_person(self):
        print(f"Имя: {self.__name}\tВозраст: {self.__age}")


tom = Person("Tom", 39)
tom.print_person()  # Имя: Tom  Возраст: 39
tom.set_age(-3486)  # Недопустимый возраст
tom.set_age(25)
tom.print_person()  # Имя: Tom  Возраст: 25


class Person:
    def __init__(self, name, age):
        self.__name = name  # устанавливаем имя
        self.__age = age  # устанавливаем возраст

    # свойство-геттер
    @property
    def age(self):
        return self.__age

    # свойство-сеттер
    @age.setter
    def age(self, age):
        if 0 < age < 110:
            self.__age = age
        else:
            print("Недопустимый возраст")

    @property
    def name(self):
        return self.__name

    def print_person(self):
        print(f"Имя: {self.__name}\tВозраст: {self.__age}")


tom = Person("Tom", 39)
tom.print_person()  # Имя: Tom  Возраст: 39
tom.age = -3486  # Недопустимый возраст  (Обращение к сеттеру)
print(tom.age)  # 39 (Обращение к геттеру)
tom.age = 25  # (Обращение к сеттеру)
tom.print_person()  # Имя: Tom  Возраст: 25

# проверка на принадлежность к классу и вызов соответствующего метода
def act(person):
    if isinstance(person, Student):
        person.study()
    elif isinstance(person, Employee):
        person.work()
    elif isinstance(person, Person):
        person.do_nothing()


# @staticmethod статические методы - результат их работы будет одинаков для всех объектов класса
class Person:
    __type = "Person"

    @staticmethod
    def print_type():
        print(Person.__type)

Person.print_type()  # Person - обращение к статическому методу через имя класса
tom = Person()
tom.print_type()  # Person - обращение к статическому методу через имя объекта

# для описания несуществующих сущностей (животное или геомет фигура) применяются абстрактные классы
# В языке Python все инструменты для создания абстрактных классов определены в специальном модуле abc

import abc
class Shape(abc.ABC): # абстрактный класс - геомет фигуры
    @abc.abstractmethod
    def area (self): pass # абстрактный метод вычисления площади
    # кода в нем нет тк у классов наследников будет у каждого свой формула вычисления площади
    # Классы-наследники должны реализовать все абстрактные методы абстрактного класса


# класс прямоугольника
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self): return self.width * self.height

# класс круга
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self): return self.radius * self.radius * 3.14

def print_area(shape):
    print("Area:", shape.area())

rect = Rectangle(30, 50)
circle = Circle(30)
print_area(rect)  # Area: 1500
print_area(circle)  # Area: 2826.0


