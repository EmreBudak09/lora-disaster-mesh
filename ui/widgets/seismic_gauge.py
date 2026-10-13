"""
ui/widgets/seismic_gauge.py
Modern Dijital Kokpit / HUD Hissiyatlı MPU-6050 Sismik Eğim İbresi
"""

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen
from PyQt5.QtWidgets import QFrame, QGroupBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class BubbleLevelCanvas(QWidget):
    """QPainter tabanlı modern 2D eğim dairesi."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pitch = 0
        self.roll = 0
        self.is_light_theme = False
        self.setMinimumSize(190, 190)

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
        radius = min(w, h) // 2 - 12
        center = QPointF(w / 2, h / 2)

        # 1. Dış Çember
        bg_color = QColor("#FFFFFF") if self.is_light_theme else QColor("#0B1120")
        border_color = QColor("#CBD5E1") if self.is_light_theme else QColor("#1F2937")
        
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

        # 3. Kesişen Artı Çizgisi (Crosshair)
        cross_color = QColor("#CBD5E1") if self.is_light_theme else QColor("#334155")
        painter.setPen(QPen(cross_color, 1))
        painter.drawLine(int(center.x() - radius), int(center.y()), int(center.x() + radius), int(center.y()))
        painter.drawLine(int(center.x()), int(center.y() - radius), int(center.x()), int(center.y() + radius))

        # 4. Eğim Kabarcığı
        offset_x = (self.roll / 90.0) * radius
        offset_y = -(self.pitch / 90.0) * radius

        bubble_center = QPointF(center.x() + offset_x, center.y() + offset_y)
        bubble_radius = 13

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
        self.is_light_theme = False

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Çizim Alanı
        self.canvas = BubbleLevelCanvas()
        layout.addWidget(self.canvas, alignment=Qt.AlignCenter)

        # Sayısal Değerler Kartı (2'li Yan Yana)
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(10)

        self.card_pitch = QFrame()
        self.card_pitch.setStyleSheet("background-color: #0B1120; border: 1px solid #1F2937; border-radius: 8px; padding: 6px;")
        pitch_box = QVBoxLayout(self.card_pitch)
        pitch_box.setContentsMargins(8, 4, 8, 4)
        lbl_p_title = QLabel("EĞİM (PITCH)")
        lbl_p_title.setStyleSheet("font-size: 10px; color: #64748B; font-weight: 700;")
        self.lbl_pitch_val = QLabel("0°")
        self.lbl_pitch_val.setStyleSheet("font-size: 18px; color: #38BDF8; font-weight: 800;")
        pitch_box.addWidget(lbl_p_title)
        pitch_box.addWidget(self.lbl_pitch_val)
        cards_layout.addWidget(self.card_pitch)

        self.card_roll = QFrame()
        self.card_roll.setStyleSheet("background-color: #0B1120; border: 1px solid #1F2937; border-radius: 8px; padding: 6px;")
        roll_box = QVBoxLayout(self.card_roll)
        roll_box.setContentsMargins(8, 4, 8, 4)
        lbl_r_title = QLabel("YATMA (ROLL)")
        lbl_r_title.setStyleSheet("font-size: 10px; color: #64748B; font-weight: 700;")
        self.lbl_roll_val = QLabel("0°")
        self.lbl_roll_val.setStyleSheet("font-size: 18px; color: #38BDF8; font-weight: 800;")
        roll_box.addWidget(lbl_r_title)
        roll_box.addWidget(self.lbl_roll_val)
        cards_layout.addWidget(self.card_roll)

        layout.addLayout(cards_layout)

        # Durum Hapı (Status Pill)
        self.lbl_status = QLabel("✅ DURUM: STABİL / NORMAL")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet("""
            background-color: #064E3B;
            color: #10B981;
            font-size: 12px;
            font-weight: 700;
            padding: 8px;
            border-radius: 8px;
        """)
        layout.addWidget(self.lbl_status)

    def set_theme(self, is_light: bool):
        self.is_light_theme = is_light
        self.canvas.set_theme(is_light)
        bg = "#FFFFFF" if is_light else "#0B1120"
        border = "#E2E8F0" if is_light else "#1F2937"
        self.card_pitch.setStyleSheet(f"background-color: {bg}; border: 1px solid {border}; border-radius: 8px; padding: 6px;")
        self.card_roll.setStyleSheet(f"background-color: {bg}; border: 1px solid {border}; border-radius: 8px; padding: 6px;")

    def update_angles(self, pitch: int, roll: int):
        self.canvas.set_angles(pitch, roll)
        self.lbl_pitch_val.setText(f"{pitch}°")
        self.lbl_roll_val.setText(f"{roll}°")

        total_tilt = (pitch**2 + roll**2)**0.5
        if total_tilt > 45:
            self.lbl_status.setText("💥 SİSMİK ÇÖKME / ENKAZ DEVRİLMESİ!")
            self.lbl_status.setStyleSheet("background-color: #EF4444; color: #FFFFFF; font-size: 12px; font-weight: 800; padding: 8px; border-radius: 8px;")
        elif total_tilt > 25:
            self.lbl_status.setText("⚠️ TEHLİKELİ EĞİM / ARTÇI SARSINTI")
            self.lbl_status.setStyleSheet("background-color: #F59E0B; color: #FFFFFF; font-size: 12px; font-weight: 800; padding: 8px; border-radius: 8px;")
        else:
            self.lbl_status.setText("✅ DURUM: STABİL / NORMAL")
            self.lbl_status.setStyleSheet("background-color: #064E3B; color: #10B981; font-size: 12px; font-weight: 700; padding: 8px; border-radius: 8px;")
