class Flyable:
    def fly(self):
        return "Flying in the sky"


class Swimmable:
    def swim(self):
        return "Swimming in the water"


class Duck(Flyable, Swimmable):
    def quack(self):
        return "Quack!"


# Example usage
duck = Duck()
print(duck.fly())     # Flying in the sky
print(duck.swim())    # Swimming in the water
print(duck.quack())   # Quack!