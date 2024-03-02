import os
import webbrowser
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QCheckBox, QGridLayout
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont

class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App Launcher")
        self.setup_ui()
        self.dark_mode = False

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        layout.setAlignment(Qt.AlignCenter)

        # Title label
        title_label = QLabel("ATTENDENCE APPLICATION")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 30))
        layout.addWidget(title_label)

        # Dark mode switch
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        layout.addWidget(self.dark_mode_checkbox)

        # Buttons layout
        self.buttons_layout = QGridLayout()
        layout.addLayout(self.buttons_layout)

        # Buttons
        self.create_button("Get Faces from Camera", lambda: self.launch_app("get_faces_from_camera_tkinter.py"), 0, 0)
        self.create_button("Features Extraction to CSV", lambda: self.launch_app("features_extraction_to_csv.py"), 0, 1)
        self.create_button("Attendance Taker", lambda: self.launch_app("attendance_taker.py"), 1, 0)
        self.create_button("Launch Flask App", self.launch_flask_app, 1, 1)

        # Message label
        self.message_label = QLabel("Made by Gurjot Singh")
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

    def create_button(self, text, on_click, row, column):
        button = QPushButton(text)
        button.clicked.connect(on_click)
        self.buttons_layout.addWidget(button, row, column)

        # Animation
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(QRect(button.x(), button.y() + 200, button.width(), button.height()))
        animation.setEndValue(QRect(button.x(), button.y(), button.width(), button.height()))
        animation.start(QPropertyAnimation.DeleteWhenStopped)

    def launch_app(self, file_name):
        try:
            os.system("python " + os.path.join(os.path.dirname(__file__), file_name))
        except Exception as e:
            print("Error launching app:", e)

    def launch_flask_app(self):
        try:
            subprocess.Popen(["python", os.path.join(os.path.dirname(__file__), "app.py")])
            self.timer = self.startTimer(5000)
        except Exception as e:
            print("Error launching Flask app:", e)

    def toggle_dark_mode(self, state):
        self.dark_mode = state == Qt.Checked
        self.update_theme()

    def update_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #222;
                    color: white;
                }
                QLabel {
                    color: white;
                }
                QCheckBox {
                    color: white;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 10px;
                    border: 2px solid #4CAF50;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                    border: 2px solid #45a049;
                }
            """)
            self.message_label.setStyleSheet("color: white;")
        else:
            self.setStyleSheet("")
            self.message_label.setStyleSheet("")

    def resizeEvent(self, event):
        self.update_button_sizes()

    def update_button_sizes(self):
        for row in range(self.buttons_layout.rowCount()):
            for col in range(self.buttons_layout.columnCount()):
                item = self.buttons_layout.itemAtPosition(row, col)
                if item is not None:
                    button = item.widget()
                    button.setFixedSize(self.width() // self.buttons_layout.columnCount() - 20, 50)

    def timerEvent(self, event):
        self.killTimer(self.timer)
        webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    app = QApplication([])
    launcher = LauncherWindow()
    launcher.showFullScreen()
    app.exec_()