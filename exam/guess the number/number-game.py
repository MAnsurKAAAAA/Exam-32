import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox


class GuessGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("угадай число")
        self.setGeometry(400, 300, 300, 200)

        self.layout = QVBoxLayout()

        self.label = QLabel("угадай число от 1 до 100")
        self.layout.addWidget(self.label)

        self.input = QLineEdit()
        self.input.setPlaceholderText("введи число")
        self.layout.addWidget(self.input)

        btn = QPushButton("проверить")
        btn.clicked.connect(self.check)
        self.layout.addWidget(btn)

        self.result = QLabel("")
        self.layout.addWidget(self.result)

        self.reset_btn = QPushButton("снова")
        self.reset_btn.clicked.connect(self.reset)
        self.layout.addWidget(self.reset_btn)

        self.setLayout(self.layout)

        self.reset()

    def reset(self):
        self.number = random.randint(1, 100)
        self.result.setText("")
        self.input.clear()

    def check(self):
        text = self.input.text().strip()

        # обработка ошибок
        if not text:
            QMessageBox.warning(self, "Ошибка", "ЧИСЛО!")
            return

        if not text.isdigit():
            QMessageBox.warning(self, "Ошибка", "ЧИСЛО!")
            return

        guess = int(text)

        if guess < 1 or guess > 100:
            QMessageBox.warning(self, "1-100")
            return

        # логика игры
        if guess < self.number:
            self.result.setText("больше")
        elif guess > self.number:
            self.result.setText("меньше")
        else:
            QMessageBox.information(self, "Victory")
            self.reset()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GuessGame()
    window.show()
    sys.exit(app.exec())