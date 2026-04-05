import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer, Qt, QUrl
from PyQt6.QtGui import QPainter
from PyQt6.QtMultimedia import QSoundEffect  # импортируем для звука


class SnakeGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Змейка")
        self.setGeometry(400, 300, 400, 400)

        self.snake = [(200, 200)]
        self.dx = 20
        self.dy = 0
        self.food = self.spawn_food()


        self.bite_sound = QSoundEffect()
        self.bite_sound.setSource(QUrl.fromLocalFile("bite.wav"))  # путь к файлу bite.wav
        self.bite_sound.setVolume(0.5)  # громкость от 0.0 до 1.0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(150)

    def spawn_food(self):
        return (random.randrange(0, 400, 20), random.randrange(0, 400, 20))

    def update_game(self):
        head = (self.snake[0][0] + self.dx, self.snake[0][1] + self.dy)
        self.snake.insert(0, head)

        if head == self.food:
            self.food = self.spawn_food()
            self.bite_sound.play()  # проигрываем звук при съедании
        else:
            self.snake.pop()

        if head[0] < 0 or head[0] >= 400 or head[1] < 0 or head[1] >= 400:
            self.game_over()

        if head in self.snake[1:]:
            self.game_over()

        self.update()

    def game_over(self):
        self.timer.stop()
        self.snake = [(200, 200)]
        self.dx = 20
        self.dy = 0
        self.food = self.spawn_food()
        self.timer.start(150)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up and self.dy == 0:
            self.dx, self.dy = 0, -20
        elif event.key() == Qt.Key.Key_Down and self.dy == 0:
            self.dx, self.dy = 0, 20
        elif event.key() == Qt.Key.Key_Left and self.dx == 0:
            self.dx, self.dy = -20, 0
        elif event.key() == Qt.Key.Key_Right and self.dx == 0:
            self.dx, self.dy = 20, 0

    def paintEvent(self, event):
        painter = QPainter(self)

        for x, y in self.snake:
            painter.drawRect(x, y, 20, 20)

        fx, fy = self.food
        painter.drawRect(fx, fy, 20, 20)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnakeGame()
    window.show()
    sys.exit(app.exec())