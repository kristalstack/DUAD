from user_manager import UserManager
from car_manager import CarManager
from address_manager import AddressManager


user_manager = UserManager()
car_manager = CarManager()
address_manager = AddressManager()

# Crear usuario
user = user_manager.create_user(
    "Juan Pérez",
    "juan@email.com"
)

# Crear automóvil
car = car_manager.create_car(
    "Toyota",
    "Corolla",
    2023
)

# Crear dirección
address = address_manager.create_address(
    "Calle Principal 123",
    "San José",
    "Costa Rica",
    user.id
)

# Asociar automóvil al usuario
car_manager.assign_car_to_user(
    car.id,
    user.id
)

print("\n===== USUARIOS =====")
for user in user_manager.get_all_users():
    print(user)

print("\n===== AUTOMÓVILES =====")
for car in car_manager.get_all_cars():
    print(car)

print("\n===== DIRECCIONES =====")
for address in address_manager.get_all_addresses():
    print(address)