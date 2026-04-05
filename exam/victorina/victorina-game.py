import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import QTimer


class Quiz(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Викторина")
        self.setGeometry(400, 300, 350, 250)

        # загрузка JSON
        try:
            with open("questions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            self.questions = data["questions"]
        except Exception:
            QMessageBox.critical(self, "Ошибка", "Проблема с questions.json")
            sys.exit()

        self.index = 0
        self.time_left = 10

        self.layout = QVBoxLayout()

        self.timer_label = QLabel()
        self.layout.addWidget(self.timer_label)

        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.input = QLineEdit()
        self.layout.addWidget(self.input)

        btn = QPushButton("Ответить")
        btn.clicked.connect(self.check)
        self.layout.addWidget(btn)

        self.setLayout(self.layout)

        # время
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.start_question()

    def start_question(self):
        if self.index >= len(self.questions):
            QMessageBox.information(self, "Конец", "Вопросы закончились")
            self.index = 0

        self.time_left = 10
        self.timer.start(1000)

        self.question_label.setText(self.questions[self.index]["q"])
        self.timer_label.setText(f"Время: {self.time_left}")
        self.input.clear()

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Time\ {self.time_left}")

        if self.time_left == 0:
            self.timer.stop()
            QMessageBox.warning(self, "Время", "Время вышло!")
            self.index += 1
            self.start_question()

    def check(self):
        answer = self.input.text().strip().lower()

        if not answer:
            QMessageBox.warning(self, "ошибка", "введите ответ")
            return

        self.timer.stop()

        correct = self.questions[self.index]["a"]

        if answer == correct:
            QMessageBox.information(self, "верно", "вравильно!")
        else:
            QMessageBox.critical(self, "неверно", f"Ответ: {correct}")

        self.index += 1
        self.start_question()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Quiz()
    window.show()
    sys.exit(app.exec())