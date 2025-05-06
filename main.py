import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                            QVBoxLayout, QAction, QMessageBox, QLabel)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tools import ToolBar
from canvas import Canvas
from color_picker import ColorPicker

class PaintApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Paint - by Adrian Lesniak")
        self.setGeometry(100, 100, 1200, 800)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(5, 5, 5, 5)

        # Create canvas
        self.canvas = Canvas()
        
        # Create toolbars and color picker
        self.tool_bar = ToolBar(self.canvas)
        self.color_picker = ColorPicker(self.canvas)

        # Replace info label with image
        image_label = QLabel()
        try:
            # Load image as a simple QPixmap without color profile
            pixmap = QPixmap(160, 120)  # Create empty pixmap
            pixmap.fill(QColor("#333333"))  # Fill with dark background
            
            # Add wrapped text to image
            painter = QPainter(pixmap)
            painter.setPen(QColor("#FFFFFF"))
            font = QFont("Arial", 10)
            painter.setFont(font)
            
            # Create text with word wrapping
            rect = pixmap.rect().adjusted(10, 10, -10, -10)  # Add 10px padding
            quote = '"Creativity is intelligence having fun."\n- Albert Einstein'
            painter.drawText(rect, Qt.AlignCenter | Qt.TextWordWrap, quote)
            painter.end()
            
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
        except Exception as e:
            print(f"Image creation error: {e}")
            image_label.setText("Professional Paint")
        
        # Update layout with more space
        tools_widget = QWidget()
        tools_widget.setMaximumWidth(160)  # Wider for larger image
        tools_panel = QVBoxLayout(tools_widget)
        tools_panel.setContentsMargins(5, 10, 5, 5)  # Add top padding
        tools_panel.setSpacing(10)  # Increase spacing between elements
        
        tools_panel.addWidget(image_label)
        tools_panel.addSpacing(10)  # Add space after image
        tools_panel.addWidget(self.tool_bar)
        tools_panel.addSpacing(15)  # Add more space before color picker
        tools_panel.addWidget(self.color_picker)
        tools_panel.addStretch(1)

        layout.addWidget(tools_widget)
        layout.addWidget(self.canvas, stretch=1)

        self.create_menu_bar()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QMenuBar {
                background-color: #333333;
                color: #FFFFFF;
            }
            QMenuBar::item:selected {
                background-color: #404040;
            }
            QMenu {
                background-color: #333333;
                color: #FFFFFF;
                border: 1px solid #404040;
            }
            QMenu::item:selected {
                background-color: #404040;
            }
            QLabel {
                color: #FFFFFF;
            }
            QMessageBox {
                background-color: #333333;
                color: #FFFFFF;
            }
            QMessageBox QPushButton {
                background-color: #404040;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 5px;
                min-width: 70px;
            }
            QMessageBox QPushButton:hover {
                background-color: #505050;
            }
        """)

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Create new image')
        new_action.triggered.connect(self.confirm_new)

        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.canvas.open_image)

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.canvas.save_image)
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)

        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        undo_action = QAction('Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.canvas.undo)

        redo_action = QAction('Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.canvas.redo)
        
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        # Effects menu
        effects_menu = menubar.addMenu('Effects')
        
        blur_action = QAction('Blur', self)
        blur_action.triggered.connect(lambda: self.canvas.apply_filter('blur'))
        
        sharpen_action = QAction('Sharpen', self)
        sharpen_action.triggered.connect(lambda: self.canvas.apply_filter('sharpen'))
        
        grayscale_action = QAction('Grayscale', self)
        grayscale_action.triggered.connect(lambda: self.canvas.apply_filter('grayscale'))
        
        invert_action = QAction('Invert Colors', self)
        invert_action.triggered.connect(lambda: self.canvas.apply_filter('invert'))
        
        brightness_action = QAction('Adjust Brightness...', self)
        brightness_action.triggered.connect(lambda: self.canvas.apply_filter('brightness'))
        
        contrast_action = QAction('Adjust Contrast...', self)
        contrast_action.triggered.connect(lambda: self.canvas.apply_filter('contrast'))

        effects_menu.addAction(blur_action)
        effects_menu.addAction(sharpen_action)
        effects_menu.addAction(grayscale_action)
        effects_menu.addAction(invert_action)
        effects_menu.addAction(brightness_action)
        effects_menu.addAction(contrast_action)

        # Help menu
        help_menu = menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        shortcuts_action = QAction('Shortcuts', self)
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)

    def confirm_new(self):
        reply = QMessageBox.question(self, 'New Canvas',
                                   'Are you sure you want to create a new canvas?\nAny unsaved changes will be lost.',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.canvas.new_canvas()

    def show_about(self):
        QMessageBox.about(self, 'About Professional Paint',
            '<h3>Professional Paint Editor</h3>'
            '<p>Version 1.0</p>'
            '<p>Created by Adrian Lesniak</p>'
            '<p>A professional image editing tool with:'
            '<ul>'
            '<li>Multiple drawing tools</li>'
            '<li>Image filters and effects</li>'
            '<li>Layer support</li>'
            '<li>File operations</li>'
            '</ul></p>')

    def show_shortcuts(self):
        QMessageBox.information(self, 'Keyboard Shortcuts',
            'Ctrl+N: New Image\n'
            'Ctrl+O: Open Image\n'
            'Ctrl+S: Save Image\n'
            'Ctrl+Z: Undo\n'
            'Ctrl+Y: Redo\n'
            'Space: Pan canvas\n'
            'Mouse wheel: Zoom canvas')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PaintApp()
    window.show()
    sys.exit(app.exec_())
