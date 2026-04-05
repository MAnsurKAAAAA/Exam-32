import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox


class Pizza:
    def __init__(self, name, dough, sauce, topping, price):
        self.name = name
        self.dough = dough
        self.sauce = sauce
        self.topping = topping
        self.price = price

    def prepare(self):
        return f"{self.name}: тесто({self.dough}), соус({self.sauce}), начинка({self.topping})"

    def bake(self):
        return f"{self.name}: печется"

    def cut(self):
        return f"{self.name}: измельчены"

    def pack(self):
        return f"{self.name}: упакована"


class PepperoniPizza(Pizza):
    def __init__(self):
        super().__init__("Пепперони", "тонкое", "томатный", "пепперони", 12)


class BBQPizza(Pizza):
    def __init__(self):
        super().__init__("Грибная", "пышное", "грибной", "грибы", 9)


class Mushroom(Pizza):
    def __init__(self):
        super().__init__("Моцарелла", "тонкое", "сливочный", "сыр моцарелла", 7)


class CrashPizza(Pizza):
    def __init__(self):
        super().__init__("Взрывная пицца", "???", "Молотый Порох", "Присыпка из Тротила",1000)

    def prepare(self):
        raise Exception("Все взорвалось!")


class Order:
    def __init__(self):
        self.pizzas = []

    def add_pizza(self, pizza):
        self.pizzas.append(pizza)

    def total_price(self):
        return sum(p.price for p in self.pizzas)

    def summary(self):
        if not self.pizzas:
            return "Заказ пуст"
        text = "Заказ:\n"
        for p in self.pizzas:
            text += f"- {p.name} ({p.price} $)\n"
        text += f"\nИтого: {self.total_price()} $"
        return text


class Terminal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пиццерия")
        self.setGeometry(300, 300, 400, 400)

        self.order = Order()
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Выберите пиццу:"))

        self.menu = QListWidget()
        self.menu.addItems([
            "1. Пепперони - 12$",
            "2. Грибная - 9$",
            "3. Моцарелла - 7$",
            "4. Взрывная Пицца - 1000$ "
        ])
        self.layout.addWidget(self.menu)

        btn_add = QPushButton("Добавить")
        btn_add.clicked.connect(self.add_pizza)
        self.layout.addWidget(btn_add)

        btn_ok = QPushButton("Подтвердить")
        btn_ok.clicked.connect(self.confirm)
        self.layout.addWidget(btn_ok)

        btn_cancel = QPushButton("Отмена")
        btn_cancel.clicked.connect(self.cancel)
        self.layout.addWidget(btn_cancel)

        self.setLayout(self.layout)

    def add_pizza(self):
        i = self.menu.currentRow()
        if i == 0:
            p = PepperoniPizza()
        elif i == 1:
            p = BBQPizza()
        elif i == 2:
            p = Mushroom()
        elif i == 3:
            p = CrashPizza()
        else:
            QMessageBox.warning(self, "Ошибка", "Ты что наделал!")
            return

        self.order.add_pizza(p)
        QMessageBox.information(self, "Ок", f"{p.name} добавлена")

    def confirm(self):
        if not self.order.pizzas:
            QMessageBox.warning(self, "Ошибка", "Пусто")
            return

        if QMessageBox.question(self, "Заказ", self.order.summary() + "\nОплатить?") \
                == QMessageBox.StandardButton.Yes:
            self.process()

    def process(self):
        text = ""
        try:
            for p in self.order.pizzas:
                text += p.prepare() + "\n"
                text += p.bake() + "\n"
                text += p.cut() + "\n"
                text += p.pack() + "\n\n"

            QMessageBox.information(self, "Готово", text)
            self.order = Order()

        except Exception as e:
            QMessageBox.critical(self, "КРАШ", str(e))
            sys.exit()  # закрывает приложение

    def cancel(self):
        self.order = Order()
        QMessageBox.information(self, "Отмена", "Сброшено")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Terminal()
    w.show()
    sys.exit(app.exec())