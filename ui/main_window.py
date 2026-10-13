"""
ui/main_window.py
Modern Web / SaaS Dashboard Hissiyatlı AFAD İzleme İstasyonu Ana Penceresi
Burdur Mehmet Akif Ersoy Üniversitesi (MAKÜ) Logosu Tam Ortada Entegre Edilmiştir.
"""

import os
import random
import socket
import time
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
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
from core.telemetry_protocol import MessageType, NodeRole, TelemetryPacket
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
        self.resize(1360, 880)

        # 1. Veri Modeli ve Alıcı İş Parçacığı
        self.node_manager = NodeManager()
        self.receiver = TelemetryReceiverThread(mode="UDP", udp_port=5005)
        self.latest_raw_hex = ""

        # Dahili Simülasyon Değişkenleri
        self.sim_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sim_running = False
        self.sim_hop = 1
        self.sim_battery = 96
        self.sim_timer = QTimer(self)
        self.sim_timer.timeout.connect(self._send_auto_heartbeat)

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
        main_layout.setContentsMargins(14, 10, 14, 12)
        main_layout.setSpacing(10)

        # 1. Modern Web Navbar (MAKÜ Logosu Tam Ortada)
        main_layout.addWidget(self._create_top_navbar())

        # 2. Hızlı Test & Senaryo Çubuğu
        main_layout.addWidget(self._create_scenario_bar())

        # 3. Ana Gövde (Splitter: Sol Göstergeler / Sağ Tablo & Alarmlar)
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

        splitter.setSizes([520, 840])
        main_layout.addWidget(splitter, 1)

        # 4. Durum Çubuğu
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
        """Modern Web Dashboard Header / Navbar (MAKÜ Logosu Tam Ortada)."""
        navbar = QFrame()
        navbar.setObjectName("TopNavBar")
        navbar.setFixedHeight(86)

        layout = QHBoxLayout(navbar)
        layout.setContentsMargins(18, 6, 18, 6)
        layout.setSpacing(14)

        # 1. SOL KISIM: AFAD Rozeti ve Başlık (Stretch = 1)
        brand_layout = QHBoxLayout()
        brand_layout.setSpacing(12)
        brand_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        icon_lbl = QLabel("🚨")
        icon_lbl.setStyleSheet("font-size: 26px;")
        brand_layout.addWidget(icon_lbl)

        title_vbox = QVBoxLayout()
        title_vbox.setSpacing(2)
        title_lbl = QLabel("AFAD MESH OPERASYON MERKEZİ")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; letter-spacing: 0.5px;")
        
        sub_lbl = QLabel("Çok Sekmeli LoRa Mesh & Uçta Akustik Enkaz Tespit Sistemi")
        sub_lbl.setStyleSheet("font-size: 11px; color: #94A3B8; font-weight: 500;")
        
        title_vbox.addWidget(title_lbl)
        title_vbox.addWidget(sub_lbl)
        brand_layout.addLayout(title_vbox)
        layout.addLayout(brand_layout, 1)

        # 2. ORTA KISIM: MAKÜ LOGOSU (TAM GEOMETRİK ORTA, SIFIR BOZULMA)
        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        self.logo_lbl = QLabel()
        self.logo_lbl.setAlignment(Qt.AlignCenter)
        self.logo_lbl.setToolTip("Burdur Mehmet Akif Ersoy Üniversitesi (MAKÜ) | Lisans Tezi")

        # Logoyu assets dizininden yükle (Önce yuvarlatılmış saydam png, yoksa orijinal jpeg)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(project_root, "assets", "maku_logo_circle.png")
        if not os.path.exists(logo_path):
            logo_path = os.path.join(project_root, "assets", "maku_logo.jpeg")

        if os.path.exists(logo_path):
            pix = QPixmap(logo_path)
            if not pix.isNull():
                # En-boy oranını bozmadan, pürüzsüz (SmoothTransformation) ölçekleme
                scaled_pix = pix.scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_lbl.setPixmap(scaled_pix)
                self.logo_lbl.setFixedSize(74, 74)
                self.logo_lbl.setStyleSheet("background: transparent;")
        else:
            self.logo_lbl.setText("🏛️ MAKÜ")
            self.logo_lbl.setStyleSheet("font-size: 20px; font-weight: bold;")

        center_layout.addWidget(self.logo_lbl)
        layout.addLayout(center_layout, 0)

        # 3. SAĞ KISIM: Bağlantı Hızlı Kontrolleri, Tema ve TÜBİTAK Rozeti (Stretch = 1)
        right_container = QHBoxLayout()
        right_container.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        right_container.setSpacing(10)

        right_container.addWidget(QLabel("Giriş:"))
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["UDP Soket (Simülatör)", "Seri Port (USB Gateway)"])
        self.combo_mode.currentIndexChanged.connect(self._on_mode_changed)
        right_container.addWidget(self.combo_mode)

        self.lbl_port = QLabel("Port:")
        right_container.addWidget(self.lbl_port)
        self.spin_port = QSpinBox()
        self.spin_port.setRange(1024, 65535)
        self.spin_port.setValue(5005)
        right_container.addWidget(self.spin_port)

        self.edit_serial = QLineEdit("COM3")
        self.edit_serial.setMaximumWidth(80)
        self.edit_serial.setVisible(False)
        right_container.addWidget(self.edit_serial)

        self.btn_toggle_conn = QPushButton("Durdur")
        self.btn_toggle_conn.setObjectName("btn_disconnect")
        self.btn_toggle_conn.clicked.connect(self._toggle_connection)
        right_container.addWidget(self.btn_toggle_conn)

        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet("color: #334155; margin: 4px 4px;")
        right_container.addWidget(sep)

        right_container.addWidget(QLabel("🎨"))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(list(THEMES.keys()))
        self.combo_theme.currentTextChanged.connect(self.on_theme_changed)
        right_container.addWidget(self.combo_theme)

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
        right_container.addWidget(badge)

        layout.addLayout(right_container, 1)
        return navbar

    def _create_scenario_bar(self) -> QFrame:
        """Kullanıcının tek tıklamayla sistemi test edebileceği Hızlı Senaryo Çubuğu."""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border: 1px solid #1F2937;
                border-radius: 10px;
            }
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(10)

        lbl = QLabel("⚡ HIZLI TEST:")
        lbl.setStyleSheet("font-weight: 800; color: #F59E0B; font-size: 12px;")
        layout.addWidget(lbl)

        self.btn_auto_sim = QPushButton("▶ Canlı Simülasyonu Başlat")
        self.btn_auto_sim.setStyleSheet("background-color: #059669; color: white; font-weight: 700; padding: 6px 14px; border-radius: 6px;")
        self.btn_auto_sim.clicked.connect(self._toggle_internal_sim)
        layout.addWidget(self.btn_auto_sim)

        self.btn_whistle_test = QPushButton("🚨 Düdük Alarmı Bas (2950 Hz)")
        self.btn_whistle_test.setStyleSheet("background-color: #B91C1C; color: white; font-weight: 700; padding: 6px 14px; border-radius: 6px;")
        self.btn_whistle_test.clicked.connect(self._send_test_whistle)
        layout.addWidget(self.btn_whistle_test)

        self.btn_seismic_test = QPushButton("💥 Sismik Çökme Bas (75°)")
        self.btn_seismic_test.setStyleSheet("background-color: #B45309; color: white; font-weight: 700; padding: 6px 14px; border-radius: 6px;")
        self.btn_seismic_test.clicked.connect(self._send_test_seismic)
        layout.addWidget(self.btn_seismic_test)

        self.btn_hop_test = QPushButton("🔄 Sekme Değiştir (1 ↔ 2 Hop)")
        self.btn_hop_test.setStyleSheet("background-color: #1E293B; color: #38BDF8; font-weight: 700; padding: 6px 14px; border-radius: 6px;")
        self.btn_hop_test.clicked.connect(self._toggle_test_hop)
        layout.addWidget(self.btn_hop_test)

        layout.addStretch()

        hint = QLabel("💡 Harici 'mock_telemetry.py' veya gerçek LoRa Gateway verileri de eşzamanlı dinlenir.")
        hint.setStyleSheet("color: #64748B; font-size: 11px;")
        layout.addWidget(hint)

        return frame

    def _toggle_internal_sim(self):
        self.sim_running = not self.sim_running
        if self.sim_running:
            self.btn_auto_sim.setText("⏸️ Simülasyonu Durdur")
            self.btn_auto_sim.setStyleSheet("background-color: #DC2626; color: white; font-weight: 700; padding: 6px 14px; border-radius: 6px;")
            self._send_auto_heartbeat()
            self.sim_timer.start(2000)
        else:
            self.btn_auto_sim.setText("▶ Canlı Simülasyonu Başlat")
            self.btn_auto_sim.setStyleSheet("background-color: #059669; color: white; font-weight: 700; padding: 6px 14px; border-radius: 6px;")
            self.sim_timer.stop()

    def _send_udp_packet(self, pkt: TelemetryPacket):
        raw = pkt.pack()
        try:
            self.sim_socket.sendto(raw, ("127.0.0.1", self.spin_port.value()))
        except Exception as e:
            self.status_bar.showMessage(f"Simülasyon gönderim hatası: {e}", 3000)

    def _send_auto_heartbeat(self):
        pitch = random.randint(-4, 4)
        roll = random.randint(-3, 3)
        if random.random() < 0.1 and self.sim_battery > 10:
            self.sim_battery -= 1

        pkt = TelemetryPacket(
            node_id=NodeRole.RUBBLE_NODE,
            msg_type=MessageType.HEARTBEAT,
            pitch=pitch,
            roll=roll,
            peak_freq=0,
            confidence=0,
            hop_count=self.sim_hop,
            battery=self.sim_battery,
        )
        self._send_udp_packet(pkt)

    def _send_test_whistle(self):
        pkt = TelemetryPacket(
            node_id=NodeRole.RUBBLE_NODE,
            msg_type=MessageType.ACOUSTIC_ALARM,
            pitch=random.randint(-6, 6),
            roll=random.randint(-4, 4),
            peak_freq=random.randint(2850, 3100),
            confidence=random.randint(93, 99),
            hop_count=self.sim_hop,
            battery=self.sim_battery,
        )
        self._send_udp_packet(pkt)

    def _send_test_seismic(self):
        pkt = TelemetryPacket(
            node_id=NodeRole.RUBBLE_NODE,
            msg_type=MessageType.SEISMIC_ALERT,
            pitch=random.choice([65, 75, -78]),
            roll=random.choice([48, -52, 64]),
            peak_freq=0,
            confidence=100,
            hop_count=self.sim_hop,
            battery=self.sim_battery,
        )
        self._send_udp_packet(pkt)

    def _toggle_test_hop(self):
        self.sim_hop = 2 if self.sim_hop == 1 else 1
        self._send_auto_heartbeat()
        self.status_bar.showMessage(f"Sekme Durumu Değiştirildi: {self.sim_hop} Hop", 3000)

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
        self.topology_widget.on_packet_arrived(pkt.hop_count)

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
        self.sim_timer.stop()
        self.receiver.stop()
        self.sim_socket.close()
        event.accept()
