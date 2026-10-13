"""
ui/widgets/telemetry_table.py
Canlı Akan Telemetri Paket Log Tablosu ve CSV Dışa Aktarma
Çoklu Tema Uyumlu
"""

import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)
from core.telemetry_protocol import MessageType, TelemetryPacket


class TelemetryTableWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("📜 CANLI TELEMETRİ VE PAKET AKIŞ LOGU", parent)
        self.is_light_theme = False

        layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.lbl_count = QLabel("Toplam Alınan Paket: 0")
        self.lbl_count.setStyleSheet("color: #0284C7; font-weight: bold;")
        top_layout.addWidget(self.lbl_count)
        top_layout.addStretch()

        self.btn_export = QPushButton("CSV Olarak Kaydet")
        self.btn_export.clicked.connect(self.export_to_csv)
        top_layout.addWidget(self.btn_export)

        self.btn_clear = QPushButton("Temizle")
        self.btn_clear.clicked.connect(self.clear_table)
        top_layout.addWidget(self.btn_clear)
        layout.addLayout(top_layout)

        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels([
            "Zaman", "Düğüm", "Mesaj Türü", "Eğim (X/Y)", 
            "Frekans", "Güven", "Sekme (Hop)", "Pil", "Ham Hex"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addWidget(self.table)
        self.total_packets = 0

    def set_theme(self, is_light: bool):
        self.is_light_theme = is_light

    def add_packet(self, pkt: TelemetryPacket, raw_hex: str = ""):
        self.total_packets += 1
        self.lbl_count.setText(f"Toplam Alınan Paket: {self.total_packets}")

        row = 0
        self.table.insertRow(row)

        cur_time = time.strftime("%H:%M:%S")
        freq_str = f"{pkt.peak_freq} Hz" if pkt.peak_freq > 0 else "--"
        conf_str = f"%{pkt.confidence}" if pkt.confidence > 0 else "--"
        type_str = pkt.msg_type.name

        items = [
            QTableWidgetItem(cur_time),
            QTableWidgetItem(f"Düğüm #{pkt.node_id}"),
            QTableWidgetItem(type_str),
            QTableWidgetItem(f"{pkt.pitch}° / {pkt.roll}°"),
            QTableWidgetItem(freq_str),
            QTableWidgetItem(conf_str),
            QTableWidgetItem(f"{pkt.hop_count} Hop"),
            QTableWidgetItem(f"%{pkt.battery}"),
            QTableWidgetItem(raw_hex),
        ]

        if pkt.msg_type == MessageType.ACOUSTIC_ALARM:
            bg_color = QColor("#FEE2E2") if self.is_light_theme else QColor("#450A0A")
            fg_color = QColor("#B91C1C") if self.is_light_theme else QColor("#FCA5A5")
        elif pkt.msg_type == MessageType.SEISMIC_ALERT:
            bg_color = QColor("#FEF3C7") if self.is_light_theme else QColor("#451A03")
            fg_color = QColor("#B45309") if self.is_light_theme else QColor("#FDE047")
        else:
            bg_color = QColor("#FFFFFF") if self.is_light_theme else QColor("#0F172A")
            fg_color = QColor("#0F172A") if self.is_light_theme else QColor("#E2E8F0")

        for col, item in enumerate(items):
            item.setBackground(bg_color)
            item.setForeground(fg_color)
            self.table.setItem(row, col, item)

        if self.table.rowCount() > 200:
            self.table.removeRow(self.table.rowCount() - 1)

    def clear_table(self):
        self.table.setRowCount(0)
        self.total_packets = 0
        self.lbl_count.setText("Toplam Alınan Paket: 0")

    def export_to_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Telemetri Verisini CSV Olarak Kaydet", "", "CSV Dosyası (*.csv)")
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
                f.write(";".join(headers) + "\n")
                for r in range(self.table.rowCount()):
                    row_data = [self.table.item(r, c).text() if self.table.item(r, c) else "" for c in range(self.table.columnCount())]
                    f.write(";".join(row_data) + "\n")
        except Exception as e:
            print(f"CSV Kaydetme Hatası: {e}")
