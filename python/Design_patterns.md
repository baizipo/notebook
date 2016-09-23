# 创建型模式

创建型设计模式处理对象创建相关的问题，目标是当直接创建对象不太方便时，提供更好的方式

## 工厂模式

工厂模式主要是为创建对象提供过渡接口，以便将创建对象的具体过程屏蔽隔离起来，达到提高灵活性的目的。与客户端自己基于类实例化直接创建对象相比，基于一个中心化函数来实现，更易于追踪创建了哪些对象。通过将创建对象的代码和使用对象的代码解耦工厂能够降低应用维护的复杂度。

```python
class GreekGetter:
    def __init__(self):
        self.trans = dict(dog="σκύλος", cat="γάτα")

    def get(self, msgid):
        try:
            return self.trans[msgid]
        except KeyError:
            retrun str(msgid)

class EnglishGetter:
    def get(self, msgid):
        return str(msgid)

def get_localizer(language='Englist'):
    languages = dict(English=EnglishGetter, Greek=GreekGetter)
    return languages[language]()

e, g = get_localizer("English"), get_localizer("Greek")

for msgid in "dog parrot cat bear".split():
    print e.get(msgid), g.get(msgid)
```

```python
import xml.etree.ElementTree as etree
import json

class JSONConnector:
    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, mode='r', encoding='utf-8') as f:
            self.data = json.load(f)

    @property
    def parsed_data(self):
        return self.data

class XMLConnector:
    def __init__(self, filepath):
        self.tree = etree.parse(filepath)

    @property
    def parsed_data(self):
        return self.tree

def connection_factory(filepath):
    if filepath.endswith('json'):
        connector = JSONConnector
    elif filepath.endswith('xml'):
        connector = XMLConnector
    else:
        raise ValueError('Cannot connect to {}'.format(filepath))
    return  connector

def connect_to(filepath):
    factory = None
    try:
        factory = connection_factory(filename)
    except ValueError as ve:
        print ve
    return factory

sqlite_factory = connect_to('/tmp/123.sq3')

json_factory = connect_to('/tmp/asdf.json')
json_data = json_factory.parsed_data
#### 接下来数据处理
```

## 抽象工厂

一个抽象工厂是（逻辑上的）一组工厂方法，其中的每个工厂方法负责产生不同种类的对象。因为抽象工厂模式是工厂方法模式的一种泛化，所以它能提供相同的好处：让对象的创建更容易追踪；将对象创建与使用解耦；提供优化内存占用和应用性能的潜力。

```python
# 脚本包含两个游戏,一个面向孩子,一个面向成人。在运行时,基于用户输入,决定该创建哪个游戏并运行。游戏的创建部分由一个抽象工厂维护。

class Frog:

    # 定义青蛙的名称
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    # 描述青蛙与障碍物之间的交互
    def interact_with(self, obstacle):
        print '{} the Frog encounters {} and {}!'.format(self,
                                                         obstacle,
                                                         obstacle.action())

# 障碍物可以有多种,但对于我们的列子,可以仅仅是虫子,当青蛙遇到一只虫子,只支持一种动作,那就是吃掉它。
class Bug:
    def __str__(self):
        return 'a bug'

    def action(self):
        return 'eats it'

#类FrogWorld是一个抽象工厂,主要职责是创建有限的主人公和障碍物。区分创建方法并使其名字通用(比如,make_character()和make_obstacle()),这让我们可以动态改变当前激活的工厂,而无需进行任何代码变更。
class FrogWorld:
    def __init__(self, name):
        print self
        self.player_name = name

    def __str__(self):
        return '\n\n\t---Frog World---'

    def make_character(self):
        return Frog(self.player_name)

    def make_obstacle(self):
        return Bug()

# WizardWorld游戏也类似。在故事中唯一的区别是男巫战怪兽而不是吃虫子。
class Wizard:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def interact_with(self, obstacle):
        print '{} the wizard battles against {} and {}!'.format(self,
                                                                obstacle,
                                                                obstacle.action())

class Ork:
    def __str__(self):
        return 'an evil ork'

    def action(self):
        return 'kills it'

class WizardWorld:
    def __init__(self, name):
        print self
        self.player_name = name

    def __str__(self):
        return '\n\n\t---Wizard World---'

    def make_character(self):
        return Wizard(self.player_name)

    def make_obstacle(self):
        return Ork()

# 类GameEnvironment是游戏的主入口。它接受factory作为输入,用其创建游戏的世界。方法play()则会启动hero和obstacle之间的交互
class GameEnvironment:
    def __init__(self, factory):
        self.hero = factory.make_character()
        self.obstacle = factory.make_obstacle()

    def play(self):
        self.hero.interact_with(self.obstacle)

# 提示用户提供一个有效的年龄。如果年龄无效,则会返回一个元祖,其第一个元素设置为False。如果年龄没问题,元素的第一个元素则设置为True。但我们真正关心的是第二个元素,也就是用户提供的年龄
def validate_age(name):
    try:
        age = input('welcom {}. How old are you?'.format(name))
        age = int(age)
    except ValueError as err:
        print "Age {} is invalid, please try again...".format(age)
        return False, age
    return True, age

# 最后一个要点是main()函数,该函数请求用户的姓名和年龄,并根据用户的年龄决定该玩哪个游戏
def main():
    name = raw_input("Hello, What's your name?")
    valid_input = False
    while not valid_input:
        valid_input, age = validate_age(name)
    game = FrogWorld if age < 18 else WizardWorld
    environment = GameEnvironment(game(name))
    environment.play()

if __name__ == '__main__':
    main()
```

