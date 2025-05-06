from PyQt5.QtWidgets import QToolBar, QAction, QSpinBox, QVBoxLayout, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class ToolBar(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.actions = []
        self.init_tools()

    def init_tools(self):
        layout = QVBoxLayout()
        layout.setSpacing(3)  # Slightly increase spacing
        layout.setContentsMargins(2, 5, 2, 5)  # Add more top/bottom padding

        tools = [
            ("Brush", "brush"),
            ("Eraser", "eraser"),
            ("Line", "line"),
            ("Rectangle", "rectangle"),
            ("Circle", "circle"),
            ("Spray", "spray"),
            ("Fill", "fill"),
            ("Text", "text"),
            ("Gradient", "gradient"),
            ("Polygon", "polygon"),
            ("Selection", "selection")
        ]

        tool_group = QWidget()
        tool_layout = QVBoxLayout(tool_group)
        tool_layout.setSpacing(1)
        tool_layout.setContentsMargins(0, 0, 0, 0)

        for name, tool in tools:
            action = QPushButton(name)
            action.setCheckable(True)
            action.setStyleSheet("""
                QPushButton {
                    background-color: #404040;
                    color: white;
                    border: 1px solid #555555;
                    padding: 5px;
                    margin: 1px;
                }
                QPushButton:checked {
                    background-color: #666666;
                }
                QPushButton:hover {
                    background-color: #505050;
                }
            """)
            action.clicked.connect(lambda checked, t=tool: self.select_tool(t))
            tool_layout.addWidget(action)
            self.actions.append(action)
        
        self.actions[0].setChecked(True)
        layout.addWidget(tool_group)

        # Move brush size control down a bit
        layout.addSpacing(10)  # Add space before brush size control
        size_label = QLabel("Brush Size:")
        size_label.setStyleSheet("color: white; padding-top: 5px;")
        layout.addWidget(size_label)
        
        self.brush_size = QSpinBox()
        self.brush_size.setMinimum(1)
        self.brush_size.setMaximum(50)
        self.brush_size.setValue(3)
        self.brush_size.valueChanged.connect(self.canvas.set_brush_size)
        layout.addWidget(self.brush_size)

        layout.addStretch()
        self.setLayout(layout)

    def select_tool(self, tool):
        for action in self.actions:
            action.setChecked(action.text().lower() == tool)
        self.canvas.set_tool(tool)
