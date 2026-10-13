"""
ui/widgets/alarm_panel.py
Modern Web Bildirim Kartı Hissiyatlı Acil Durum Alarm Paneli
"""

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import (
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class AlarmPanelWidget(QGroupBox):
    alarm_cleared = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("🚨 ACİL DURUM VE AKUSTİK TESPİT ALARMI", parent)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Ana Alarm Bildirim Kartı
        self.banner = QFrame()
        self.banner.setStyleSheet("""
            QFrame {
                background-color: #0B1120;
                border: 1px solid #1F2937;
                border-radius: 10px;
                padding: 14px;
            }
        """)
        banner_layout = QVBoxLayout(self.banner)
        banner_layout.setSpacing(6)

        self.lbl_headline = QLabel("🛡️ SİSTEM DEVREDE: ENKAZDA AKUSTİK BELİRTİ ARANIYOR")
        self.lbl_headline.setStyleSheet("color: #10B981; font-weight: 800; font-size: 15px;")
        self.lbl_headline.setAlignment(Qt.AlignCenter)
        banner_layout.addWidget(self.lbl_headline)

        self.lbl_details = QLabel("Dinlenen Frekanslar: Düdük (2.5 - 3.5 kHz) | Ritmik Vuruş (< 500 Hz)")
        self.lbl_details.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 500;")
        self.lbl_details.setAlignment(Qt.AlignCenter)
        banner_layout.addWidget(self.lbl_details)

        layout.addWidget(self.banner)

        # Kontrol Satırı
        btn_layout = QHBoxLayout()
        self.lbl_active_pill = QLabel("AKTİF ALARM YOK")
        self.lbl_active_pill.setStyleSheet("""
            background-color: #1E293B;
            color: #94A3B8;
            font-size: 11px;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 12px;
        """)
        btn_layout.addWidget(self.lbl_active_pill)
        btn_layout.addStretch()

        self.btn_clear = QPushButton("🔕 Alarmı Sustur / Onayla")
        self.btn_clear.setObjectName("btn_clear_alarm")
        self.btn_clear.clicked.connect(self.on_clear_clicked)
        btn_layout.addWidget(self.btn_clear)
        layout.addLayout(btn_layout)

        # Flaş Zamanlayıcısı
        self.flash_state = False
        self.is_flashing = False
        self.flash_timer = QTimer(self)
        self.flash_timer.timeout.connect(self._toggle_flash)

    def trigger_acoustic_alarm(self, freq: int, confidence: int, node_id: int):
        is_whistle = 2000 <= freq <= 4000
        tip_str = "DÜDÜK SESİ" if is_whistle else "RİTMİK VURUŞ"

        self.lbl_headline.setText(f"🚨 DÜĞÜM #{node_id}: {tip_str} TESPİT EDİLDİ!")
        self.lbl_details.setText(f"Baskın Frekans: {freq} Hz  |  Algılama Güveni: %{confidence}  |  ACİL MÜDAHALE GEREKLİ!")
        
        self.lbl_active_pill.setText("🚨 1 ACİL ALARM")
        self.lbl_active_pill.setStyleSheet("""
            background-color: #EF4444;
            color: #FFFFFF;
            font-size: 11px;
            font-weight: 800;
            padding: 6px 14px;
            border-radius: 12px;
        """)

        self._start_flashing()

    def trigger_seismic_alert(self, pitch: int, roll: int, node_id: int):
        self.lbl_headline.setText(f"💥 DÜĞÜM #{node_id}: ENKAZ ÇÖKMESİ TESPİT EDİLDİ!")
        self.lbl_details.setText(f"Kritik Eğim / Sensör Devrildi: Eğim (X): {pitch}°, Yatma (Y): {roll}°")
        
        self.lbl_active_pill.setText("💥 1 SİSMİK UYARI")
        self.lbl_active_pill.setStyleSheet("""
            background-color: #F59E0B;
            color: #FFFFFF;
            font-size: 11px;
            font-weight: 800;
            padding: 6px 14px;
            border-radius: 12px;
        """)

        self._start_flashing()

    def _start_flashing(self):
        if not self.is_flashing:
            self.is_flashing = True
            self.flash_timer.start(500)

    def _toggle_flash(self):
        self.flash_state = not self.flash_state
        if self.flash_state:
            self.banner.setStyleSheet("""
                QFrame {
                    background-color: #7F1D1D;
                    border: 2px solid #EF4444;
                    border-radius: 10px;
                    padding: 14px;
                }
            """)
        else:
            self.banner.setStyleSheet("""
                QFrame {
                    background-color: #450A0A;
                    border: 2px solid #DC2626;
                    border-radius: 10px;
                    padding: 14px;
                }
            """)

    def on_clear_clicked(self):
        self.flash_timer.stop()
        self.is_flashing = False
        self.banner.setStyleSheet("""
            QFrame {
                background-color: #0B1120;
                border: 1px solid #1F2937;
                border-radius: 10px;
                padding: 14px;
            }
        """)
        self.lbl_headline.setText("🛡️ SİSTEM DEVREDE: TEHLİKE YOK")
        self.lbl_headline.setStyleSheet("color: #10B981; font-weight: 800; font-size: 15px;")
        self.lbl_details.setText("Alarm operatör tarafından onaylandı ve sıfırlandı.")
        self.lbl_active_pill.setText("AKTİF ALARM YOK")
        self.lbl_active_pill.setStyleSheet("""
            background-color: #1E293B;
            color: #94A3B8;
            font-size: 11px;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 12px;
        """)
        self.alarm_cleared.emit()