```python
import random


class PetShop:
    """A pet shop"""

    def __init__(self, animal_factory=None):
        """pet_factory is our abstract factory.
        We can set it at will."""

        self.pet_factory = animal_factory

    def show_pet(self):
        """Creates and shows a pet using the
        abstract factory"""

        pet = self.pet_factory.get_pet()
        print("This is a lovely", pet)
        print("It says", pet.speak())
        print("It eats", self.pet_factory.get_food())


# Stuff that our factory makes

class Dog:
    def speak(self):
        return "woof"

    def __str__(self):
        return "Dog"


class Cat:
    def speak(self):
        return "meow"

    def __str__(self):
        return "Cat"


# Factory classes

class DogFactory:
    def get_pet(self):
        return Dog()

    def get_food(self):
        return "dog food"


class CatFactory:
    def get_pet(self):
        return Cat()

    def get_food(self):
        return "cat food"


# Create the proper family
def get_factory():
    """Let's be dynamic!"""
    return random.choice([DogFactory, CatFactory])()


# Show pets with various factories
if __name__ == "__main__":
    shop = PetShop()
    for i in range(3):
        shop.pet_factory = get_factory()
        shop.show_pet()
        print("=" * 20)
```


## 建造者模式

我们想要创建一个由多个部分构成的对象，而且它的构成需要一步接一步地完成。只有当各个部分都创建好，这个对象才算是完整的。这正是建造者设计模式的用武之地。建造者模式将一个复杂对象的构造过程与其表现分离，这样，同一个构造过程可用于多个不同的表现。该模式中，有两个参与者：建造者（builder）和指挥者（director）。建造者负责创建复杂对象的各个组成部分。指挥者使用一个建造者实例控制建造的过程。

> ##### 建造者与工厂模式的差别:
> ###### 1. 工厂模式以单个步骤创建对象，而建造者模式以多个步骤创建对象，并且几乎始终会使用一个指挥者。
> ###### 2. 在工厂模式下，会立即返回一个创建好的对象；而在建造者模式下，仅在需要时客户端代码才显式地请求指挥者返回最终的对象。

```python
class Computer:
    def __init__(self, serial_number):
        self.serial = serial_number
        self.memory = None
        self.hdd = None
        self.gpu = None

    def __str__(self):
        info = ('Memory: {}GB'.format(self.memory),
               'Hard Disk: {}GB'.format(self.hdd),
               'Graphics Card: {}'.format(self.gpu))
        return '\n'.join(info)

class ComputerBuilder:
    def __init__(self):
        self.computer = Computer('AG23385193')

    def configure_memory(self, amount):
        self.computer.memory = amount

    def configure_hdd(self, amount):
        self.computer.hdd = amount

    def configure_gpu(self, gpu_model):
        self.computer.gpu = gpu_model


class HardwareEngineer:
    def __init__(self):
        self.builder = None

    def construct_computer(self, memory, hdd, gpu):
        self.builder = ComputerBuilder()
        self.builder.configure_memory(memory)
        self.builder.configure_hdd(hdd)
        self.builder.configure_gpu(gpu)

    @property
    def computer(self):
        return self.builder.computer

def main():
    engineer = HardwareEngineer()
    engineer.construct_computer(hdd=500, memory=8, gpu='GeForce GTX 650 Ti')
    computer = engineer.computer
    print computer
if __name__ == '__main__':
    main()
```

```python
#!/usr/bin/python
# -*- coding : utf-8 -*-

"""
    @author: Diogenes Augusto Fernandes Herminio <diofeher@gmail.com>
    https://gist.github.com/420905#file_builder_python.py
"""


# Director
class Director(object):
    def __init__(self):
        self.builder = None

    def construct_building(self):
        self.builder.new_building()
        self.builder.build_floor()
        self.builder.build_size()

    def get_building(self):
        return self.builder.building


# Abstract Builder
class Builder(object):
    def __init__(self):
        self.building = None

    def new_building(self):
        self.building = Building()


# Concrete Builder
class BuilderHouse(Builder):
    def build_floor(self):
        self.building.floor = 'One'

    def build_size(self):
        self.building.size = 'Big'


class BuilderFlat(Builder):
    def build_floor(self):
        self.building.floor = 'More than One'

    def build_size(self):
        self.building.size = 'Small'


# Product
class Building(object):
    def __init__(self):
        self.floor = None
        self.size = None

    def __repr__(self):
        return 'Floor: %s | Size: %s' % (self.floor, self.size)


# Client
if __name__ == "__main__":
    director = Director()
    director.builder = BuilderHouse()
    director.construct_building()
    building = director.get_building()
    print(building)
    director.builder = BuilderFlat()
    director.construct_building()
    building = director.get_building()
    print(building)
```

