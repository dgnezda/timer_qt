from PyQt6.QtWidgets import QApplication
from timer_app import TimerApp
import sys


def main():
    app = QApplication([])
    timer_app = TimerApp()
    timer_app.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
