from dataclasses import dataclass
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


@dataclass
class Pair(ABC):
    @abstractmethod
    def __add__(self, other) -> "Pair":
        pass

    @abstractmethod
    def __sub__(self, other) -> "Pair":
        pass

    @abstractmethod
    def __mul__(self, other) -> "Pair":
        pass

    @abstractmethod
    def __truediv__(self, other) -> "Pair":
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def to_xml(self, element_name: str) -> str:
        root = ET.Element(element_name)
        for key, value in self.__dict__.items():
            child = ET.Element(key)
            child.text = str(value)
            root.append(child)
        return ET.tostring(root, encoding="utf-8").decode()

    @classmethod
    def from_xml(cls, xml_string: str) -> "Pair":
        root = ET.fromstring(xml_string)
        kwargs = {child.tag: child.text for child in root}
        return cls(**kwargs)


@dataclass
class Money(Pair):
    amount: float

    def __add__(self, other: "Money") -> "Money":
        if isinstance(other, Money):
            return Money(self.amount + other.amount)
        else:
            raise TypeError("Unsupported operand type")

    def __sub__(self, other: "Money") -> "Money":
        if isinstance(other, Money):
            return Money(self.amount - other.amount)
        else:
            raise TypeError("Unsupported operand type")

    def __mul__(self, other: float) -> "Money":
        if isinstance(other, (int, float)):
            return Money(self.amount * other)
        else:
            raise TypeError("Unsupported operand type")

    def __truediv__(self, other: float) -> "Money":
        if isinstance(other, (int, float)):
            return Money(self.amount / other)
        else:
            raise TypeError("Unsupported operand type")

    def __str__(self) -> str:
        return str(self.amount)

    def to_xml(self) -> str:
        return super().to_xml("Money")

    @classmethod
    def from_xml(cls, xml_string: str) -> "Money":
        return super().from_xml(xml_string)


@dataclass
class Fraction(Pair):
    numerator: int
    denominator: int

    def __add__(self, other: "Fraction") -> "Fraction":
        if isinstance(other, Fraction):
            common_denominator = self.denominator * other.denominator
            new_numerator = (self.numerator * other.denominator) + (
                other.numerator * self.denominator
            )
            return Fraction(new_numerator, common_denominator)
        else:
            raise TypeError("Unsupported operand type")

    def __sub__(self, other: "Fraction") -> "Fraction":
        if isinstance(other, Fraction):
            common_denominator = self.denominator * other.denominator
            new_numerator = (self.numerator * other.denominator) - (
                other.numerator * self.denominator
            )
            return Fraction(new_numerator, common_denominator)
        else:
            raise TypeError("Unsupported operand type")

    def __mul__(self, other: float) -> "Fraction":
        if isinstance(other, (int, float)):
            return Fraction(int(self.numerator * other), self.denominator)
        else:
            raise TypeError("Unsupported operand type")

    def __truediv__(self, other: float) -> "Fraction":
        if isinstance(other, (int, float)):
            return Fraction(self.numerator, int(self.denominator * other))
        else:
            raise TypeError("Unsupported operand type")

    def __str__(self) -> str:
        return f"{self.numerator}/{self.denominator}"

    def to_xml(self) -> str:
        return super().to_xml("Fraction")

    @classmethod
    def from_xml(cls, xml_string: str) -> "Fraction":
        return super().from_xml(xml_string)


if __name__ == "__main__":
    money1 = Money(100)
    money2 = Money(50)
    print(money1 + money2)
    print(money1 - money2)
    print(money1 * 2)
    print(money1 / 2)

    # Сериализация и десериализация для Money
    money_xml = money1.to_xml()
    money_from_xml = Money.from_xml(money_xml)
    print(f"Deserialized Money: {money_from_xml}")

    # Сохранение XML в файл
    with open("money.xml", "w") as money_file:
        money_file.write(money_xml)

    fraction1 = Fraction(1, 2)
    fraction2 = Fraction(3, 4)
    print(fraction1 + fraction2)
    print(fraction1 - fraction2)
    print(fraction1 * 2)
    print(fraction1 / 2)

    # Сериализация и десериализация для Fraction
    fraction_xml = fraction1.to_xml()
    fraction_from_xml = Fraction.from_xml(fraction_xml)
    print(f"Deserialized Fraction: {fraction_from_xml}")

    # Сохранение XML в файл
    with open("fraction.xml", "w") as fraction_file:
        fraction_file.write(fraction_xml)
