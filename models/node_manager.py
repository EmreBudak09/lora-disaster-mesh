"""
models/node_manager.py
Ağdaki Düğümlerin Durum Yönetimi ve Olay Takibi
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from core.telemetry_protocol import MessageType, NodeRole, TelemetryPacket


@dataclass
class NodeState:
    node_id: int
    name: str = ""
    role: NodeRole = NodeRole.RUBBLE_NODE
    battery: int = 100
    pitch: int = 0
    roll: int = 0
    peak_freq: int = 0
    confidence: int = 0
    hop_count: int = 1
    last_msg_type: MessageType = MessageType.HEARTBEAT
    last_seen_timestamp: float = 0.0
    packet_count: int = 0
    is_alarm_active: bool = False
    alarm_description: str = ""

    @property
    def is_online(self) -> bool:
        """Son 12 saniye içinde veri geldiyse düğüm çevrimiçidir."""
        if self.last_seen_timestamp == 0.0:
            return False
        return (time.time() - self.last_seen_timestamp) < 12.0

    @property
    def time_since_last_seen(self) -> float:
        if self.last_seen_timestamp == 0.0:
            return 999.0
        return max(0.0, time.time() - self.last_seen_timestamp)


class NodeManager:
    def __init__(self):
        self.nodes: Dict[int, NodeState] = {}
        self.alarm_history: List[dict] = []
        self._initialize_default_nodes()

    def _initialize_default_nodes(self):
        """Formdaki 3 ana düğümü başlangıçta tanımlar."""
        self.nodes[1] = NodeState(
            node_id=1,
            name="Enkaz Düğümü #1",
            role=NodeRole.RUBBLE_NODE,
            battery=95,
        )
        self.nodes[2] = NodeState(
            node_id=2,
            name="Röle Düğümü #2",
            role=NodeRole.RELAY_NODE,
            battery=100,
        )
        self.nodes[3] = NodeState(
            node_id=3,
            name="AFAD Gateway #3",
            role=NodeRole.GATEWAY_NODE,
            battery=100,
        )

    def get_node(self, node_id: int) -> Optional[NodeState]:
        return self.nodes.get(node_id)

    def update_with_packet(self, pkt: TelemetryPacket) -> NodeState:
        """Gelen telemetri paketine göre düğüm durumunu günceller."""
        if pkt.node_id not in self.nodes:
            # Yeni keşfedilen düğüm
            role = NodeRole(pkt.node_id) if pkt.node_id in [1, 2, 3] else NodeRole.RUBBLE_NODE
            self.nodes[pkt.node_id] = NodeState(
                node_id=pkt.node_id,
                name=f"Düğüm #{pkt.node_id}",
                role=role,
            )

        node = self.nodes[pkt.node_id]
        node.battery = pkt.battery
        node.pitch = pkt.pitch
        node.roll = pkt.roll
        node.peak_freq = pkt.peak_freq
        node.confidence = pkt.confidence
        node.hop_count = pkt.hop_count
        node.last_msg_type = pkt.msg_type
        node.last_seen_timestamp = time.time()
        node.packet_count += 1

        # Alarm kontrolü
        if pkt.msg_type == MessageType.ACOUSTIC_ALARM:
            node.is_alarm_active = True
            desc = f"Akustik Tespit: {pkt.peak_freq} Hz (%{pkt.confidence})"
            node.alarm_description = desc
            self._log_alarm(node.node_id, "AKUSTİK ALARM", desc)
        elif pkt.msg_type == MessageType.SEISMIC_ALERT:
            node.is_alarm_active = True
            desc = f"Sismik Çökme: Eğim {pkt.pitch}° / {pkt.roll}°"
            node.alarm_description = desc
            self._log_alarm(node.node_id, "SİSMİK ÇÖKME", desc)
        else:
            # Normal kalp atışında eğer alarm manuel sıfırlanmadıysa bir süre sonra sönsün
            pass

        return node

    def clear_node_alarm(self, node_id: int):
        """Alarmı operatör tarafından sıfırlar."""
        if node_id in self.nodes:
            self.nodes[node_id].is_alarm_active = False
            self.nodes[node_id].alarm_description = ""

    def _log_alarm(self, node_id: int, alarm_type: str, detail: str):
        record = {
            "time": time.strftime("%H:%M:%S"),
            "node_id": node_id,
            "type": alarm_type,
            "detail": detail,
        }
        self.alarm_history.insert(0, record)
        # Maksimum 100 alarm kaydı tut
        if len(self.alarm_history) > 100:
            self.alarm_history.pop()
