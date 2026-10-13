"""
ui/widgets/topology_widget.py
3 Düğümlü Mesh Ağ Topolojisi ve Sekme (Multi-Hop) Görselleştiricisi
Çoklu Tema Uyumlu
"""

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from models.node_manager import NodeManager, NodeState


class NodeCardWidget(QWidget):
    """Tek bir düğümün durumunu gösteren bilgi kartı."""

    def __init__(self, node_id: int, title: str, subtitle: str, parent=None):
        super().__init__(parent)
        self.node_id = node_id
        self.title = title
        self.subtitle = subtitle
        self.is_light_theme = False

        self.setObjectName("NodeCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        # Başlık ve Çevrimiçi Göstergesi
        header_layout = QHBoxLayout()
        self.lbl_status_dot = QLabel("●")
        self.lbl_status_dot.setStyleSheet("color: #64748B; font-size: 16px;")
        
        self.lbl_title = QLabel(self.title)
        self.lbl_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        
        header_layout.addWidget(self.lbl_status_dot)
        header_layout.addWidget(self.lbl_title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Alt Başlık / Rol
        self.lbl_sub = QLabel(self.subtitle)
        self.lbl_sub.setStyleSheet("color: #94A3B8; font-size: 11px;")
        layout.addWidget(self.lbl_sub)

        # Pil ve Son Görülme
        self.lbl_battery = QLabel("Pil: -- %")
        self.lbl_battery.setStyleSheet("color: #0284C7; font-size: 12px; font-weight: 600;")
        layout.addWidget(self.lbl_battery)

        self.lbl_last_seen = QLabel("Sinyal: Bekleniyor")
        self.lbl_last_seen.setStyleSheet("color: #64748B; font-size: 11px;")
        layout.addWidget(self.lbl_last_seen)

        self._apply_base_style()

    def set_theme(self, is_light: bool):
        self.is_light_theme = is_light
        self._apply_base_style()

    def _apply_base_style(self):
        bg = "#F8FAFC" if self.is_light_theme else "#0F172A"
        border = "#CBD5E1" if self.is_light_theme else "#334155"
        self.setStyleSheet(f"""
            QWidget#NodeCard {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 8px;
            }}
        """)

    def update_state(self, state: NodeState):
        bg = "#F8FAFC" if self.is_light_theme else "#0F172A"
        if state.is_online:
            if state.is_alarm_active:
                self.lbl_status_dot.setStyleSheet("color: #EF4444; font-size: 16px;")
                alarm_bg = "#FEE2E2" if self.is_light_theme else "#3B0764"
                self.setStyleSheet(f"""
                    QWidget#NodeCard {{
                        background-color: {alarm_bg};
                        border: 2px solid #EF4444;
                        border-radius: 8px;
                    }}
                """)
            else:
                self.lbl_status_dot.setStyleSheet("color: #10B981; font-size: 16px;")
                self.setStyleSheet(f"""
                    QWidget#NodeCard {{
                        background-color: {bg};
                        border: 1px solid #10B981;
                        border-radius: 8px;
                    }}
                """)
            self.lbl_battery.setText(f"Pil: %{state.battery}")
            self.lbl_last_seen.setText(f"Son Sinyal: {int(state.time_since_last_seen)} sn önce")
        else:
            self.lbl_status_dot.setStyleSheet("color: #64748B; font-size: 16px;")
            self._apply_base_style()
            self.lbl_last_seen.setText("Çevrimdışı")


class RouteDiagramWidget(QWidget):
    """Sekme (Hop) rotasını gösteren dinamik çizim alanı."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_hop = 1
        self.is_light_theme = False
        self.setMinimumHeight(55)

    def set_hop(self, hop: int):
        if self.current_hop != hop:
            self.current_hop = hop
            self.update()

    def set_theme(self, is_light: bool):
        self.is_light_theme = is_light
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        mid_y = h // 2

        painter.setFont(QFont("Segoe UI", 11, QFont.Bold))

        if self.current_hop == 1:
            line_color = QColor("#059669") if self.is_light_theme else QColor("#10B981")
            painter.setPen(QPen(line_color, 3, Qt.DashLine))
            painter.drawLine(50, mid_y, w - 50, mid_y)
            painter.setPen(line_color)
            painter.drawText(0, 0, w, h, Qt.AlignCenter, "⚡ 1 SEKME (DOĞRUDAN LORA HATTI)")
        else:
            line_color = QColor("#0284C7") if self.is_light_theme else QColor("#38BDF8")
            painter.setPen(QPen(line_color, 3, Qt.SolidLine))
            painter.drawLine(50, mid_y, w // 2, mid_y - 12)
            painter.drawLine(w // 2, mid_y - 12, w - 50, mid_y)
            painter.setPen(line_color)
            painter.drawText(0, 0, w, h, Qt.AlignCenter, "🔄 2 SEKME (RÖLE AKTARIMLI MESH)")


class TopologyWidget(QGroupBox):
    """Ana Ağ Topoloji Paneli."""

    def __init__(self, node_manager: NodeManager, parent=None):
        super().__init__("🛰️ ÇOK SEKME (MULTI-HOP) LORA MESH TOPOLOJİSİ", parent)
        self.node_manager = node_manager

        layout = QVBoxLayout(self)

        cards_layout = QHBoxLayout()
        self.card_rubble = NodeCardWidget(1, "Enkaz Düğümü #1", "Uç Sensör / Akustik")
        self.card_relay = NodeCardWidget(2, "Röle Düğümü #2", "Aktarıcı / Mesh")
        self.card_gateway = NodeCardWidget(3, "AFAD Gateway #3", "Merkez Koordinasyon")

        cards_layout.addWidget(self.card_rubble)
        cards_layout.addWidget(self.card_relay)
        cards_layout.addWidget(self.card_gateway)
        layout.addLayout(cards_layout)

        self.route_diagram = RouteDiagramWidget()
        layout.addWidget(self.route_diagram)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_ui)
        self.timer.start(1000)

    def set_theme(self, is_light: bool):
        self.card_rubble.set_theme(is_light)
        self.card_relay.set_theme(is_light)
        self.card_gateway.set_theme(is_light)
        self.route_diagram.set_theme(is_light)

    def refresh_ui(self):
        node1 = self.node_manager.get_node(1)
        node2 = self.node_manager.get_node(2)
        node3 = self.node_manager.get_node(3)

        if node1:
            self.card_rubble.update_state(node1)
            self.route_diagram.set_hop(node1.hop_count)
        if node2:
            self.card_relay.update_state(node2)
        if node3:
            self.card_gateway.update_state(node3)
