from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSystemTrayIcon, 
    QMenu,
    QApplication
)
from PyQt6.QtGui import QAction, QIcon, QFont
from PyQt6.QtCore import QTimer, Qt
from src.constants import (
    DISPLAY_FONT, 
    BACKGROUND_COLOR, 
    FONT_COLOR_WHITE, 
    FONT_COLOR_BLUE, 
)
from src.dialogs.add_log_dialog import AddLogDialog
from src.dialogs.view_logs_dialog import ViewLogsDialog


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
        self.start_button.setStyleSheet(
            "QPushButton { color: #EEEEEE; padding: 5px 0 5px 0; background-color: #36454F; border-style: outset; border-radius: 5px; border-width: 1px; border-color: transparent; } "
            "QPushButton:hover { background-color: #222831; color: #22d3ee; border-color: #36454F; }"
        )
        self.start_button.clicked.connect(self.start_timer)
        self.start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addWidget(self.start_button)

        # Reset Button
        self.reset_button = QPushButton("↺", self)
        self.reset_button.setStyleSheet(
            "QPushButton { color: #EEEEEE; padding: 5px 0 5px 0; background-color: #36454F; border-style: outset; border-radius: 5px; border-width: 1px; border-color: transparent; } "
            "QPushButton:hover { background-color: #222831; color: #22d3ee; border-color: #36454F; }"
        )
        self.reset_button.clicked.connect(self.reset_timer)
        self.reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        button_layout.addWidget(self.reset_button)
        self.reset_button.setEnabled(False)

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

        # System tray icon and menu
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("img/icon.png"))
        self.tray_icon.setToolTip('Time Logger')
        self.tray_menu = QMenu()

        # Live timer display - tray menu
        self.tray_timer_label = QAction('Timer: 0:00:00', self.tray_menu)
        self.tray_timer_label.setFont(QFont('Helvetica', 10))
        self.tray_timer_label.setDisabled(True)
        self.tray_menu.addAction(self.tray_timer_label)
        self.tray_menu.addSeparator()

        # Timer controls - tray menu
        self.start_action = self.tray_menu.addAction('Start Timer')
        self.pause_action = self.tray_menu.addAction('Pause Timer')
        self.reset_action = self.tray_menu.addAction('Reset Timer')
        self.tray_menu.addSeparator()

        # Other actions - tray menu
        self.add_log_action = self.tray_menu.addAction('Add Log')
        self.view_logs_action = self.tray_menu.addAction('View Logs')
        self.export_logs_action = self.tray_menu.addAction('Export Logs')
        self.tray_menu.addSeparator()

        # Quit action - tray menu
        self.quit_action = self.tray_menu.addAction('Quit Time Logger')

        # Connect actions to functions
        self.start_action.triggered.connect(self.start_timer)
        self.pause_action.triggered.connect(self.pause_timer)
        self.reset_action.triggered.connect(self.reset_timer)
        self.add_log_action.triggered.connect(self.open_add_log_dialog)
        self.view_logs_action.triggered.connect(self.open_view_logs_dialog)
        self.export_logs_action.triggered.connect(self.export_logs_from_menu)
        self.quit_action.triggered.connect(QApplication.instance().quit)

        # Set the menu for the system tray icon
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        # Menu setup
        self.create_menu()

    def keyPressEvent(self, event):
        """Handle key press events in the application."""
        if event.key() == Qt.Key.Key_Space:
            self.toggle_timer()
        else:
            super().keyPressEvent(event)
    
    def toggle_timer(self):
        """Toggle the timer between running and paused."""
        if self.running:
            self.pause_timer()
        else:
            self.start_timer()

    def start_timer(self):
        """Start the timer."""
        if not self.running:
            self.running = True
            self.start_button.setText("■")
            self.add_log_button.setEnabled(False)
            self.time_label.setStyleSheet(
                f"color: {FONT_COLOR_BLUE}; font-family: {DISPLAY_FONT}; font-size: 46px;"
            )
            self.reset_button.setEnabled(False) 
            self.timer.start(1000)
        else:
            self.running = False
            self.start_button.setText("►")
            self.add_log_button.setEnabled(True)
            self.pause_timer()
            self.reset_button.setEnabled(True)

    def pause_timer(self): 
        """Pause the timer."""
        self.running = False
        self.reset_button.setEnabled(True)
        self.start_button.setText("►")
        self.add_log_button.setEnabled(True)
        self.time_label.setStyleSheet(
            f"color: {FONT_COLOR_WHITE}; font-family: {DISPLAY_FONT}; font-size: 46px;"
        ) 
        self.timer.stop()

    def reset_timer(self):
        """Reset the timer."""
        self.running = False
        self.seconds = 0
        self.time_label.setText("0:00:00")
        self.tray_timer_label.setText('Timer: 0:00:00')
        self.start_button.setText("►")
        self.add_log_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.time_label.setStyleSheet(
            f"color: {FONT_COLOR_WHITE}; font-family: {DISPLAY_FONT}; font-size: 46px;"
        ) 

    def update_timer(self):
        """Update the timer display."""
        self.seconds += 1
        hours = self.seconds // 3600
        minutes = (self.seconds // 60) % 60
        seconds = self.seconds % 60
        formatted_time = f"{hours}:{minutes:02}:{seconds:02}"
        self.time_label.setText(formatted_time)
        self.tray_timer_label.setText(f"Timer: {formatted_time}")

        if not self.tray_icon.isVisible():
            self.tray_icon.show()

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
        dialog = ViewLogsDialog(parent=self)
        dialog.exec()
    
    def export_logs_from_menu(self):
        """Method to export logs from the menu."""
        dialog = ViewLogsDialog(parent=self)
        dialog.export_logs()