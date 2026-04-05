import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox


def check_winner(user, comp):
    if user == comp:
        return "Ничья!"
    elif (user == "камень" and comp == "ножницы") or \
         (user == "ножницы" and comp == "бумага") or \
         (user == "бумага" and comp == "камень"):
        return "ты выиграл!"
    else:
        return "You WON!"


class Game(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("камень ножницы бумага")
        self.setGeometry(400, 300, 300, 250)

        layout = QVBoxLayout()

        self.label = QLabel("Выбери:")
        self.label.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.label)

        btn_rock = QPushButton("Камень")
        btn_rock.clicked.connect(lambda: self.play("камень"))
        layout.addWidget(btn_rock)

        btn_scissors = QPushButton("Ножницы")
        btn_scissors.clicked.connect(lambda: self.play("ножницы"))
        layout.addWidget(btn_scissors)

        btn_paper = QPushButton("Бумага")
        btn_paper.clicked.connect(lambda: self.play("бумага"))
        layout.addWidget(btn_paper)

        self.setLayout(layout)

    def play(self, user):
        options = ["камень", "ножницы", "бумага"]
        comp = random.choice(options)

        result = check_winner(user, comp)

        QMessageBox.information(
            self,
            "результат",
            f"Ты: {user}\nКомпьютер: {comp}\n\n{result}"
        )



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Game()
    window.show()
    sys.exit(app.exec())