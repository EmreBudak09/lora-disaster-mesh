"""
core/telemetry_protocol.py
11-Baytlık İkili Telemetri Protokol Motoru (v1.0)
"""

import struct
from dataclasses import dataclass
from enum import IntEnum

HEADER_BYTE = 0xAA
PACKET_SIZE = 11
STRUCT_FORMAT = "<BBBbbHBBB"  # Son Checksum hariç ilk 10 bayt


class MessageType(IntEnum):
    HEARTBEAT = 0x01      # Normal durum / Yaşam sinyali
    ACOUSTIC_ALARM = 0x02 # Düdük veya ritmik vuruş tespiti
    SEISMIC_ALERT = 0x03  # Enkaz çökme / aşırı eğim tespiti


class NodeRole(IntEnum):
    RUBBLE_NODE = 0x01    # Enkaz Altı Düğümü
    RELAY_NODE = 0x02     # Röle / Aktarıcı Düğümü
    GATEWAY_NODE = 0x03   # AFAD Gateway / Koordinasyon Merkezi


@dataclass
class TelemetryPacket:
    node_id: int
    msg_type: MessageType
    pitch: int
    roll: int
    peak_freq: int
    confidence: int
    hop_count: int
    battery: int

    @staticmethod
    def calculate_checksum(raw_bytes_10: bytes) -> int:
        """İlk 10 baytın XOR toplamını hesaplar."""
        chk = 0
        for b in raw_bytes_10:
            chk ^= b
        return chk

    def pack(self) -> bytes:
        """Paketi 11 baytlık ikili (binary) veriye dönüştürür."""
        raw_10 = struct.pack(
            STRUCT_FORMAT,
            HEADER_BYTE,
            int(self.node_id),
            int(self.msg_type),
            int(self.pitch),
            int(self.roll),
            int(self.peak_freq),
            int(self.confidence),
            int(self.hop_count),
            int(self.battery),
        )
        checksum = self.calculate_checksum(raw_10)
        return raw_10 + struct.pack("<B", checksum)

    @classmethod
    def unpack(cls, data: bytes):
        """11 baytlık ikili veriyi TelemetryPacket nesnesine dönüştürür."""
        if len(data) != PACKET_SIZE:
            raise ValueError(f"Hatalı paket boyutu: {len(data)} bayt (Beklenen: {PACKET_SIZE})")

        header, node_id, msg_type, pitch, roll, peak_freq, confidence, hop_count, battery = struct.unpack(
            STRUCT_FORMAT, data[:10]
        )

        if header != HEADER_BYTE:
            raise ValueError(f"Geçersiz paket başlığı: {hex(header)} (Beklenen: {hex(HEADER_BYTE)})")

        checksum_gelen = data[10]
        chk_hesaplanan = cls.calculate_checksum(data[:10])

        if checksum_gelen != chk_hesaplanan:
            raise ValueError(
                f"Checksum hatası! Gelen: {checksum_gelen}, Hesaplanan: {chk_hesaplanan}"
            )

        return cls(
            node_id=node_id,
            msg_type=MessageType(msg_type),
            pitch=pitch,
            roll=roll,
            peak_freq=peak_freq,
            confidence=confidence,
            hop_count=hop_count,
            battery=battery,
        )
