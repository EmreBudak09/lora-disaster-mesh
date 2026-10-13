"""
Afet Sonrası Altyapısız Arama-Kurtarma İçin Çok Sekmeli (Multi-Hop) LoRa Mesh ve Uçta Akustik Tespit Sistemi
Ortak Telemetri İkili (Binary) Protokol Modülü (v1.0)

Paket Yapısı (11 Bayt - Little Endian):
| Bayt | Tip     | Alan        | Açıklama                                       |
|------|---------|-------------|------------------------------------------------|
| 0    | uint8   | header      | Sabit 0xAA                                     |
| 1    | uint8   | node_id     | 1: Enkaz, 2: Röle, 3: Gateway                   |
| 2    | uint8   | msg_type    | 1: Periyodik/Canlı, 2: Düdük/Vuruş, 3: Sismik  |
| 3    | int8    | pitch       | -90 .. +90 derece                              |
| 4    | int8    | roll        | -90 .. +90 derece                              |
| 5..6 | uint16  | peak_freq   | 0 .. 5000 Hz (Düdük ~2500-3500 Hz)             |
| 7    | uint8   | confidence  | 0 .. 100 (%)                                   |
| 8    | uint8   | hop_count   | Sekme sayısı (TTL / Mesh takibi)               |
| 9    | uint8   | battery     | Pil yüzdesi (0 .. 100)                         |
| 10   | uint8   | checksum    | İlk 10 baytın XOR kontrolü                     |
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

    def calculate_checksum(self, raw_bytes_10: bytes) -> int:
        """İlk 10 baytın XOR toplamını hesaplar."""
        chk = 0
        for b in raw_bytes_10:
            chk ^= b
        return chk

    def pack(self) -> bytes:
        """Paketi 11 baytlık ikili (binary) veriye dönüştürür."""
        # İlk 10 baytı paketle
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
        # Checksum hesapla ve 11. bayt olarak ekle
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
        chk_hesaplanan = 0
        for b in data[:10]:
            chk_hesaplanan ^= b

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


if __name__ == "__main__":
    # Kendi kendine birim testi (Unit Test)
    test_pkt = TelemetryPacket(
        node_id=NodeRole.RUBBLE_NODE,
        msg_type=MessageType.ACOUSTIC_ALARM,
        pitch=-12,
        roll=5,
        peak_freq=2950,
        confidence=94,
        hop_count=1,
        battery=88,
    )
    binary_data = test_pkt.pack()
    print(f"Oluşturulan Paket ({len(binary_data)} Bayt): {binary_data.hex(' ')}")
    
    cozulen = TelemetryPacket.unpack(binary_data)
    print(f"Çözülen Paket: {cozulen}")
    assert cozulen.peak_freq == 2950
    assert cozulen.confidence == 94
    print("[OK] Protokol birim testi basariyla gecti!")
