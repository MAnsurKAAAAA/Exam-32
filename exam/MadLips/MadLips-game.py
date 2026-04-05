import sys
import json
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)

with open("stories.json", "r", encoding="utf-8") as f:
    stories = json.load(f)

class MadLibsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MadLibs")
        self.setGeometry(100, 100, 500, 400)
        self.current_story = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.input_fields = {}
        self.input_layout = QVBoxLayout()
        layout.addLayout(self.input_layout)

        self.generate_button = QPushButton("start")
        self.generate_button.clicked.connect(self.prepare_story)
        layout.addWidget(self.generate_button)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def prepare_story(self):
        self.current_story = random.choice(stories)
        self.update_inputs()

    def update_inputs(self):
        for i in reversed(range(self.input_layout.count())):
            widget = self.input_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.input_fields.clear()

        story_template = self.current_story["template"]

        placeholders = set()
        temp = story_template
        while "{" in temp and "}" in temp:
            start = temp.index("{") + 1
            end = temp.index("}")
            placeholders.add(temp[start:end])
            temp = temp[end+1:]

        for placeholder in placeholders:
            label = QLabel(f"введите {placeholder}:")
            edit = QLineEdit()
            self.input_fields[placeholder] = edit
            self.input_layout.addWidget(label)
            self.input_layout.addWidget(edit)

        self.generate_button.setText("сгенерировать")
        self.generate_button.clicked.disconnect()
        self.generate_button.clicked.connect(self.generate_story)

    def generate_story(self):
        story_template = self.current_story["template"]
        user_inputs = {}

        for key, field in self.input_fields.items():
            text = field.text().strip()
            if not text:
                QMessageBox.warning(self, "ошибка", f"Поле '{key}' не заполнено!")
                return
            user_inputs[key] = text

        try:
            story = story_template.format(**user_inputs)
            self.output.setText(story)
        except Exception as e:
            QMessageBox.critical(self, "ошибка", f"ошибка: {e}")

        self.generate_button.setText("start")
        self.generate_button.clicked.disconnect()
        self.generate_button.clicked.connect(self.prepare_story)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MadLibsApp()
    window.show()
    sys.exit(app.exec())