"""
ui/widgets/seismic_gauge.py
MPU-6050 Sismik Eğim ve Çökme Analiz İbresi (Yapay Ufuk / Çift Eksenli Su Terazisi)
Çoklu Tema Uyumlu
"""

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class BubbleLevelCanvas(QWidget):
    """QPainter tabanlı 2D eğim dairesi."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pitch = 0
        self.roll = 0
        self.is_light_theme = False
        self.setMinimumSize(180, 180)

    def set_theme(self, is_light: bool):
        self.is_light_theme = is_light
        self.update()

    def set_angles(self, pitch: int, roll: int):
        self.pitch = max(-90, min(90, pitch))
        self.roll = max(-90, min(90, roll))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        radius = min(w, h) // 2 - 15
        center = QPointF(w / 2, h / 2)

        # 1. Arka Plan Çemberi
        bg_color = QColor("#F8FAFC") if self.is_light_theme else QColor("#0F172A")
        border_color = QColor("#CBD5E1") if self.is_light_theme else QColor("#334155")
        
        painter.setPen(QPen(border_color, 2))
        painter.setBrush(QBrush(bg_color))
        painter.drawEllipse(center, radius, radius)

        # 2. Güvenli Eşik Çemberleri (25° ve 45°)
        r_safe = radius * (25 / 90)
        painter.setPen(QPen(QColor("#10B981"), 1, Qt.DashLine))
        painter.drawEllipse(center, r_safe, r_safe)

        r_warn = radius * (45 / 90)
        painter.setPen(QPen(QColor("#EF4444"), 1, Qt.DashLine))
        painter.drawEllipse(center, r_warn, r_warn)

        # 3. Kesişen Artı Göstergesi (Crosshair)
        cross_color = QColor("#94A3B8") if self.is_light_theme else QColor("#475569")
        painter.setPen(QPen(cross_color, 1))
        painter.drawLine(int(center.x() - radius), int(center.y()), int(center.x() + radius), int(center.y()))
        painter.drawLine(int(center.x()), int(center.y() - radius), int(center.x()), int(center.y() + radius))

        # 4. Eğim Kabarcığı (Bubble Indicator)
        offset_x = (self.roll / 90.0) * radius
        offset_y = -(self.pitch / 90.0) * radius

        bubble_center = QPointF(center.x() + offset_x, center.y() + offset_y)
        bubble_radius = 12

        total_tilt = (self.pitch**2 + self.roll**2)**0.5
        if total_tilt > 45:
            bubble_color = QColor("#EF4444")
        elif total_tilt > 25:
            bubble_color = QColor("#F59E0B")
        else:
            bubble_color = QColor("#0284C7") if self.is_light_theme else QColor("#38BDF8")

        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(QBrush(bubble_color))
        painter.drawEllipse(bubble_center, bubble_radius, bubble_radius)


class SeismicGaugeWidget(QGroupBox):
    """Sismik Yıkım ve Eğim Gösterge Paneli."""

    def __init__(self, parent=None):
        super().__init__("📐 SİSMİK EĞİM VE ÇÖKME İBRESİ (MPU-6050)", parent)

        layout = QVBoxLayout(self)

        self.canvas = BubbleLevelCanvas()
        layout.addWidget(self.canvas, alignment=Qt.AlignCenter)

        values_layout = QHBoxLayout()
        self.lbl_pitch = QLabel("Pitch (X): 0°")
        self.lbl_pitch.setStyleSheet("font-weight: bold; color: #0284C7; font-size: 13px;")
        
        self.lbl_roll = QLabel("Roll (Y): 0°")
        self.lbl_roll.setStyleSheet("font-weight: bold; color: #0284C7; font-size: 13px;")
        
        values_layout.addWidget(self.lbl_pitch)
        values_layout.addWidget(self.lbl_roll)
        layout.addLayout(values_layout)

        self.lbl_status = QLabel("DURUM: STABİL / NORMAL")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet("color: #10B981; font-weight: bold; font-size: 12px; padding: 4px;")
        layout.addWidget(self.lbl_status)

    def set_theme(self, is_light: bool):
        self.canvas.set_theme(is_light)

    def update_angles(self, pitch: int, roll: int):
        self.canvas.set_angles(pitch, roll)
        self.lbl_pitch.setText(f"Pitch (X): {pitch}°")
        self.lbl_roll.setText(f"Roll (Y): {roll}°")

        total_tilt = (pitch**2 + roll**2)**0.5
        if total_tilt > 45:
            self.lbl_status.setText("💥 SİSMİK ÇÖKME / ENKAZ DEVRİLMESİ!")
            self.lbl_status.setStyleSheet("color: #FFFFFF; background-color: #EF4444; border-radius: 4px; font-weight: bold;")
        elif total_tilt > 25:
            self.lbl_status.setText("⚠️ TEHLİKELİ EĞİM / ARTÇI SARSINTI")
            self.lbl_status.setStyleSheet("color: #FFFFFF; background-color: #F59E0B; border-radius: 4px; font-weight: bold;")
        else:
            self.lbl_status.setText("✅ DURUM: STABİL / NORMAL")
            self.lbl_status.setStyleSheet("color: #10B981; font-weight: bold;")
