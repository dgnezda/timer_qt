import os
from PyQt5.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QDialog,
    QListWidget,
    QMessageBox
)


class LogsDialog(QDialog):
    """A dialog window to manage logs."""

    def __init__(self, logs, parent=None):
        """
        Initialize the LogsDialog.

        Args:
            logs (list): A list of log entries to display.
        """
        super().__init__(parent)
        self.setWindowTitle("View Logs")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # List widget to display logs
        self.logs_list = QListWidget(self)
        self.layout.addWidget(self.logs_list)

        # Remove Log button
        self.remove_button = QPushButton("Remove Log", self)
        self.remove_button.setStyleSheet(
            "QPushButton { color: #EEEEEE; background-color: #36454F; border-style: outset; border-radius: 5px; border-width: 2px; border-color: transparent; } QPushButton:hover { color: #22d3ee }"
        )
        self.remove_button.clicked.connect(self.remove_log)
        self.layout.addWidget(self.remove_button)

        self.load_logs(logs)

    def load_logs(self, logs):
        """Load logs from logs.txt file."""
        with open(os.path.join(os.path.dirname(__file__), "logs.txt"), "r") as f:
            for line in f:
                self.logs_list.addItem(line.strip())

    def remove_log(self):
        """Remove the selected log entry."""
        selected_item = self.logs_list.currentItem()
        if selected_item:
            log_to_remove = selected_item.text()
            confirmation = QMessageBox(self)
            confirmation.setWindowTitle("Confirm Removal")
            confirmation.setText(f"Are you sure you want to remove the log '{log_to_remove}'?")
            confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            # Set stylesheet for QMessageBox and its buttons
            confirmation.setStyleSheet(
                "QMessageBox { background-color: #222831; }"
                "QPushButton { color: #EEEEEE; background-color: #36454F; border-style: outset; border-radius: 5px; border-width: 2px; border-color: transparent; } "
                "QPushButton:hover { color: #22d3ee } "
            )

            # Execute the QMessageBox and check the user's choice
            choice = confirmation.exec_()
            if choice == QMessageBox.Yes:
                self.logs_list.takeItem(self.logs_list.row(selected_item))
                parent_widget = self.parent()
                if parent_widget and log_to_remove in parent_widget.logs:
                    parent_widget.logs.remove(log_to_remove)
                    with open(os.path.join(os.path.dirname(__file__), "logs.txt"), "w") as f:
                        for log in parent_widget.logs:
                            f.write(log + '\n')
        else:
            QMessageBox.critical(self, "Error", "Please select a log to remove.")


