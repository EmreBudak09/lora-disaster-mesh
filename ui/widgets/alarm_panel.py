"""
ui/widgets/alarm_panel.py
Acil Durum, Akustik Düdük ve Ritmik Vuruş Alarm Paneli
"""

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AlarmPanelWidget(QGroupBox):
    alarm_cleared = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("🚨 ACİL DURUM VE AKUSTİK TESPİT ALARMI", parent)

        layout = QVBoxLayout(self)

        # Ana Alarm Kutusu
        self.banner = QWidget()
        self.banner.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                border: 2px solid #334155;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        banner_layout = QVBoxLayout(self.banner)

        self.lbl_headline = QLabel("🛡️ SİSTEM HAZIR: ENKAZDA AKUSTİK BELİRTİ ARANIYOR")
        self.lbl_headline.setStyleSheet("color: #10B981; font-weight: bold; font-size: 14px;")
        self.lbl_headline.setAlignment(Qt.AlignCenter)
        banner_layout.addWidget(self.lbl_headline)

        self.lbl_details = QLabel("Beklenen frekans: Düdük (2.5 - 3.5 kHz) | Ritmik Darbe (< 500 Hz)")
        self.lbl_details.setStyleSheet("color: #94A3B8; font-size: 12px;")
        self.lbl_details.setAlignment(Qt.AlignCenter)
        banner_layout.addWidget(self.lbl_details)

        layout.addWidget(self.banner)

        # Kontrol ve Sıfırlama Butonu
        btn_layout = QHBoxLayout()
        self.lbl_active_count = QLabel("Aktif Alarm: 0")
        self.lbl_active_count.setStyleSheet("color: #64748B; font-weight: bold;")
        btn_layout.addWidget(self.lbl_active_count)
        btn_layout.addStretch()

        self.btn_clear = QPushButton("Alarmı Sustur / Onayla")
        self.btn_clear.setObjectName("btn_clear_alarm")
        self.btn_clear.clicked.connect(self.on_clear_clicked)
        btn_layout.addWidget(self.btn_clear)
        layout.addLayout(btn_layout)

        # Flaş Efekti Zamanlayıcısı
        self.flash_state = False
        self.is_flashing = False
        self.flash_timer = QTimer(self)
        self.flash_timer.timeout.connect(self._toggle_flash)

    def trigger_acoustic_alarm(self, freq: int, confidence: int, node_id: int):
        """Düdük veya ritmik darbe alarmı tetikler."""
        is_whistle = 2000 <= freq <= 4000
        tip_str = "DÜDÜK SESİ" if is_whistle else "RİTMİK VURUŞ"

        self.lbl_headline.setText(f"🚨 DÜĞÜM #{node_id}: {tip_str} TESPİT EDİLDİ!")
        self.lbl_details.setText(f"Baskın Frekans: {freq} Hz | Tespit Güveni: %{confidence} | CANLI BELİRTİSİ!")
        self.lbl_active_count.setText("Aktif Alarm: 1 (ACİL)")
        self.lbl_active_count.setStyleSheet("color: #EF4444; font-weight: bold;")

        self._start_flashing()

    def trigger_seismic_alert(self, pitch: int, roll: int, node_id: int):
        """Sismik çökme uyarısı tetikler."""
        self.lbl_headline.setText(f"💥 DÜĞÜM #{node_id}: ENKAZ ÇÖKMESİ TESPİT EDİLDİ!")
        self.lbl_details.setText(f"Aşırı Eğim / Sensör Devrildi: Pitch: {pitch}°, Roll: {roll}°")
        self.lbl_active_count.setText("Aktif Alarm: 1 (SİSMİK)")
        self.lbl_active_count.setStyleSheet("color: #F59E0B; font-weight: bold;")

        self._start_flashing()

    def _start_flashing(self):
        if not self.is_flashing:
            self.is_flashing = True
            self.flash_timer.start(500)

    def _toggle_flash(self):
        self.flash_state = not self.flash_state
        if self.flash_state:
            self.banner.setStyleSheet("""
                QWidget {
                    background-color: #7F1D1D;
                    border: 2px solid #EF4444;
                    border-radius: 8px;
                    padding: 12px;
                }
            """)
        else:
            self.banner.setStyleSheet("""
                QWidget {
                    background-color: #450A0A;
                    border: 2px solid #DC2626;
                    border-radius: 8px;
                    padding: 12px;
                }
            """)

    def on_clear_clicked(self):
        self.flash_timer.stop()
        self.is_flashing = False
        self.banner.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                border: 2px solid #334155;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        self.lbl_headline.setText("🛡️ SİSTEM DEVREDE: TEHLİKE YOK")
        self.lbl_headline.setStyleSheet("color: #10B981; font-weight: bold; font-size: 14px;")
        self.lbl_details.setText("Alarm operatör tarafından onaylandı ve sıfırlandı.")
        self.lbl_active_count.setText("Aktif Alarm: 0")
        self.lbl_active_count.setStyleSheet("color: #64748B; font-weight: bold;")
        self.alarm_cleared.emit()
