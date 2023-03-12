class MyCalculator:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def add_numbers(self):
        return self.num1 + self.num2

    def subtract_numbers(self):
        return self.num1 - self.num2

if __name__ == "__main__":
    calculator = MyCalculator(5, 3)
    print(calculator.add_numbers())
    print(calculator.subtract_numbers())
