from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QTimer, Qt
from src.constants import (
    DISPLAY_FONT, 
    BACKGROUND_COLOR, 
    FONT_COLOR_WHITE, 
    FONT_COLOR_BLUE, 
)

from src.dialogs.add_log_dialog import AddLogDialog
from src.dialogs.logs_dialog import LogsDialog


class TimerApp(QMainWindow):
    """Main application window for the Timer App."""

    def __init__(self):
        """Initialize the TimerApp."""
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Time Logger")
        self.setStyleSheet(f"background-color: {BACKGROUND_COLOR}; color: {FONT_COLOR_WHITE}")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        # Timer label
        self.time_label = QLabel("0:00:00", self)
        self.time_label.setStyleSheet(
            f"color: {FONT_COLOR_WHITE}; font-family: {DISPLAY_FONT}; font-size: 46px;"
        )
        self.layout.addWidget(self.time_label)

        # Control buttons
        button_layout = QHBoxLayout()
        # Start Button
        self.start_button = QPushButton("►", self)
        self.start_button.setShortcut("Ctrl+S")
        self.start_button.setStyleSheet(
            "QPushButton { color: #EEEEEE; padding: 5px 0 5px 0; background-color: #36454F; border-style: outset; border-radius: 5px; border-width: 1px; border-color: transparent; } "
            "QPushButton:hover { background-color: #222831; color: #22d3ee; border-color: #36454F; }"
        )
        self.start_button.clicked.connect(self.start_timer)
        self.start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addWidget(self.start_button)
        # Reset Button
        self.reset_button = QPushButton("↺", self)
        self.reset_button.setShortcut("Ctrl+R")
        self.reset_button.setStyleSheet(
            "QPushButton { color: #EEEEEE; padding: 5px 0 5px 0; background-color: #36454F; border-style: outset; border-radius: 5px; border-width: 1px; border-color: transparent; } "
            "QPushButton:hover { background-color: #222831; color: #22d3ee; border-color: #36454F; }"
        )
        self.reset_button.clicked.connect(self.reset_timer)
        self.reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addWidget(self.reset_button)
        # Add Log Button
        self.add_log_button = QPushButton("+", self)
        self.add_log_button.setShortcut("Ctrl+A")
        self.add_log_button.setStyleSheet(
            "QPushButton { color: #EEEEEE; padding: 5px 0 5px 0; background-color: #36454F; border-style: outset; border-radius: 5px; border-width: 1px; border-color: transparent; } "
            "QPushButton:hover { background-color: #222831; color: #22d3ee; border-color: #36454F; }"
        )
        self.add_log_button.clicked.connect(self.open_add_log_dialog)
        self.add_log_button.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addWidget(self.add_log_button)
        self.add_log_button.setEnabled(False) 
        self.layout.addLayout(button_layout)
        # View Logs Button
        self.view_logs_button = QPushButton("≣", self)
        self.view_logs_button.setStyleSheet(
            "QPushButton { color: #EEEEEE; padding: 5px 10px; background-color: #36454F; border-style: outset; border-radius: 5px; border-width: 1px; border-color: transparent; } "
            "QPushButton:hover { background-color: #222831; color: #22d3ee; border-color: #36454F; }"
        )
        self.view_logs_button.clicked.connect(self.open_view_logs_dialog)
        self.view_logs_button.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addWidget(self.view_logs_button)

        # Timer setup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.seconds = 0
        self.running = False

        # Menu setup
        self.create_menu()

    def start_timer(self):
        """Start or pause the timer."""
        if not self.running:
            self.running = True
            self.start_button.setText("■")
            self.add_log_button.setEnabled(False)
            self.time_label.setStyleSheet(
                f"color: {FONT_COLOR_BLUE}; font-family: {DISPLAY_FONT}; font-size: 46px;"
            ) 
            self.timer.start(1000)
        else:
            self.running = False
            self.start_button.setText("►")
            self.add_log_button.setEnabled(True)
            self.pause_timer()

    def pause_timer(self): 
        """Pause the timer."""
        self.running = False
        self.time_label.setStyleSheet(
            f"color: {FONT_COLOR_WHITE}; font-family: {DISPLAY_FONT}; font-size: 46px;"
        ) 
        self.timer.stop()

    def reset_timer(self):
        """Reset the timer."""
        self.running = False
        self.seconds = 0
        self.time_label.setText("0:00:00")
        self.start_button.setText("►")
        self.add_log_button.setEnabled(False)
        self.time_label.setStyleSheet(
            f"color: {FONT_COLOR_WHITE}; font-family: {DISPLAY_FONT}; font-size: 46px;"
        ) 

    def update_timer(self):
        """Update the timer display."""
        self.seconds += 1
        hours = self.seconds // 3600
        minutes = (self.seconds // 60) % 60
        seconds = self.seconds % 60
        self.time_label.setText(f"{hours}:{minutes:02}:{seconds:02}")

    def open_add_log_dialog(self):
        """Open the dialog for adding a log."""
        dialog = AddLogDialog(self)
        dialog.exec()

    def create_menu(self):
        """Create the application menu."""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        # View logs action
        view_logs_action = QAction("View Logs", self)
        view_logs_action.setShortcut("Ctrl+O")
        view_logs_action.triggered.connect(self.open_view_logs_dialog)
        file_menu.addAction(view_logs_action)
        # Export logs action
        export_logs_action = QAction(QIcon(), "Export Logs", self)
        export_logs_action.setShortcut("Ctrl+E")
        export_logs_action.triggered.connect(self.export_logs_from_menu)
        file_menu.addAction(export_logs_action)

    def open_view_logs_dialog(self):
        """Open the dialog for viewing logs."""
        dialog = LogsDialog(parent=self)
        dialog.exec()
    
    def export_logs_from_menu(self):
        """Method to export logs from the menu."""
        dialog = LogsDialog(parent=self)
        dialog.export_logs()