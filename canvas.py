from PyQt5.QtWidgets import QWidget, QInputDialog, QFontDialog, QFileDialog
from PyQt5.QtCore import Qt, QPoint, QBuffer, QRect
from PyQt5.QtGui import QPainter, QPen, QImage, QColor, QBrush, QFont, QLinearGradient, QPolygon
import random
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from PyQt5.QtWidgets import QInputDialog
import numpy as np
import io

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize colors before init_canvas
        self.primary_color = Qt.black
        self.secondary_color = Qt.white
        self.brush_color = self.primary_color
        self.init_canvas()
        self.undo_stack = []
        self.redo_stack = []
        self.save_to_undo_stack()

    def init_canvas(self):
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.last_point = QPoint()
        self.drawing = False
        
        # Drawing settings
        self.brush_size = 3
        self.brush_color = self.primary_color
        self.current_tool = "brush"
        self.start_pos = None
        self.temp_image = None
        self.text_font = QFont('Arial', 12)
        self.tools = {
            "brush": self.draw_brush_line,
            "eraser": self.draw_eraser_line,
            "spray": self.draw_spray_effect,
            "line": self.draw_line_shape,
            "rectangle": self.draw_rectangle_shape,
            "circle": self.draw_circle_shape,
            "fill": self.flood_fill,
            "text": self.draw_text,
            "gradient": self.draw_gradient,
            "polygon": self.draw_polygon,
            "selection": self.make_selection
        }

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            new_image = QImage(self.size(), QImage.Format_RGB32)
            new_image.fill(Qt.white)
            painter = QPainter(new_image)
            painter.drawImage(QPoint(0, 0), self.image)
            self.image = new_image

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.brush_color = self.primary_color
        elif event.button() == Qt.RightButton:
            self.brush_color = self.secondary_color
            
        # Now handle the tool actions
        if self.current_tool == "polygon":
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size))
            self.draw_polygon(painter, event)
            self.update()
            return
            
        if event.button() in [Qt.LeftButton, Qt.RightButton]:
            self.drawing = True
            self.last_point = event.pos()
            self.start_pos = event.pos()
            
            if self.current_tool in ["line", "rectangle", "circle", "gradient", "selection"]:
                self.temp_image = self.image.copy()
            elif self.current_tool == "fill":
                self.flood_fill(event.pos())
            elif self.current_tool == "text":
                text, ok = QInputDialog.getText(self, 'Text Tool', 'Enter text:')
                if ok and text:
                    painter = QPainter(self.image)
                    self.draw_text(painter, event.pos(), text)
                    self.update()

    def mouseMoveEvent(self, event):
        if not self.drawing or (not event.buttons() & (Qt.LeftButton | Qt.RightButton)):
            return
            
        if self.current_tool in ["line", "rectangle", "circle", "gradient", "selection"]:
            self.image = self.temp_image.copy()
            
        painter = QPainter(self.image)
        
        # Set brush color based on which mouse button is pressed
        if event.buttons() & Qt.RightButton:
            self.brush_color = self.secondary_color
        elif event.buttons() & Qt.LeftButton:
            self.brush_color = self.primary_color
        
        if self.current_tool == "brush":
            self.draw_brush_line(painter, self.last_point, event.pos())
        elif self.current_tool == "eraser":
            self.draw_eraser_line(painter, self.last_point, event.pos())
        elif self.current_tool == "spray":
            self.draw_spray_effect(painter, event.pos())
        elif self.current_tool == "line":
            self.draw_line_shape(painter, self.start_pos, event.pos())
        elif self.current_tool == "rectangle":
            self.draw_rectangle_shape(painter, self.start_pos, event.pos())
        elif self.current_tool == "circle":
            self.draw_circle_shape(painter, self.start_pos, event.pos())
        elif self.current_tool == "gradient":
            gradient = QLinearGradient(self.start_pos, event.pos())
            gradient.setColorAt(0, self.brush_color)
            gradient.setColorAt(1, Qt.transparent)
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.NoPen)
            painter.drawRect(QRect(self.start_pos, event.pos()).normalized())
        elif self.current_tool == "selection":
            painter.setPen(QPen(Qt.black, 1, Qt.DashLine))
            painter.drawRect(QRect(self.start_pos, event.pos()).normalized())
        
        self.last_point = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() in [Qt.LeftButton, Qt.RightButton]:
            self.drawing = False
            self.save_to_undo_stack()  # Save state after each draw

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

    def set_color(self, color):
        self.brush_color = color

    def set_tool(self, tool):
        self.current_tool = tool

    def set_brush_size(self, size):
        self.brush_size = size

    def flood_fill(self, pos):
        target_color = self.image.pixelColor(pos)
        if target_color == self.brush_color:
            return

        stack = [pos]
        while stack:
            current = stack.pop()
            x, y = current.x(), current.y()
            
            if (x < 0 or x >= self.image.width() or 
                y < 0 or y >= self.image.height()):
                continue
                
            if self.image.pixelColor(x, y) != target_color:
                continue

            self.image.setPixelColor(x, y, self.brush_color)
            
            stack.append(QPoint(x + 1, y))
            stack.append(QPoint(x - 1, y))
            stack.append(QPoint(x, y + 1))
            stack.append(QPoint(x, y - 1))
        
        self.update()

    def save_to_undo_stack(self):
        self.undo_stack.append(self.image.copy())
        self.redo_stack.clear()
        if len(self.undo_stack) > 20:  # Limit stack size
            self.undo_stack.pop(0)

    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.image = self.undo_stack[-1].copy()
            self.update()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.image = self.undo_stack[-1].copy()
            self.update()

    def new_canvas(self):
        self.image.fill(Qt.white)
        self.save_to_undo_stack()
        self.update()

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", 
                                                 "PNG Files (*.png);;JPG Files (*.jpg);;All Files (*.*)")
        if file_path:
            self.image.save(file_path)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                 "PNG Files (*.png);;JPG Files (*.jpg);;All Files (*.*)")
        if file_path:
            self.image.load(file_path)
            self.image = self.image.scaled(self.size(), Qt.KeepAspectRatio)
            self.save_to_undo_stack()
            self.update()

    def apply_filter(self, filter_name):
        # Convert QImage to PIL Image
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        self.image.save(buffer, "PNG")
        pil_image = Image.open(io.BytesIO(buffer.data()))
        
        if filter_name == 'blur':
            pil_image = pil_image.filter(ImageFilter.BLUR)
        elif filter_name == 'sharpen':
            pil_image = pil_image.filter(ImageFilter.SHARPEN)
        elif filter_name == 'grayscale':
            pil_image = pil_image.convert('L').convert('RGB')
        elif filter_name == 'invert':
            pil_image = ImageOps.invert(pil_image)
        elif filter_name == 'brightness':
            factor, ok = QInputDialog.getDouble(self, 'Brightness',
                                              'Enter brightness factor (0.0-2.0):',
                                              1.0, 0.0, 2.0, 2)
            if ok:
                pil_image = ImageEnhance.Brightness(pil_image).enhance(factor)
        elif filter_name == 'contrast':
            factor, ok = QInputDialog.getDouble(self, 'Contrast',
                                              'Enter contrast factor (0.0-2.0):',
                                              1.0, 0.0, 2.0, 2)
            if ok:
                pil_image = ImageEnhance.Contrast(pil_image).enhance(factor)

        # Convert back to QImage
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        self.image.loadFromData(buffer.getvalue())
        self.save_to_undo_stack()
        self.update()

    def draw_gradient(self, painter, event):
        gradient = QLinearGradient(self.start_pos, event.pos())
        gradient.setColorAt(0, self.brush_color)
        gradient.setColorAt(1, Qt.transparent)
        painter.setBrush(gradient)
        painter.drawRect(QRect(self.start_pos, event.pos()).normalized())

    def draw_polygon(self, painter, event):
        if not hasattr(self, 'polygon_points'):
            self.polygon_points = []
            
        if event.button() == Qt.LeftButton:
            self.polygon_points.append(event.pos())
            if len(self.polygon_points) > 2:
                points = [QPoint(p.x(), p.y()) for p in self.polygon_points]
                painter.drawPolygon(QPolygon(points))
        elif event.button() == Qt.RightButton:
            # Complete polygon on right click
            if len(self.polygon_points) > 2:
                points = [QPoint(p.x(), p.y()) for p in self.polygon_points]
                painter.drawPolygon(QPolygon(points))
            self.polygon_points = []  # Reset points for next polygon

    def make_selection(self, painter, event):
        if not self.temp_image:
            self.temp_image = self.image.copy()
        painter.drawRect(QRect(self.start_pos, event.pos()).normalized())

    def draw_brush_line(self, painter, start, end):
        painter.setPen(QPen(self.brush_color, self.brush_size, 
                          Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(start, end)

    def draw_eraser_line(self, painter, start, end):
        painter.setPen(QPen(Qt.white, self.brush_size, 
                          Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(start, end)

    def draw_spray_effect(self, painter, pos):
        painter.setPen(QPen(self.brush_color, 1))
        for _ in range(20):
            xo = int(random.gauss(0, self.brush_size))
            yo = int(random.gauss(0, self.brush_size))
            painter.drawPoint(int(pos.x() + xo), int(pos.y() + yo))

    def draw_line_shape(self, painter, start, end):
        painter.setPen(QPen(self.brush_color, self.brush_size))
        painter.drawLine(start, end)

    def draw_rectangle_shape(self, painter, start, end):
        painter.setPen(QPen(self.brush_color, self.brush_size))
        painter.drawRect(QRect(start, end).normalized())

    def draw_circle_shape(self, painter, start, end):
        painter.setPen(QPen(self.brush_color, self.brush_size))
        painter.drawEllipse(QRect(start, end).normalized())

    def draw_text(self, painter, pos, text):
        painter.setPen(QPen(self.brush_color))
        painter.setFont(self.text_font)
        painter.drawText(pos, text)

    def set_primary_color(self, color):
        self.primary_color = color
        if self.brush_color == self.primary_color:  # Update current brush color if it was primary
            self.brush_color = color

    def set_secondary_color(self, color):
        self.secondary_color = color
        if self.brush_color == self.secondary_color:  # Update current brush color if it was secondary
            self.brush_color = color
