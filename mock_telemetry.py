"""
Afet Sonrası Altyapısız Arama-Kurtarma İçin Çok Sekmeli (Multi-Hop) LoRa Mesh ve Uçta Akustik Tespit Sistemi
Sahte Veri Simülatörü (Mock Telemetry Generator) v1.0

Bu script, fiziksel ESP32 ve LoRa donanımları hazır olmasa bile:
1. AFAD İzleme İstasyonu arayüzünü (PyQt/PySide) canlı veriyle besler.
2. UDP soketi (varsayılan: 127.0.0.1:5005) veya Seri Port (COMx) üzerinden 11 baytlık standart telemetri basar.
3. Klavyeden anlık senaryo tetiklemeyi destekler (Düdük, Sismik Çökme, Röle Aktarımı).
"""

import argparse
import random
import socket
import sys
import threading
import time
from telemetry_protocol import MessageType, NodeRole, TelemetryPacket

# Windows konsolunda Türkçe karakterlerin düzgün görünmesi için
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach(), errors="replace")


class MockTelemetryGenerator:
    def __init__(self, target_ip="127.0.0.1", target_port=5005, serial_port=None, baudrate=115200):
        self.target_ip = target_ip
        self.target_port = target_port
        self.serial_port_name = serial_port
        self.baudrate = baudrate
        self.running = False
        self.auto_interval = 2.0  # saniye

        # Simülasyon Durum Değişkenleri
        self.battery = 98
        self.pitch = 2
        self.roll = -1
        self.active_node = NodeRole.RUBBLE_NODE
        self.active_hop = 1

        # Soket Kurulumu (UDP)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Seri Port Kurulumu (Opsiyonel)
        self.serial_conn = None
        if self.serial_port_name:
            try:
                import serial
                self.serial_conn = serial.Serial(self.serial_port_name, self.baudrate, timeout=1)
                print(f"[OK] Seri port acildi: {self.serial_port_name} @ {self.baudrate}")
            except Exception as e:
                print(f"[HATA] Seri port acilamadi: {e}. UDP uzerinden devam ediliyor.")

    def send_packet(self, packet: TelemetryPacket, tag=""):
        raw_bytes = packet.pack()

        # UDP ile gönder
        try:
            self.udp_socket.sendto(raw_bytes, (self.target_ip, self.target_port))
        except Exception as e:
            print(f"[HATA] UDP gonderim hatasi: {e}")

        # Seri Port ile gönder (varsa)
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(raw_bytes)
            except Exception as e:
                print(f"[HATA] Seri port gonderim hatasi: {e}")

        # Ekrana log bas
        freq_str = f"{packet.peak_freq} Hz" if packet.peak_freq > 0 else "Sessiz"
        print(
            f"[{time.strftime('%H:%M:%S')}] {tag:<16} | Düğüm: {packet.node_id} | "
            f"Tip: {packet.msg_type.name:<14} | Eğim: ({packet.pitch:3d}°, {packet.roll:3d}°) | "
            f"Frekans: {freq_str:<9} | Güven: %{packet.confidence:2d} | "
            f"Sekme: {packet.hop_count} | Pil: %{packet.battery:2d} | Hex: {raw_bytes.hex(' ')}"
        )

    def trigger_heartbeat(self):
        """Rastgele hafif gürültülü normal kalp atışı."""
        self.pitch = max(-90, min(90, self.pitch + random.randint(-1, 1)))
        self.roll = max(-90, min(90, self.roll + random.randint(-1, 1)))
        if random.random() < 0.1 and self.battery > 5:
            self.battery -= 1

        pkt = TelemetryPacket(
            node_id=self.active_node,
            msg_type=MessageType.HEARTBEAT,
            pitch=self.pitch,
            roll=self.roll,
            peak_freq=0,
            confidence=0,
            hop_count=self.active_hop,
            battery=self.battery,
        )
        self.send_packet(pkt, tag="[NORMAL]")

    def trigger_whistle_alarm(self):
        """Enkaz altından 2.5 - 3.2 kHz aralığında düdük alarmı."""
        whistle_freq = random.randint(2850, 3150)
        confidence = random.randint(92, 99)
        pkt = TelemetryPacket(
            node_id=NodeRole.RUBBLE_NODE,
            msg_type=MessageType.ACOUSTIC_ALARM,
            pitch=self.pitch,
            roll=self.roll,
            peak_freq=whistle_freq,
            confidence=confidence,
            hop_count=self.active_hop,
            battery=self.battery,
        )
        self.send_packet(pkt, tag="🚨 [DÜDÜK ALARMI]")

    def trigger_knocking_alarm(self):
        """Enkaz altında ritmik taş/çekiç vurma tespiti."""
        knock_freq = random.randint(150, 320)
        confidence = random.randint(85, 94)
        pkt = TelemetryPacket(
            node_id=NodeRole.RUBBLE_NODE,
            msg_type=MessageType.ACOUSTIC_ALARM,
            pitch=self.pitch,
            roll=self.roll,
            peak_freq=knock_freq,
            confidence=confidence,
            hop_count=self.active_hop,
            battery=self.battery,
        )
        self.send_packet(pkt, tag="🔨 [RİTMİK VURUŞ]")

    def trigger_seismic_collapse(self):
        """Bina yıkımı / sensör kutusunun devrilmesi (Ani yüksek eğim)."""
        self.pitch = random.choice([65, 75, -70, -82])
        self.roll = random.choice([45, -55, 60, -68])
        pkt = TelemetryPacket(
            node_id=NodeRole.RUBBLE_NODE,
            msg_type=MessageType.SEISMIC_ALERT,
            pitch=self.pitch,
            roll=self.roll,
            peak_freq=0,
            confidence=100,
            hop_count=self.active_hop,
            battery=self.battery,
        )
        self.send_packet(pkt, tag="💥 [SİSMİK ÇÖKME]")

    def toggle_relay_hop(self):
        """Sekme sayısını 1 (Doğrudan) ile 2 (Röle Aktarımlı) arasında değiştirir."""
        if self.active_hop == 1:
            self.active_hop = 2
            print("\n>>> SEKME DURUMU DEGISTI: 2 Sekme (Paket Röle Üzerinden İletiliyor)\n")
        else:
            self.active_hop = 1
            print("\n>>> SEKME DURUMU DEGISTI: 1 Sekme (Doğrudan İletim)\n")

    def _auto_loop(self):
        while self.running:
            self.trigger_heartbeat()
            time.sleep(self.auto_interval)

    def start(self):
        self.running = True
        print("=" * 75)
        print("   AFET SONRASI LORA MESH & AKUSTİK TESPİT SAHTE VERİ SİMÜLATÖRÜ")
        print("=" * 75)
        print(f"Yayın Hedefi: UDP {self.target_ip}:{self.target_port}")
        if self.serial_conn:
            print(f"Seri Port:    {self.serial_port_name} @ {self.baudrate}")
        print("-" * 75)
        print("KOMUTLAR:")
        print(" [1] veya [w] : DÜDÜK Alarmı Tetikle (2950 Hz)")
        print(" [2] veya [k] : RİTMİK VURUŞ Alarmı Tetikle (Taş/Çekiç)")
        print(" [3] veya [s] : SİSMİK ÇÖKME Uyarısı Tetikle (Yüksek Eğim)")
        print(" [r]          : Sekme Sayısını Değiştir (Hop 1 <-> Hop 2)")
        print(" [h]          : Anlık Kalp Atışı Gönder")
        print(" [q]          : Çıkış")
        print("=" * 75)

        # Arka planda periyodik kalp atışı döngüsü
        t = threading.Thread(target=self._auto_loop, daemon=True)
        t.start()

        # Ana döngü: Kullanıcı klavye komutlarını dinler
        try:
            while self.running:
                cmd = input().strip().lower()
                if cmd in ["1", "w"]:
                    self.trigger_whistle_alarm()
                elif cmd in ["2", "k"]:
                    self.trigger_knocking_alarm()
                elif cmd in ["3", "s"]:
                    self.trigger_seismic_collapse()
                elif cmd == "r":
                    self.toggle_relay_hop()
                elif cmd == "h":
                    self.trigger_heartbeat()
                elif cmd == "q":
                    print("Simülatör kapatılıyor...")
                    self.running = False
                    break
        except KeyboardInterrupt:
            self.running = False
            print("\nSimülatör durduruldu.")
        finally:
            if self.serial_conn and self.serial_conn.is_open:
                self.serial_conn.close()
            self.udp_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LoRa Afet Mesh Telemetri Simülatörü")
    parser.add_argument("--ip", default="127.0.0.1", help="Hedef UDP IP adresi")
    parser.add_argument("--port", type=int, default=5005, help="Hedef UDP Portu (Varsayılan: 5005)")
    parser.add_argument("--serial", default=None, help="Hedef Seri Port (Örn: COM3)")
    parser.add_argument("--baud", type=int, default=115200, help="Seri Port Baudrate")
    args = parser.parse_args()

    sim = MockTelemetryGenerator(
        target_ip=args.ip,
        target_port=args.port,
        serial_port=args.serial,
        baudrate=args.baud
    )
    sim.start()
