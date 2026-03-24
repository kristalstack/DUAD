class Head:
    def __init__(self):
        pass


class Hand:
    def __init__(self):
        pass


class Feet:
    def __init__(self):
        pass


class Arm:
    def __init__(self, hand):
        self.hand = hand


class Leg:
    def __init__(self, feet):
        self.feet = feet


class Torso:
    def __init__(self, head, left_arm, right_arm, left_leg, right_leg):
        self.head = head
        self.left_arm = left_arm
        self.right_arm = right_arm
        self.left_leg = left_leg
        self.right_leg = right_leg


class Human:
    def __init__(self):
        head = Head()

        left_hand = Hand()
        right_hand = Hand()

        left_arm = Arm(left_hand)
        right_arm = Arm(right_hand)

        left_feet = Feet()
        right_feet = Feet()

        left_leg = Leg(left_feet)
        right_leg = Leg(right_feet)

        self.torso = Torso(
            head,
            left_arm,
            right_arm,
            left_leg,
            right_leg
        )


# Example usage
human = Human()

print("Human created successfully")