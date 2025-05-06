from PyQt5.QtWidgets import QWidget, QColorDialog, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class ColorPicker(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Primary color button (left click)
        self.primary_button = QPushButton()
        self.primary_button.setFixedSize(50, 50)
        self.primary_color = QColor(Qt.black)
        self.primary_button.clicked.connect(lambda: self.show_color_dialog('primary'))
        
        # Secondary color button (right click)
        self.secondary_button = QPushButton()
        self.secondary_button.setFixedSize(50, 50)
        self.secondary_color = QColor(Qt.white)
        self.secondary_button.clicked.connect(lambda: self.show_color_dialog('secondary'))
        
        # Labels
        primary_label = QLabel("Primary (Left Click)")
        primary_label.setStyleSheet("color: white;")
        secondary_label = QLabel("Secondary (Right Click)")
        secondary_label.setStyleSheet("color: white;")
        
        layout.addStretch(1)  # Push buttons down
        layout.addWidget(primary_label)
        layout.addWidget(self.primary_button)
        layout.addWidget(secondary_label)
        layout.addWidget(self.secondary_button)
        layout.addStretch(1)  # Keep buttons centered vertically
        
        self.update_button_colors()
        self.setLayout(layout)

    def show_color_dialog(self, button_type):
        color = QColorDialog.getColor(
            self.primary_color if button_type == 'primary' else self.secondary_color
        )
        if color.isValid():
            if button_type == 'primary':
                self.primary_color = color
                self.canvas.set_primary_color(color)
            else:
                self.secondary_color = color
                self.canvas.set_secondary_color(color)
            self.update_button_colors()

    def update_button_colors(self):
        self.primary_button.setStyleSheet(
            f"background-color: {self.primary_color.name()};"
            f"border: 2px solid #666666;"
        )
        self.secondary_button.setStyleSheet(
            f"background-color: {self.secondary_color.name()};"
            f"border: 2px solid #666666;"
        )