## 原型模式

原型设计模式(Prototype design pattern)帮助我们创建对象的克隆，其最简单的形式就是一个clone()函数，接受一个对象作为输入参数，返回输入对象的副本。

Python中的对象之间赋值时是按引用传递的，如果需要拷贝对象，需要使用标准库中的copy模块。

1. copy.copy 浅拷贝 只拷贝父对象，不会拷贝对象的内部的子对象。 
2. copy.deepcopy 深拷贝 拷贝对象及其子对象 

```python
import copy

class Prototype:
    def __init__(self):
        self._objects = {}

    def register_object(self, name, obj):
        """Register an object"""
        self._objects[name] = obj

    def unregister_object(self, name):
        """Unregister an object"""
        del self._objects[name]

    def clone(self, name, **attr):
        """Clone a registered object and update inner attributes dictionary"""
        obj = copy.deepcopy(self._objects.get(name))
        obj.__dict__.update(attr)
        return obj

def main():
    class A:
        pass

    a = A()
    prototype = Prototype()
    prototype.register_object('a', a)
    b = prototype.clone('a', a=1, b=2, c=3)

    print(a)
    print(b.a, b.b, b.c)
    print('ID a : {} != ID b : {}'.format(id(a), id(b)))

if __name__ == '__main__':
    main()
```

# 结构型设计模式
结构型设计模式处理一个系统中不同实体(比如，类和对象)之间的关系，关注的是提供一种简单的对象组合方式来创造新功能。

## 适配器模式
设配器模式(Adapter pattern)是一种结构型设计模式，帮助我们实现两个不兼容接口之间的兼容。我们可以编写一个额外的代码层，该代码层包含让两个接口之间能够通信需要进行的所有修改，这个代码层就交适配器。适配器模式遵从开放/封闭原则。(开放/封闭原则是面向对象设计的基本原则之一，声明一个软件实体应该对扩展是开放的，对修改是封闭的)

```python
class Synthesizer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} synthesizer'.format(self.name)

    def play(self):
        return 'is playing an eletrronic song'


class Human:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '{} the human'.format(self.name)

    def speak(self):
        return 'says hello'


class Computer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} computer'.format(self.name)

    def execute(self):
        return 'executes a program'


class Adapter:
    def __init__(self, obj, adapted_methods):
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __str__(self):
        return str(self.obj)


def main():
    objects = [ Computer('Asus')]
    synth = Synthesizer('moog')
    objects.append(Adapter(synth, dict(execute=synth.play)))
    human = Human('Bob')
    objects.append(Adapter(human, dict(execute=human.speak)))

    for i in objects:
        print '{}, {}'.format(str(i), i.execute())

if __name__ == '__main__':
    main()
```

```python
# http://ginstrom.com/scribbles/2008/11/06/generic-adapter-class-in-python/

import os


class Dog(object):
    def __init__(self):
        self.name = "Dog"

    def bark(self):
        return "woof!"


class Cat(object):
    def __init__(self):
        self.name = "Cat"

    def meow(self):
        return "meow!"


class Human(object):
    def __init__(self):
        self.name = "Human"

    def speak(self):
        return "'hello'"


class Car(object):
    def __init__(self):
        self.name = "Car"

    def make_noise(self, octane_level):
        return "vroom%s" % ("!" * octane_level)


class Adapter(object):
    """
    Adapts an object by replacing methods.
    Usage:
    dog = Dog
    dog = Adapter(dog, dict(make_noise=dog.bark))
    """
    def __init__(self, obj, adapted_methods):
        """We set the adapted methods in the object's dict"""
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __getattr__(self, attr):
        """All non-adapted calls are passed to the object"""
        return getattr(self.obj, attr)


def main():
    objects = []
    dog = Dog()
    objects.append(Adapter(dog, dict(make_noise=dog.bark)))
    cat = Cat()
    objects.append(Adapter(cat, dict(make_noise=cat.meow)))
    human = Human()
    objects.append(Adapter(human, dict(make_noise=human.speak)))
    car = Car()
    car_noise = lambda: car.make_noise(3)
    objects.append(Adapter(car, dict(make_noise=car_noise)))

    for obj in objects:
        print("A", obj.name, "goes", obj.make_noise())


if __name__ == "__main__":
    main()
```

