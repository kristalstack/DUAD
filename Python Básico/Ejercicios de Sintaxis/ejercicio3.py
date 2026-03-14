import random

secret_number = random.randint(1, 10)

print("Guess the secret number between 1 and 10!")

while True:
    user_guess = int(input("Enter your guess: "))

    if user_guess == secret_number:
        print("🎉 Congratulations! You guessed the number!")
        break
    elif user_guess < secret_number:
        print("Too low! Try again.")
    else:
        print("Too high! Try again.")