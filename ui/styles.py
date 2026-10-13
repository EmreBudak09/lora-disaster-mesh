"""
ui/styles.py
AFAD Operasyon Merkezi Kurumsal Koyu Tema (QSS)
Modern, yüksek kontrastlı ve okunabilir afet yönetim arayüzü tasarımı.
"""

DARK_THEME_QSS = """
/* Genel Pencere ve Zemin */
QMainWindow, QDialog {
    background-color: #0B0F19;
    color: #F1F5F9;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}

QWidget {
    font-size: 13px;
    color: #E2E8F0;
}

/* Kartlar ve Grup Kutuları */
QGroupBox {
    background-color: #131B2E;
    border: 1px solid #1E293B;
    border-radius: 8px;
    margin-top: 24px;
    padding: 14px 12px 12px 12px;
    font-weight: bold;
    font-size: 13px;
    color: #38BDF8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 10px;
    background-color: #1E293B;
    border-radius: 4px;
    color: #38BDF8;
    left: 14px;
}

/* Butonlar */
QPushButton {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #F8FAFC;
    padding: 8px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #2563EB;
    border-color: #3B82F6;
    color: #FFFFFF;
}

QPushButton:pressed {
    background-color: #1D4ED8;
}

QPushButton#btn_connect {
    background-color: #059669;
    border-color: #10B981;
}

QPushButton#btn_connect:hover {
    background-color: #10B981;
}

QPushButton#btn_disconnect {
    background-color: #DC2626;
    border-color: #EF4444;
}

QPushButton#btn_disconnect:hover {
    background-color: #EF4444;
}

QPushButton#btn_clear_alarm {
    background-color: #B45309;
    border-color: #F59E0B;
}

QPushButton#btn_clear_alarm:hover {
    background-color: #D97706;
}

/* Giriş Kutuları ve Açılır Menüler */
QLineEdit, QComboBox, QSpinBox {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 10px;
    color: #F8FAFC;
    selection-background-color: #2563EB;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #38BDF8;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #0F172A;
    border: 1px solid #334155;
    selection-background-color: #1E293B;
    color: #F8FAFC;
}

/* Canlı Telemetri Tablosu */
QTableWidget {
    background-color: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 6px;
    gridline-color: #1E293B;
    color: #E2E8F0;
    selection-background-color: #1E293B;
}

QHeaderView::section {
    background-color: #1E293B;
    color: #94A3B8;
    padding: 6px 8px;
    border: none;
    border-right: 1px solid #0F172A;
    font-weight: bold;
    font-size: 12px;
}

QTableWidget::item {
    padding: 5px;
}

/* Durum Çubuğu */
QStatusBar {
    background-color: #0B0F19;
    border-top: 1px solid #1E293B;
    color: #94A3B8;
    font-size: 12px;
}

/* Kaydırma Çubukları */
QScrollBar:vertical {
    background-color: #0F172A;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background-color: #334155;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #475569;
}
"""
