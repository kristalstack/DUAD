class Person:
    def __init__(self, name):
        self.name = name


class Bus:
    def __init__(self, max_passengers):
        self.max_passengers = max_passengers
        self.passengers = []

    def add_passenger(self, person):
        if len(self.passengers) < self.max_passengers:
            self.passengers.append(person)
            print(f"{person.name} got on the bus.")
        else:
            print("The bus is full.")

    def remove_passenger(self, person):
        if person in self.passengers:
            self.passengers.remove(person)
            print(f"{person.name} got off the bus.")
        else:
            print("Passenger not found.")


# Example usage
bus = Bus(2)

p1 = Person("Ana")
p2 = Person("Luis")
p3 = Person("Carlos")

bus.add_passenger(p1)
bus.add_passenger(p2)
bus.add_passenger(p3)

bus.remove_passenger(p1)
bus.remove_passenger(p3)