"""
ui/main_window.py
AFAD İzleme İstasyonu Ana Pencere Mimari Orkestratörü
Çoklu Renk Temaları Destekli (Koyu / Mavi / Beyaz)
"""

import time
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from core.receiver import TelemetryReceiverThread
from core.telemetry_protocol import MessageType, TelemetryPacket
from models.node_manager import NodeManager
from ui.styles import THEMES, get_theme_qss
from ui.widgets import (
    AlarmPanelWidget,
    SeismicGaugeWidget,
    TelemetryTableWidget,
    TopologyWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AFAD | Afet Sonrası Çok Sekmeli LoRa Mesh & Akustik İzleme İstasyonu v1.0")
        self.resize(1300, 820)

        # 1. Veri Modeli ve Alıcı İş Parçacığı
        self.node_manager = NodeManager()
        self.receiver = TelemetryReceiverThread(mode="UDP", udp_port=5005)
        self.latest_raw_hex = ""

        # 2. Arayüz Bileşenlerini Kur
        self._init_ui()

        # 3. Sinyal / Yuva (Signal/Slot) Bağlantıları
        self._connect_signals()

        # 4. Varsayılan Olarak UDP Alıcısını Başlat
        self.start_receiver()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(12)

        # Üst Başlık ve Tema / Bağlantı Çubuğu
        main_layout.addLayout(self._create_header_layout())
        main_layout.addLayout(self._create_connection_bar())

        # Ana Gövde (Splitter: Sol Göstergeler / Sağ Tablo ve Alarmlar)
        splitter = QSplitter(Qt.Horizontal)

        # Sol Panel (Topoloji ve Sismik İbre)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        self.topology_widget = TopologyWidget(self.node_manager)
        self.seismic_widget = SeismicGaugeWidget()

        left_layout.addWidget(self.topology_widget)
        left_layout.addWidget(self.seismic_widget)
        splitter.addWidget(left_widget)

        # Sağ Panel (Acil Durum Paneli ve Canlı Telemetri Tablosu)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        self.alarm_panel = AlarmPanelWidget()
        self.table_widget = TelemetryTableWidget()

        right_layout.addWidget(self.alarm_panel)
        right_layout.addWidget(self.table_widget)
        splitter.addWidget(right_widget)

        splitter.setSizes([480, 820])
        main_layout.addWidget(splitter)

        # Durum Çubuğu (Status Bar)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.lbl_status_mode = QLabel("Durum: Başlatılıyor...")
        self.lbl_clock = QLabel(time.strftime("%d.%m.%Y %H:%M:%S"))
        self.status_bar.addWidget(self.lbl_status_mode, 1)
        self.status_bar.addPermanentWidget(self.lbl_clock)

        # Saat Güncelleme Zamanlayıcısı
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(lambda: self.lbl_clock.setText(time.strftime("%d.%m.%Y %H:%M:%S")))
        self.clock_timer.start(1000)

    def _create_header_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title = QLabel("T.C. İÇİŞLERİ BAKANLIĞI AFAD & MAKÜ BİLGİSAYAR MÜHENDİSLİĞİ")
        title.setStyleSheet("color: #0284C7; font-weight: bold; font-size: 11px; letter-spacing: 1px;")
        
        subtitle = QLabel("AFET SONRASI ALTYAPISIZ ÇOK SEKME (MULTI-HOP) LORA MESH & AKUSTİK İZLEME PANELİ")
        subtitle.setStyleSheet("font-weight: 800; font-size: 16px;")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        layout.addLayout(title_layout)
        layout.addStretch()

        # Tema Seçici Açılır Kutu
        layout.addWidget(QLabel("🎨 Tema:"))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(list(THEMES.keys()))
        self.combo_theme.currentTextChanged.connect(self.on_theme_changed)
        layout.addWidget(self.combo_theme)

        badge = QLabel("PROJE TEZİ v1.0 | TÜBİTAK 2209-A")
        badge.setStyleSheet("background-color: #1E293B; color: #94A3B8; padding: 6px 12px; border-radius: 6px; font-weight: bold;")
        layout.addWidget(badge)

        return layout

    def _create_connection_bar(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(10)

        layout.addWidget(QLabel("Bağlantı Kaynağı:"))
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["UDP Soket (Simülatör)", "Seri Port (USB Gateway)"])
        self.combo_mode.currentIndexChanged.connect(self._on_mode_changed)
        layout.addWidget(self.combo_mode)

        self.lbl_port = QLabel("UDP Port:")
        layout.addWidget(self.lbl_port)
        self.spin_port = QSpinBox()
        self.spin_port.setRange(1024, 65535)
        self.spin_port.setValue(5005)
        layout.addWidget(self.spin_port)

        self.edit_serial = QLineEdit("COM3")
        self.edit_serial.setMaximumWidth(80)
        self.edit_serial.setVisible(False)
        layout.addWidget(self.edit_serial)

        self.btn_toggle_conn = QPushButton("Durdur")
        self.btn_toggle_conn.setObjectName("btn_disconnect")
        self.btn_toggle_conn.clicked.connect(self._toggle_connection)
        layout.addWidget(self.btn_toggle_conn)

        layout.addStretch()
        return layout

    def on_theme_changed(self, theme_name: str):
        """Kullanıcı tema seçtiğinde tüm uygulamayı anında güncelle."""
        qss = get_theme_qss(theme_name)
        app = QApplication.instance()
        if app:
            app.setStyleSheet(qss)

        is_light = "Beyaz" in theme_name or "Gündüz" in theme_name
        self.topology_widget.set_theme(is_light)
        self.seismic_widget.set_theme(is_light)
        self.table_widget.set_theme(is_light)

    def _on_mode_changed(self, idx: int):
        is_udp = (idx == 0)
        self.lbl_port.setText("UDP Port:" if is_udp else "Seri Port:")
        self.spin_port.setVisible(is_udp)
        self.edit_serial.setVisible(not is_udp)

    def _connect_signals(self):
        self.receiver.packet_received.connect(self.on_packet_received)
        self.receiver.raw_packet_hex.connect(self.on_raw_hex_received)
        self.receiver.status_changed.connect(self.on_status_changed)
        self.receiver.error_occurred.connect(lambda err: self.status_bar.showMessage(f"Hata: {err}", 4000))
        self.alarm_panel.alarm_cleared.connect(self.on_alarm_cleared)

    def start_receiver(self):
        if self.combo_mode.currentIndex() == 0:
            self.receiver.configure_udp(self.spin_port.value())
        else:
            self.receiver.configure_serial(self.edit_serial.text().strip())

        self.receiver.start()
        self.btn_toggle_conn.setText("Durdur")
        self.btn_toggle_conn.setObjectName("btn_disconnect")
        self.btn_toggle_conn.setStyleSheet("")

    def stop_receiver(self):
        self.receiver.stop()
        self.btn_toggle_conn.setText("Başlat")
        self.btn_toggle_conn.setObjectName("btn_connect")
        self.btn_toggle_conn.setStyleSheet("")

    def _toggle_connection(self):
        if self.receiver.isRunning():
            self.stop_receiver()
        else:
            self.start_receiver()

    def on_raw_hex_received(self, hex_str: str):
        self.latest_raw_hex = hex_str

    def on_packet_received(self, pkt: TelemetryPacket, source_desc: str):
        updated_node = self.node_manager.update_with_packet(pkt)

        if pkt.node_id == 1:
            self.seismic_widget.update_angles(pkt.pitch, pkt.roll)

        if pkt.msg_type == MessageType.ACOUSTIC_ALARM:
            self.alarm_panel.trigger_acoustic_alarm(pkt.peak_freq, pkt.confidence, pkt.node_id)
        elif pkt.msg_type == MessageType.SEISMIC_ALERT:
            self.alarm_panel.trigger_seismic_alert(pkt.pitch, pkt.roll, pkt.node_id)

        self.table_widget.add_packet(pkt, self.latest_raw_hex)

    def on_status_changed(self, is_connected: bool, message: str):
        self.lbl_status_mode.setText(f"Bağlantı: {message}")
        if is_connected:
            self.lbl_status_mode.setStyleSheet("color: #10B981; font-weight: bold;")
        else:
            self.lbl_status_mode.setStyleSheet("color: #EF4444; font-weight: bold;")

    def on_alarm_cleared(self):
        self.node_manager.clear_node_alarm(1)
        self.node_manager.clear_node_alarm(2)

    def closeEvent(self, event):
        self.receiver.stop()
        event.accept()
