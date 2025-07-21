import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                            QVBoxLayout, QAction, QMessageBox, QLabel)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tools import ToolBar
from canvas import Canvas
from color_picker import ColorPicker
from error_logger import log_error
import json
import os

class PaintApp(QMainWindow):
    """
    Main window for Professional Paint Editor.
    Contains menu, toolbar, canvas, color picker, settings, and a log/status bar at the bottom.
    """
    def __init__(self):
        """Inicjalizuje główne okno, layout, menu, narzędzia i ładuje ustawienia użytkownika."""
        super().__init__()
        self.setWindowTitle("Professional Paint - by Adrian Lesniak")
        self.setGeometry(100, 100, 1200, 800)

        # --- Pasek informacyjny na górze okna ---
        # Tworzymy widget z opisem programu, autorem i skrótem opcji menu
        info_bar = QLabel()
        info_bar.setText(
            '<b>Professional Paint Editor</b> - author: Adrian Lesniak<br>'
            '<span style="color:#2e7dff;">New (Ctrl+N)</span>, '
            '<span style="color:#43a047;">Open (Ctrl+O)</span>, '
            '<span style="color:#fbc02d;">Save (Ctrl+S)</span>, '
            '<span style="color:#d84315;">Undo (Ctrl+Z)</span>, '
            '<span style="color:#8e24aa;">Effects</span>, '
            '<span style="color:#00838f;">Help</span><br>'
            '<i>Advanced image editor with tools, filters, and file support.</i>'
        )
        info_bar.setAlignment(Qt.AlignCenter)
        info_bar.setStyleSheet(
            'background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e3f2fd, stop:1 #fffde7);'
            'color: #222;'
            'font-size: 13px;'
            'padding: 8px;'
            'border-bottom: 2px solid #90caf9;'
        )

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        layout.addWidget(info_bar)  # Dodajemy pasek informacyjny na górze

        # Add log bar at the bottom
        self.log_bar = QLabel()
        self.log_bar.setText('Ready.')
        self.log_bar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.log_bar.setStyleSheet('background: #e3f2fd; color: #222; font-size: 12px; padding: 6px 12px; border-top: 2px solid #90caf9;')
        layout.addWidget(self.log_bar)

        # --- Reszta layoutu (narzędzia, canvas, itp.) ---
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

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

        content_layout.addWidget(tools_widget)
        content_layout.addWidget(self.canvas, stretch=1)
        layout.addLayout(content_layout)

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

        self.settings_file = os.path.join(os.path.dirname(__file__), 'settings.json')
        self.load_settings()

    def create_menu_bar(self):
        """Tworzy pasek menu z opcjami File, Edit, Effects i Help."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        new_action = QAction('New', self)
        new_action.setIcon(QIcon.fromTheme('document-new'))
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Create new image')
        new_action.triggered.connect(self.confirm_new)

        open_action = QAction('Open', self)
        open_action.setIcon(QIcon.fromTheme('document-open'))
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(lambda: self.try_open_image())

        save_action = QAction('Save', self)
        save_action.setIcon(QIcon.fromTheme('document-save'))
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(lambda: self.try_save_image())
        
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)

        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        undo_action = QAction('Undo', self)
        undo_action.setIcon(QIcon.fromTheme('edit-undo'))
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.canvas.undo)

        redo_action = QAction('Redo', self)
        redo_action.setIcon(QIcon.fromTheme('edit-redo'))
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.canvas.redo)
        
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        # Effects menu
        effects_menu = menubar.addMenu('Effects')
        
        blur_action = QAction('Blur', self)
        blur_action.setIcon(QIcon.fromTheme('image-blur'))
        blur_action.triggered.connect(lambda: self.try_apply_filter('blur'))
        
        sharpen_action = QAction('Sharpen', self)
        sharpen_action.setIcon(QIcon.fromTheme('image-sharpen'))
        sharpen_action.triggered.connect(lambda: self.try_apply_filter('sharpen'))
        
        grayscale_action = QAction('Grayscale', self)
        grayscale_action.setIcon(QIcon.fromTheme('image-grayscale'))
        grayscale_action.triggered.connect(lambda: self.try_apply_filter('grayscale'))
        
        invert_action = QAction('Invert Colors', self)
        invert_action.setIcon(QIcon.fromTheme('image-invert'))
        invert_action.triggered.connect(lambda: self.try_apply_filter('invert'))
        
        brightness_action = QAction('Adjust Brightness...', self)
        brightness_action.setIcon(QIcon.fromTheme('image-brightness'))
        brightness_action.triggered.connect(lambda: self.try_apply_filter('brightness'))
        
        contrast_action = QAction('Adjust Contrast...', self)
        contrast_action.setIcon(QIcon.fromTheme('image-contrast'))
        contrast_action.triggered.connect(lambda: self.try_apply_filter('contrast'))

        effects_menu.addAction(blur_action)
        effects_menu.addAction(sharpen_action)
        effects_menu.addAction(grayscale_action)
        effects_menu.addAction(invert_action)
        effects_menu.addAction(brightness_action)
        effects_menu.addAction(contrast_action)

        # Help menu
        help_menu = menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.setIcon(QIcon.fromTheme('help-about'))
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        shortcuts_action = QAction('Shortcuts', self)
        shortcuts_action.setIcon(QIcon.fromTheme('help-contents'))
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)

    def log_action(self, message):
        """Display a message in the log bar at the bottom."""
        self.log_bar.setText(message)

    def confirm_new(self):
        """Confirms creating a new canvas, handles exceptions and menu return."""
        try:
            reply = QMessageBox.question(self, 'New Canvas',
                                       'Are you sure you want to create a new canvas?\nAny unsaved changes will be lost.',
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.canvas.new_canvas()
                self.log_action('A new canvas has been created.')
        except Exception as e:
            log_error(f'Error creating new canvas: {e}')
            QMessageBox.critical(self, 'Error', 'An error occurred while creating a new canvas.')
            self.log_action('An error occurred while creating a new canvas.')

    def show_about(self):
        """Shows the About dialog."""
        try:
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
            self.log_action('About dialog displayed.')
        except Exception as e:
            log_error(f'Error in About dialog: {e}')
            QMessageBox.critical(self, 'Error', 'An error occurred in the About dialog.')
            self.log_action('An error occurred in the About dialog.')

    def show_shortcuts(self):
        """Shows the keyboard shortcuts dialog."""
        try:
            QMessageBox.information(self, 'Keyboard Shortcuts',
                'Ctrl+N: New Image\n'
                'Ctrl+O: Open Image\n'
                'Ctrl+S: Save Image\n'
                'Ctrl+Z: Undo\n'
                'Ctrl+Y: Redo\n'
                'Space: Pan canvas\n'
                'Mouse wheel: Zoom canvas')
            self.log_action('Keyboard shortcuts displayed.')
        except Exception as e:
            log_error(f'Error in shortcuts dialog: {e}')
            QMessageBox.critical(self, 'Error', 'An error occurred in the shortcuts dialog.')
            self.log_action('An error occurred in the shortcuts dialog.')

    def load_settings(self):
        """Ładuje ustawienia z pliku JSON, takie jak ostatni kolor i narzędzie."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # Przykład: ustaw ostatni kolor i narzędzie
                    if 'last_color' in settings:
                        self.canvas.set_color(settings['last_color'])
                    if 'last_tool' in settings:
                        self.tool_bar.set_tool(settings['last_tool'])
        except Exception as e:
            log_error(f'Błąd przy wczytywaniu ustawień: {e}')

    def save_settings(self):
        """Zapisuje ustawienia do pliku JSON, takie jak ostatni kolor i narzędzie."""
        try:
            settings = {
                'last_color': getattr(self.canvas, 'current_color', None),
                'last_tool': getattr(self.tool_bar, 'current_tool', None)
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f)
        except Exception as e:
            log_error(f'Błąd przy zapisie ustawień: {e}')

    def closeEvent(self, event):
        """Obsługuje zdarzenie zamknięcia okna aplikacji, zapisując ustawienia przed zamknięciem."""
        self.save_settings()
        event.accept()

    def try_save_image(self):
        try:
            self.canvas.save_image(self.log_action)
        except Exception as e:
            log_error(f'Error saving image: {e}')
            self.log_action('An error occurred while saving the image.')

    def try_open_image(self):
        try:
            self.canvas.open_image(self.log_action)
        except Exception as e:
            log_error(f'Error opening image: {e}')
            self.log_action('An error occurred while opening the image.')

    def try_apply_filter(self, filter_name):
        try:
            self.canvas.apply_filter(filter_name, self.log_action)
        except Exception as e:
            log_error(f'Error applying filter {filter_name}: {e}')
            self.log_action(f'An error occurred while applying filter {filter_name}.')

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = PaintApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        log_error(f'Błąd krytyczny aplikacji: {e}')
        QMessageBox.critical(None, 'Błąd krytyczny', 'Wystąpił błąd krytyczny aplikacji. Sprawdź plik error_log.txt.')
