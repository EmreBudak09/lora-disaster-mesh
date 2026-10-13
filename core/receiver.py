"""
core/receiver.py
Çoklu Giriş Destekli Arka Plan Telemetri Alıcısı (QThread)
Hem Sanal UDP Portunu (Simülatör) hem de Gerçek Seri Portu (Gateway USB) dinler.
"""

import socket
import time
from PyQt5.QtCore import QThread, pyqtSignal

from core.telemetry_protocol import (
    HEADER_BYTE,
    PACKET_SIZE,
    TelemetryPacket,
)


class TelemetryReceiverThread(QThread):
    # PyQt Sinyalleri
    packet_received = pyqtSignal(object, str)       # (TelemetryPacket, kaynak_bilgisi)
    raw_packet_hex = pyqtSignal(str)               # Ham hex string (Örn: "aa 01 02 ...")
    status_changed = pyqtSignal(bool, str)          # (Bagli_mi, Durum_Mesaji)
    error_occurred = pyqtSignal(str)                # Hata mesaji

    def __init__(self, mode="UDP", udp_port=5005, serial_port=None, baudrate=115200, parent=None):
        super().__init__(parent)
        self.mode = mode.upper()  # "UDP" veya "SERIAL"
        self.udp_port = udp_port
        self.serial_port_name = serial_port
        self.baudrate = baudrate
        self._is_running = False

    def configure_udp(self, port=5005):
        """UDP moduna geçir ve port ayarla."""
        self.mode = "UDP"
        self.udp_port = port

    def configure_serial(self, port_name, baudrate=115200):
        """Seri port moduna geçir."""
        self.mode = "SERIAL"
        self.serial_port_name = port_name
        self.baudrate = baudrate

    def stop(self):
        """İş parçacığını güvenli şekilde durdurur."""
        self._is_running = False
        self.wait(2000)

    def run(self):
        self._is_running = True

        if self.mode == "UDP":
            self._run_udp_listener()
        elif self.mode == "SERIAL":
            self._run_serial_listener()
        else:
            self.error_occurred.emit(f"Bilinmeyen alıcı modu: {self.mode}")
            self.status_changed.emit(False, f"Hata: Geçersiz mod {self.mode}")

    def _run_udp_listener(self):
        had_error = False
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            import sys
            if sys.platform != "win32":
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", self.udp_port))
            sock.settimeout(0.5)

            self.status_changed.emit(True, f"UDP Dinleniyor: Port {self.udp_port}")

            while self._is_running:
                try:
                    data, addr = sock.recvfrom(128)
                    if not data:
                        continue

                    if len(data) >= PACKET_SIZE:
                        header_idx = data.find(bytes([HEADER_BYTE]))
                        if header_idx != -1 and len(data) >= header_idx + PACKET_SIZE:
                            raw_pkt = data[header_idx:header_idx + PACKET_SIZE]
                            try:
                                pkt = TelemetryPacket.unpack(raw_pkt)
                                self.raw_packet_hex.emit(raw_pkt.hex(" ").upper())
                                self.packet_received.emit(pkt, f"UDP ({addr[0]}:{addr[1]})")
                            except Exception as parse_err:
                                self.error_occurred.emit(f"UDP Ayrıştırma Hatası: {parse_err}")
                except socket.timeout:
                    continue
                except Exception as loop_err:
                    if self._is_running:
                        self.error_occurred.emit(f"Soket Okuma Hatası: {loop_err}")
                        time.sleep(0.1)

        except Exception as e:
            had_error = True
            err_msg = f"Port {self.udp_port} Meşgul! (Arka plandaki eski pencereyi kapatın)" if "10048" in str(e) else f"UDP Hatası: {e}"
            self.status_changed.emit(False, err_msg)
            self.error_occurred.emit(err_msg)
        finally:
            if sock:
                sock.close()
            if not had_error:
                self.status_changed.emit(False, "UDP Alıcısı Durduruldu")

    def _run_serial_listener(self):
        ser = None
        try:
            import serial
            ser = serial.Serial(self.serial_port_name, self.baudrate, timeout=0.5)
            self.status_changed.emit(True, f"Seri Port Açık: {self.serial_port_name} @ {self.baudrate}")

            buffer = bytearray()

            while self._is_running:
                try:
                    bytes_waiting = ser.in_waiting
                    if bytes_waiting > 0:
                        incoming = ser.read(bytes_waiting)
                        buffer.extend(incoming)

                        # Buffer içinde 0xAA başlığını ara
                        while len(buffer) >= PACKET_SIZE:
                            if buffer[0] == HEADER_BYTE:
                                raw_pkt = bytes(buffer[:PACKET_SIZE])
                                try:
                                    pkt = TelemetryPacket.unpack(raw_pkt)
                                    self.raw_packet_hex.emit(raw_pkt.hex(" ").upper())
                                    self.packet_received.emit(pkt, f"Seri ({self.serial_port_name})")
                                except Exception as parse_err:
                                    self.error_occurred.emit(f"Seri Ayrıştırma Hatası: {parse_err}")
                                # Paketi buffer'dan tüket
                                buffer = buffer[PACKET_SIZE:]
                            else:
                                # Senkronizasyon kaymışsa 0xAA görene kadar kaydır
                                buffer.pop(0)
                    else:
                        time.sleep(0.02)
                except Exception as ser_err:
                    if self._is_running:
                        self.error_occurred.emit(f"Seri Port Okuma Hatası: {ser_err}")
                        time.sleep(0.2)

        except Exception as e:
            self.status_changed.emit(False, f"Seri Port Hatası: {e}")
            self.error_occurred.emit(f"Seri Port Başlatılamadı: {e}")
        finally:
            if ser and ser.is_open:
                ser.close()
            self.status_changed.emit(False, "Seri Port Kapatıldı")
