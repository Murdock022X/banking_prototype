from typing import TypeVar
Money = TypeVar('Money')

class Money():
    """
    This is a very simple class simply used to ensure that any amounts of money
    used in our application conform to being a maximum of two decimal places.
    """
    def __init__(self, amt: float):
        """
        Money constructor, rounds value to two decimal places.
        :param amt: The amount of money the object should be initialized with.
        """
        self.amt = round(amt, 2)

    def __add__(self, other: Money) -> Money:
        """
        Add two money objects together and get the money object with the sum
        of the two for it's amount.
        :param other: The money object to add the this money object.
        :return: The new money object.
        """
        return Money(self.amt + other.amt)

    def __sub__(self, other: Money) -> Money:
        """
        Subtract a money object amt from this money object 
        amt and return new_object.
        :param other: The money object to subtract from this money object.
        :return: The new money object.
        """
        return Money(self.amt - other.amt)

    def __mul__(self, ir: float) -> Money:
        """
        Operation designed for use with an interest rate multiplier.
        Multiplies the value of this money object with a floating point number.
        :param ir: The interest rate.
        :return: The new money object.
        """
        return Money(self.amt * ir)

    def __lt__(self, other: Money) -> bool:
        """
        Check if this money object amt is less than other amt.
        :param other: The other money object.
        :return: True if the curr amt is less than other amt, False otherwise.
        """
        if self.amt < other.amt:
            return True
        return False

    def __le__(self, other: Money) -> bool:
        """
        Check if this money object amt is less than or equal to the other amt.
        :param other: The other money object.
        :return: True if the curr amt is less than or equal to the other amt,
        False otherwise.
        """
        if self.amt <= other.amt:
            return True
        return False

    def __gt__(self, other: Money) -> bool:
        """
        Check if this money object amt is greater than other amt.
        :param other: The other money object.
        :return: True if the curr amt is greater than other amt,
        False otherwise.
        """
        if self.amt > other.amt:
            return True
        return False

    def __ge__(self, other: Money) -> bool:
        """
        Check if this money object amt is greater than or 
        equal to the other amt.
        :param other: The other money object.
        :return: True if the curr amt is greater than or equal to other amt,
        False otherwise.
        """
        if self.amt >= other.amt:
            return True
        return False

    def __eq__(self, other: Money) -> bool:
        """
        Check if this money object amt is equal to the other amt.
        :param other: The other money object.
        :return: True if the curr amt is equal to the other amt, 
        False otherwise.
        """
        if self.amt == other.amt:
            return True
        return False