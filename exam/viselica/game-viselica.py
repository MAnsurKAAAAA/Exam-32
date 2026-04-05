import sys
import json
import random
import os
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox


class Hangman(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Виселица")
        self.setGeometry(400, 300, 300, 250)
        self.sound = QSoundEffect()

        sound_path = os.path.join(os.path.dirname(__file__), "undertale-soul-shatter.wav")
        self.sound.setSource(QUrl.fromLocalFile(sound_path))
        self.sound.setVolume(0.5)

        self.win_sound = QSoundEffect()

        win_sound_path = os.path.join(os.path.dirname(__file__), "undertale-sound-effect-you-win.wav")
        self.win_sound.setSource(QUrl.fromLocalFile(win_sound_path))
        self.win_sound.setVolume(0.5)

        try:
            with open("words.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            if "words" not in data or not isinstance(data["words"], list):
                raise ValueError("Неверный формат JSON")

            self.words = data["words"]

        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл words.json не найден")
            sys.exit()

        except json.JSONDecodeError:
            QMessageBox.critical(self, "Ошибка", "Ошибка чтения JSON")
            sys.exit()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            sys.exit()

        self.layout = QVBoxLayout()

        self.start_game()

        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.hearts_label = QLabel()
        self.layout.addWidget(self.hearts_label)

        self.input = QLineEdit()
        self.input.setPlaceholderText("введите букву")
        self.layout.addWidget(self.input)

        btn = QPushButton("check")
        btn.clicked.connect(self.check)
        self.layout.addWidget(btn)

        self.info = QLabel()
        self.layout.addWidget(self.info)

        self.setLayout(self.layout)
        self.update_ui()

    def start_game(self):
        self.word = random.choice(self.words)
        self.guessed = ["_"] * len(self.word)
        self.tries = 10
        self.used = set()

    def update_ui(self):
        self.label.setText(" ".join(self.guessed))

        hearts = "❤️" * self.tries
        self.hearts_label.setText(f"Жизни: {hearts}")

        self.info.setText(f"Использовано: {', '.join(self.used)}")

    def check(self):
        letter = self.input.text().lower().strip()
        self.input.clear()

        if not letter:
            QMessageBox.warning(self, "Ошибка", "Введите букву")
            return

        if len(letter) > 1:
            QMessageBox.warning(self, "Ошибка", "Только 1 буква")
            return

        if not letter.isalpha():
            QMessageBox.warning(self, "Ошибка", "Только буквы")
            return

        if letter in self.used:
            QMessageBox.warning(self, "Ошибка", "Уже вводил")
            return

        self.used.add(letter)

        if letter in self.word:
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    self.guessed[i] = letter
        else:
            self.tries -= 1
            self.sound.play()

        self.update_ui()

        if "_" not in self.guessed:
            self.win_sound.play()
            QMessageBox.information(self, "Победа", f"Слово: {self.word}")
            self.start_game()
            self.update_ui()

        if self.tries == 0:
            QMessageBox.critical(self, "Проигрыш", f"Слово: {self.word}")
            self.start_game()
            self.update_ui()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Hangman()
    window.show()
    sys.exit(app.exec())