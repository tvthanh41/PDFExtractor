from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QRubberBand
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QWheelEvent, QMouseEvent
from PySide6.QtCore import Qt, Signal, QRect, QPoint, QRectF
import pymupdf as fitz
from typing import Optional

class PdfCanvasWidget(QGraphicsView):
    # Signal emitted when a bounding box is selected (x_pct, y_pct, w_pct, h_pct)
    box_selected = Signal(float, float, float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        
        self.document: Optional[fitz.Document] = None
        self.current_page = 0
        self.pixmap_item: Optional[QGraphicsPixmapItem] = None
        self.zoom_factor = 1.0
        self.highlight_item = None
        
        # Rubberband for selection
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.is_selecting = False
        self.is_rubber_band_mode = False

    def toggle_selection_mode(self, enabled: bool):
        self.is_rubber_band_mode = enabled
        if enabled:
            self.setDragMode(QGraphicsView.NoDrag)
            self.setCursor(Qt.CrossCursor)
        else:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.setCursor(Qt.ArrowCursor)

    def load_document(self, file_path: str):
        self.document = fitz.open(file_path)
        self.current_page = 0
        self.render_page()

    def highlight_box(self, box):
        from PySide6.QtWidgets import QGraphicsRectItem
        from PySide6.QtGui import QPen, QBrush
        
        if self.highlight_item:
            self.scene.removeItem(self.highlight_item)
            self.highlight_item = None
            
        if not box or not self.pixmap_item:
            return
            
        rect = self.pixmap_item.boundingRect()
        x = box.x_pct * rect.width()
        y = box.y_pct * rect.height()
        w = box.width_pct * rect.width()
        h = box.height_pct * rect.height()
        
        self.highlight_item = QGraphicsRectItem(x, y, w, h)
        pen = QPen(QColor(255, 0, 0, 255))
        pen.setWidth(2)
        self.highlight_item.setPen(pen)
        brush = QBrush(QColor(255, 0, 0, 50))
        self.highlight_item.setBrush(brush)
        self.scene.addItem(self.highlight_item)

    def render_page(self):
        if not self.document:
            return
            
        page = self.document[self.current_page]
        # render page to image
        zoom_matrix = fitz.Matrix(self.zoom_factor * 2, self.zoom_factor * 2) # high dpi
        pix = page.get_pixmap(matrix=zoom_matrix)
        
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        qpixmap = QPixmap.fromImage(img)
        
        if self.pixmap_item:
            self.scene.removeItem(self.pixmap_item)
            
        self.pixmap_item = self.scene.addPixmap(qpixmap)
        self.scene.setSceneRect(QRectF(qpixmap.rect()))

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_factor *= 1.2
            else:
                self.zoom_factor /= 1.2
            self.render_page()
            event.accept()
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if self.is_rubber_band_mode and event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, self.origin))
            self.rubber_band.show()
            self.is_selecting = True
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_selecting:
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.is_selecting:
            self.is_selecting = False
            self.rubber_band.hide()
            
            # Map coordinates to scene
            scene_rect = self.mapToScene(self.rubber_band.geometry()).boundingRect()
            
            if self.pixmap_item:
                pixmap_rect = self.pixmap_item.boundingRect()
                
                # Calculate percentages
                x_pct = scene_rect.x() / pixmap_rect.width()
                y_pct = scene_rect.y() / pixmap_rect.height()
                w_pct = scene_rect.width() / pixmap_rect.width()
                h_pct = scene_rect.height() / pixmap_rect.height()
                
                # constrain to 0-1
                x_pct = max(0.0, min(1.0, x_pct))
                y_pct = max(0.0, min(1.0, y_pct))
                w_pct = max(0.0, min(1.0, w_pct))
                h_pct = max(0.0, min(1.0, h_pct))
                
                self.box_selected.emit(x_pct, y_pct, w_pct, h_pct)
        else:
            super().mouseReleaseEvent(event)
