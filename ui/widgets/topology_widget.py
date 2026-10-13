"""
ui/widgets/topology_widget.py
Modern Web Dashboard Hissiyatlı Çok Sekmeli LoRa Mesh Topoloji Kartları
"""

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QFrame, QGroupBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget
from models.node_manager import NodeManager, NodeState


class NodeCardWidget(QFrame):
    """Modern SaaS Metrik Kartı Görünümünde Düğüm Paneli."""

    def __init__(self, node_id: int, title: str, subtitle: str, icon: str, parent=None):
        super().__init__(parent)
        self.node_id = node_id
        self.title = title
        self.subtitle = subtitle
        self.icon_str = icon
        self.is_light_theme = False

        self.setObjectName("NodeCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        # Üst Satır: İkon, Başlık ve Çevrimiçi Hap (Pill) Rozeti
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        icon_lbl = QLabel(self.icon_str)
        icon_lbl.setStyleSheet("font-size: 18px;")
        top_row.addWidget(icon_lbl)

        self.lbl_title = QLabel(self.title)
        self.lbl_title.setStyleSheet("font-weight: 700; font-size: 14px;")
        top_row.addWidget(self.lbl_title)
        top_row.addStretch()

        self.lbl_status_pill = QLabel("ÇEVRİMDIŞI")
        self.lbl_status_pill.setStyleSheet("""
            background-color: #334155;
            color: #94A3B8;
            font-size: 10px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 10px;
        """)
        top_row.addWidget(self.lbl_status_pill)
        layout.addLayout(top_row)

        # Alt Satır / Rol Açıklaması
        self.lbl_sub = QLabel(self.subtitle)
        self.lbl_sub.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 500;")
        layout.addWidget(self.lbl_sub)

        # İstatistikler (Pil ve Son Sinyal)
        stats_layout = QHBoxLayout()
        self.lbl_battery = QLabel("🔋 Pil: -- %")
        self.lbl_battery.setStyleSheet("color: #0284C7; font-size: 13px; font-weight: 700;")
        
        self.lbl_last_seen = QLabel("⏱️ Bekleniyor")
        self.lbl_last_seen.setStyleSheet("color: #64748B; font-size: 11px;")
        
        stats_layout.addWidget(self.lbl_battery)
        stats_layout.addStretch()
        stats_layout.addWidget(self.lbl_last_seen)
        layout.addLayout(stats_layout)

        self._apply_base_style()

    def set_theme(self, is_light: bool):
        self.is_light_theme = is_light
        self._apply_base_style()

    def _apply_base_style(self):
        bg = "#FFFFFF" if self.is_light_theme else "#0B1120"
        border = "#E2E8F0" if self.is_light_theme else "#1F2937"
        self.setStyleSheet(f"""
            QFrame#NodeCard {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 10px;
            }}
        """)

    def update_state(self, state: NodeState):
        bg = "#FFFFFF" if self.is_light_theme else "#0B1120"
        if state.is_online:
            if state.is_alarm_active:
                alarm_bg = "#FEE2E2" if self.is_light_theme else "#450A0A"
                self.setStyleSheet(f"""
                    QFrame#NodeCard {{
                        background-color: {alarm_bg};
                        border: 2px solid #EF4444;
                        border-radius: 10px;
                    }}
                """)
                self.lbl_status_pill.setText("🚨 ALARM")
                self.lbl_status_pill.setStyleSheet("""
                    background-color: #EF4444;
                    color: #FFFFFF;
                    font-size: 10px;
                    font-weight: 800;
                    padding: 3px 8px;
                    border-radius: 10px;
                """)
            else:
                self.setStyleSheet(f"""
                    QFrame#NodeCard {{
                        background-color: {bg};
                        border: 1px solid #10B981;
                        border-radius: 10px;
                    }}
                """)
                self.lbl_status_pill.setText("● AKTİF")
                self.lbl_status_pill.setStyleSheet("""
                    background-color: #064E3B;
                    color: #10B981;
                    font-size: 10px;
                    font-weight: 700;
                    padding: 3px 8px;
                    border-radius: 10px;
                """)
            self.lbl_battery.setText(f"🔋 Pil: %{state.battery}")
            self.lbl_last_seen.setText(f"⏱️ {int(state.time_since_last_seen)}s önce")
        else:
            self._apply_base_style()
            self.lbl_status_pill.setText("KAPALI")
            self.lbl_status_pill.setStyleSheet("""
                background-color: #1E293B;
                color: #64748B;
                font-size: 10px;
                font-weight: 700;
                padding: 3px 8px;
                border-radius: 10px;
            """)
            self.lbl_last_seen.setText("Çevrimdışı")


class RouteDiagramWidget(QFrame):
    """Modern Sekme Rota Paneli."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_hop = 1
        self.is_light_theme = False
        self.setFixedHeight(54)
        self.setObjectName("RouteFrame")
        self._apply_style()

    def set_hop(self, hop: int):
        if self.current_hop != hop:
            self.current_hop = hop
            self.update()

    def set_theme(self, is_light: bool):
        self.is_light_theme = is_light
        self._apply_style()
        self.update()

    def _apply_style(self):
        bg = "#F1F5F9" if self.is_light_theme else "#0B1120"
        border = "#E2E8F0" if self.is_light_theme else "#1F2937"
        self.setStyleSheet(f"""
            QFrame#RouteFrame {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 8px;
            }}
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        mid_y = h // 2

        painter.setFont(QFont("Segoe UI", 12, QFont.Bold))

        if self.current_hop == 1:
            line_color = QColor("#059669") if self.is_light_theme else QColor("#10B981")
            painter.setPen(QPen(line_color, 2, Qt.DashLine))
            painter.drawLine(30, mid_y, w - 30, mid_y)
            painter.setPen(line_color)
            painter.drawText(0, 0, w, h, Qt.AlignCenter, "⚡ 1 SEKME (DOĞRUDAN KESİNTİSİZ LORA HATTI)")
        else:
            line_color = QColor("#0284C7") if self.is_light_theme else QColor("#38BDF8")
            painter.setPen(QPen(line_color, 3, Qt.SolidLine))
            painter.drawLine(30, mid_y, w // 2, mid_y - 10)
            painter.drawLine(w // 2, mid_y - 10, w - 30, mid_y)
            painter.setPen(line_color)
            painter.drawText(0, 0, w, h, Qt.AlignCenter, "🔄 2 SEKME (RÖLE AKTARIMLI AKILLI MESH)")


class TopologyWidget(QGroupBox):
    """Ana Ağ Topoloji Paneli."""

    def __init__(self, node_manager: NodeManager, parent=None):
        super().__init__("🛰️ ÇOK SEKME (MULTI-HOP) LORA MESH TOPOLOJİSİ", parent)
        self.node_manager = node_manager

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(10)
        self.card_rubble = NodeCardWidget(1, "Enkaz Düğümü #1", "Uç Sensör / Akustik", "🏚️")
        self.card_relay = NodeCardWidget(2, "Röle Düğümü #2", "Aktarıcı / Mesh", "📡")
        self.card_gateway = NodeCardWidget(3, "AFAD Gateway #3", "Merkez Koordinasyon", "🏢")

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
