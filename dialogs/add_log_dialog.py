import os
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QDialog,
    QLineEdit,
)
from PyQt5.QtCore import QDateTime, Qt

class AddLogDialog(QDialog):
    """A dialog window for adding new log entries."""

    def __init__(self, parent=None):
        """
        Initialize the AddLogDialog.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent)
        self.setWindowTitle("Add Log")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title label and input field
        self.title_label = QLabel("Enter log title:", self)
        # self.title_label.setStyleSheet(f"color: {FONT_COLOR_WHITE}; font-family: {DISPLAY_FONT}; font-size: 26px; background-color: {BUTTON_BACKGROUND};")
        self.layout.addWidget(self.title_label)
        self.title_input = QLineEdit(self)
        # self.title_input.setStyleSheet(f"color: {FONT_COLOR_WHITE}; font-size: 20px;")
        self.layout.addWidget(self.title_input)

        # Add Log button
        self.add_button = QPushButton("Add Log", self)
        self.add_button.setStyleSheet(
            "QPushButton { color: #EEEEEE; padding: 5px 0 5px 0; background-color: #36454F; border-style: outset; border-radius: 5px; border-width: 1px; border-color: transparent; } "
            "QPushButton:hover { background-color: #222831; color: #22d3ee; border-color: #36454F; }"
        )
        self.add_button.clicked.connect(self.add_log)
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.layout.addWidget(self.add_button)

    def add_log(self):
        """Add a log entry."""
        title = self.title_input.text()
        if title:
            # Get current date and time
            current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
            measured_time = self.parent().time_label.text()
            # Construct log entry
            log_entry = f"{current_time} - {title} - {measured_time}\n"
            # Write log entry to file
            with open(os.path.join(os.path.dirname(__file__), "logs.txt"), "a") as f:
                f.write(log_entry)
            self.parent().logs.append(log_entry.strip())
            self.parent().reset_timer()
            # Close dialog
            self.close()
