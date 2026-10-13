"""
ui/main_window.py
Modern Web / SaaS Dashboard Hissiyatlı AFAD İzleme İstasyonu Ana Penceresi
"""

import time
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
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
        self.setWindowTitle("AFAD | Afet Sonrası Çok Sekmeli LoRa Mesh & Akustik İzleme Paneli")
        self.resize(1340, 840)

        # 1. Veri Modeli ve Alıcı İş Parçacığı
        self.node_manager = NodeManager()
        self.receiver = TelemetryReceiverThread(mode="UDP", udp_port=5005)
        self.latest_raw_hex = ""

        # 2. Arayüzü Kur
        self._init_ui()

        # 3. Sinyalleri Bağla
        self._connect_signals()

        # 4. Alıcıyı Başlat
        self.start_receiver()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(14, 12, 14, 12)
        main_layout.setSpacing(14)

        # 1. Modern Web Tarzı Üst Navigasyon Çubuğu (Navbar)
        main_layout.addWidget(self._create_top_navbar())

        # 2. Ana Gövde (Splitter: Sol Göstergeler / Sağ Tablo & Alarmlar)
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(4)

        # Sol Panel (Topoloji & Sismik İbre)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(14)

        self.topology_widget = TopologyWidget(self.node_manager)
        self.seismic_widget = SeismicGaugeWidget()

        left_layout.addWidget(self.topology_widget)
        left_layout.addWidget(self.seismic_widget)
        splitter.addWidget(left_widget)

        # Sağ Panel (Acil Durum Paneli & Canlı Telemetri Tablosu)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(14)

        self.alarm_panel = AlarmPanelWidget()
        self.table_widget = TelemetryTableWidget()

        right_layout.addWidget(self.alarm_panel)
        right_layout.addWidget(self.table_widget)
        splitter.addWidget(right_widget)

        splitter.setSizes([500, 840])
        main_layout.addWidget(splitter, 1)

        # 3. Durum Çubuğu
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.lbl_status_mode = QLabel("Bağlantı: Bekleniyor...")
        self.lbl_clock = QLabel(time.strftime("%d.%m.%Y %H:%M:%S"))
        self.status_bar.addWidget(self.lbl_status_mode, 1)
        self.status_bar.addPermanentWidget(self.lbl_clock)

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(lambda: self.lbl_clock.setText(time.strftime("%d.%m.%Y %H:%M:%S")))
        self.clock_timer.start(1000)

    def _create_top_navbar(self) -> QFrame:
        """Modern Web Dashboard Header / Navbar."""
        navbar = QFrame()
        navbar.setObjectName("TopNavBar")
        navbar.setFixedHeight(74)

        layout = QHBoxLayout(navbar)
        layout.setContentsMargins(18, 10, 18, 10)
        layout.setSpacing(14)

        # Sol: AFAD Rozeti ve Başlık
        brand_layout = QHBoxLayout()
        brand_layout.setSpacing(12)

        icon_lbl = QLabel("🚨")
        icon_lbl.setStyleSheet("font-size: 26px;")
        brand_layout.addWidget(icon_lbl)

        title_vbox = QVBoxLayout()
        title_vbox.setSpacing(2)
        title_lbl = QLabel("AFAD MESH OPERASYON MERKEZİ")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; letter-spacing: 0.5px;")
        
        sub_lbl = QLabel("Çok Sekmeli LoRa Mesh & Uçta Akustik Enkaz Tespit Sistemi | MAKÜ Bilgisayar Müh.")
        sub_lbl.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 500;")
        
        title_vbox.addWidget(title_lbl)
        title_vbox.addWidget(sub_lbl)
        brand_layout.addLayout(title_vbox)
        layout.addLayout(brand_layout)

        layout.addStretch()

        # Orta: Bağlantı Hızlı Kontrolleri (Pill Bar)
        conn_box = QHBoxLayout()
        conn_box.setSpacing(8)

        conn_box.addWidget(QLabel("Giriş:"))
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["UDP Soket (Simülatör)", "Seri Port (USB Gateway)"])
        self.combo_mode.currentIndexChanged.connect(self._on_mode_changed)
        conn_box.addWidget(self.combo_mode)

        self.lbl_port = QLabel("Port:")
        conn_box.addWidget(self.lbl_port)
        self.spin_port = QSpinBox()
        self.spin_port.setRange(1024, 65535)
        self.spin_port.setValue(5005)
        conn_box.addWidget(self.spin_port)

        self.edit_serial = QLineEdit("COM3")
        self.edit_serial.setMaximumWidth(80)
        self.edit_serial.setVisible(False)
        conn_box.addWidget(self.edit_serial)

        self.btn_toggle_conn = QPushButton("Durdur")
        self.btn_toggle_conn.setObjectName("btn_disconnect")
        self.btn_toggle_conn.clicked.connect(self._toggle_connection)
        conn_box.addWidget(self.btn_toggle_conn)

        layout.addLayout(conn_box)

        # Ayırıcı Çizgi
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet("color: #334155; margin: 4px 6px;")
        layout.addWidget(sep)

        # Sağ: Tema ve Rozet
        right_box = QHBoxLayout()
        right_box.setSpacing(10)

        right_box.addWidget(QLabel("🎨"))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(list(THEMES.keys()))
        self.combo_theme.currentTextChanged.connect(self.on_theme_changed)
        right_box.addWidget(self.combo_theme)

        badge = QLabel("TÜBİTAK 2209-A")
        badge.setStyleSheet("""
            background-color: #1E293B;
            border: 1px solid #334155;
            color: #38BDF8;
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        """)
        right_box.addWidget(badge)

        layout.addLayout(right_box)
        return navbar

    def on_theme_changed(self, theme_name: str):
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
        self.lbl_port.setText("Port:" if is_udp else "Seri:")
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
