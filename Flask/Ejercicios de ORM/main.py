from address_manager import AddressManager
from car_manager import CarManager
from create_tables import create_missing_tables
from user_manager import UserManager


def main():
    # Verifica que las tablas existan antes de ejecutar operaciones CRUD.
    create_missing_tables()

    user_manager = UserManager()
    car_manager = CarManager()
    address_manager = AddressManager()

    # Crear un usuario
    user = user_manager.create_user(
        "Juan Pérez",
        "juan@email.com"
    )

    # Si el correo ya existe, buscamos al usuario existente
    # para poder continuar con la demostración.
    if user is None:
        users = user_manager.get_all_users()

        user = next(
            (
                current_user
                for current_user in users
                if current_user.email == "juan@email.com"
            ),
            None
        )

    if user is None:
        print("No fue posible obtener un usuario para continuar.")
        return

    # Crear un automóvil sin usuario asociado
    car = car_manager.create_car(
        "Toyota",
        "Corolla",
        2023
    )

    if car is None:
        print("No fue posible crear el automóvil.")
        return

    # Crear una dirección asociada obligatoriamente al usuario
    address_manager.create_address(
        "Calle Principal 123",
        "San José",
        "Costa Rica",
        user.id
    )

    # Asociar el automóvil al usuario
    car_manager.assign_car_to_user(
        car.id,
        user.id
    )

    # Consultar todos los usuarios
    print("\n===== USUARIOS =====")

    for current_user in user_manager.get_all_users():
        print(current_user)

    # Consultar todos los automóviles
    print("\n===== AUTOMÓVILES =====")

    for current_car in car_manager.get_all_cars():
        print(current_car)

    # Consultar todas las direcciones
    print("\n===== DIRECCIONES =====")

    for current_address in address_manager.get_all_addresses():
        print(current_address)


if __name__ == "__main__":
    main()