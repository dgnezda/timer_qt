import os
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QDialog,
    QListWidget,
    QMessageBox
)
from datetime import datetime, timedelta
from collections import defaultdict

class LogsDialog(QDialog):
    """A dialog window to manage logs."""

    def __init__(self, parent=None):
        """
        Initialize the LogsDialog.

        Args:
            logs (list): A list of log entries to display.
        """
        super().__init__(parent)
        self.setFixedWidth(400)
        self.setWindowTitle("View Logs")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # List widget to display logs
        self.logs_list = QListWidget(self)
        self.layout.addWidget(self.logs_list)

        # Remove Log button
        self.remove_button = QPushButton("Remove Log", self)
        self.remove_button.setStyleSheet(
            "QPushButton { color: #EEEEEE; background-color: #36454F; padding: 7px 30px 7px 30px; border-style: outset; border-radius: 5px; border-width: 1px; border-color: transparent; } "
            "QPushButton:hover { background-color: #222831; color: #22d3ee; border-color: #36454F;  }"
        )
        self.remove_button.clicked.connect(self.remove_log)
        self.layout.addWidget(self.remove_button)

        # Clear All button
        self.clear_all_button = QPushButton("Clear All", self)
        self.clear_all_button.setStyleSheet(
            "QPushButton { color: #EEEEEE; background-color: #36454F; padding: 7px 30px 7px 30px; border-style: outset; border-radius: 5px; border-width: 1px; border-color: transparent; } "
            "QPushButton:hover { background-color: #222831; color: #22d3ee; border-color: #36454F;  }"
        )
        self.clear_all_button.clicked.connect(self.clear_all_logs)
        self.layout.addWidget(self.clear_all_button)

        # Export Logs button
        self.export_button = QPushButton("Export Logs", self)
        self.export_button.setStyleSheet(
            "QPushButton { color: #EEEEEE; background-color: #36454F; padding: 7px 30px 7px 30px; border-style: outset; border-radius: 5px; border-width: 1px; border-color: transparent; } "
            "QPushButton:hover { background-color: #222831; color: #22d3ee; border-color: #36454F;  }"
        )
        self.export_button.clicked.connect(self.export_logs)
        self.layout.addWidget(self.export_button)

        self.logs = self.read_logs()
        self.load_logs()
    
    def read_logs(self):
        """Reads logs from the file and returns them as a list."""
        logs_path = os.path.join(os.path.dirname(__file__), "logs.txt")
        with open(logs_path, "r") as file:
            return [line.strip() for line in file]

    def load_logs(self):
        """Load logs into the QListWidget from self.logs."""
        self.logs_list.clear()
        for log in self.logs:
            self.logs_list.addItem(log)

    def remove_log(self):
        """Remove the selected log entry."""
        selected_item = self.logs_list.currentItem()
        if selected_item:
            log_to_remove = selected_item.text()
            confirmation = QMessageBox()
            confirmation.setWindowTitle("Confirm Removal")
            confirmation.setText(f"Are you sure you want to remove the log '{log_to_remove}'?")
            confirmation.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            choice = confirmation.exec()

            if choice == QMessageBox.StandardButton.Yes:
                self.logs.remove(log_to_remove)
                self.update_log_file()
                self.load_logs()
        else:
            QMessageBox.critical(self, "Error", "Please select a log to remove.")
    
    def update_log_file(self):
        """Update the logs.txt file based on current state of self.logs."""
        logs_path = os.path.join(os.path.dirname(__file__), "logs.txt")
        with open(logs_path, "w") as file:
            for log in self.logs:
                file.write(log + '\n')    

    def clear_all_logs(self):
        """Clear all logs."""
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Confirm Clear All")
        confirmation.setText("Are you sure you want to clear all logs? This action cannot be undone.")
        confirmation.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        choice = confirmation.exec()

        if choice == QMessageBox.StandardButton.Yes:
            self.logs = []
            self.update_log_file()
            self.load_logs()

    def export_logs(self):
        """Export logs to a Markdown file."""
        logs, = self.get_logs()  # Extract the sorted list of tuples from the returned tuple
        if logs:
            first_log_entry = logs[0][1][next(iter(logs[0][1]))][0]
            last_log_project, last_versions_dict = logs[-1]
            last_log_entry = last_versions_dict[next(iter(last_versions_dict))][-1]

            first_timestamp = datetime.strptime(first_log_entry.split(" - ")[0][:10], "%Y-%m-%d")
            last_timestamp = datetime.strptime(last_log_entry.split(" - ")[0][:10], "%Y-%m-%d")

            filename = f"logs_{first_timestamp.date()}-{last_timestamp.date()}.md"
            total_time = timedelta()
            with open(filename, "w") as file:
                file.write(f"# Time Log entries from {first_timestamp.date()} to {last_timestamp.date()}\n\n")
                for project, versions in logs:
                    project_time = timedelta()
                    file.write(f"## Project name: {project}\n\n")
                    for version, entries in versions.items():
                        version_time = timedelta()
                        file.write(f"### Version: {version}\n\n")
                        for entry in entries:
                            timestamp, project_version_time = entry.split(" - ", 1)
                            time_str = project_version_time.split("- ")[-1]
                            hrs, mins, secs = map(int, time_str.split(":"))
                            version_time += timedelta(hours=hrs, minutes=mins, seconds=secs)
                            file.write(f"- **{timestamp}**: {project_version_time}\n")
                        file.write("\n")
                        project_time += version_time
                        total_time += version_time
                    file.write(f"### Total time logged for {project}: {str(project_time)}\n\n")
                file.write(f"## Total time logged for all projects: {str(total_time)}\n")
            QMessageBox.information(self, "Export Successful", "Logs exported successfully to Markdown file.", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.warning(self, "No Logs", "No logs to export.", QMessageBox.StandardButton.Ok)


    def get_logs(self):
        """Retrieve logs grouped by project and version."""
        logs = defaultdict(lambda: defaultdict(list))
        for log in self.logs:
            parts = log.split(" - ")
            timestamp = parts[0]
            project, version = parts[1].split(" ", 1)
            time = parts[2]
            logs[project][version].append(f"{timestamp} - {project} {version}- {time}")
        return sorted(logs.items()),
