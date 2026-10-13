"""
ui/styles.py
Modern Web / Mobil Arayüz Hissiyatlı AFAD Tasarım Sistemi (SaaS / Dashboard QSS)
- Büyük dokunmatik dostu butonlar
- Genişletilmiş ve okunaklı tipografi
- Yumuşak köşe yuvarlatmaları (border-radius: 10px - 14px)
- Temiz ve bölünmüş modern kart tasarımları
"""

DARK_THEME_QSS = """
QMainWindow, QDialog {
    background-color: #090D16;
    color: #F8FAFC;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}

QWidget {
    font-size: 14px;
    color: #CBD5E1;
}

/* Üst Navigasyon Çubuğu Kartı */
QFrame#TopNavBar {
    background-color: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
}

/* Modern Web Kartları (GroupBox) */
QGroupBox {
    background-color: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    margin-top: 26px;
    padding: 16px 14px 14px 14px;
    font-weight: 700;
    font-size: 14px;
    color: #38BDF8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 6px 14px;
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #38BDF8;
    left: 16px;
}

/* Modern Web Butonları (Büyük, Yumuşak Köşeli) */
QPushButton {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #F8FAFC;
    padding: 9px 18px;
    font-weight: 600;
    font-size: 13px;
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
    border: 1px solid #10B981;
    color: #FFFFFF;
    font-weight: 700;
}

QPushButton#btn_connect:hover {
    background-color: #10B981;
}

QPushButton#btn_disconnect {
    background-color: #DC2626;
    border: 1px solid #EF4444;
    color: #FFFFFF;
    font-weight: 700;
}

QPushButton#btn_disconnect:hover {
    background-color: #EF4444;
}

QPushButton#btn_clear_alarm {
    background-color: #D97706;
    border: 1px solid #F59E0B;
    color: #FFFFFF;
    font-weight: 700;
    padding: 10px 20px;
    font-size: 14px;
    border-radius: 8px;
}

QPushButton#btn_clear_alarm:hover {
    background-color: #F59E0B;
}

/* Form Elemanları (Input & Dropdown) */
QLineEdit, QComboBox, QSpinBox {
    background-color: #0B1120;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 12px;
    color: #F8FAFC;
    font-size: 13px;
    min-height: 20px;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #38BDF8;
    background-color: #0F172A;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #111827;
    border: 1px solid #334155;
    selection-background-color: #1E293B;
    selection-color: #38BDF8;
    color: #F8FAFC;
    padding: 4px;
    border-radius: 6px;
}

/* Modern Tablo */
QTableWidget {
    background-color: #0B1120;
    border: 1px solid #1F2937;
    border-radius: 10px;
    gridline-color: #1E293B;
    color: #F1F5F9;
    font-size: 13px;
}

QHeaderView::section {
    background-color: #1E293B;
    color: #94A3B8;
    padding: 10px 8px;
    border: none;
    border-right: 1px solid #0B1120;
    font-weight: 700;
    font-size: 12px;
}

/* Bölücü Çizgi (Splitter Handle - İnce ve Şık) */
QSplitter::handle {
    background-color: #1E293B;
    width: 3px;
}

QSplitter::handle:hover {
    background-color: #38BDF8;
}

/* Durum Çubuğu */
QStatusBar {
    background-color: #090D16;
    border-top: 1px solid #1F2937;
    color: #94A3B8;
    font-size: 12px;
    padding: 4px;
}
"""

NAVY_THEME_QSS = """
QMainWindow, QDialog {
    background-color: #060F1E;
    color: #F0F6FC;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}

QWidget {
    font-size: 14px;
    color: #C9D1D9;
}

QFrame#TopNavBar {
    background-color: #0D1D35;
    border: 1px solid #1C335A;
    border-radius: 12px;
}

QGroupBox {
    background-color: #0D1D35;
    border: 1px solid #1C335A;
    border-radius: 12px;
    margin-top: 26px;
    padding: 16px 14px 14px 14px;
    font-weight: 700;
    font-size: 14px;
    color: #60A5FA;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 6px 14px;
    background-color: #172D4D;
    border: 1px solid #23416F;
    border-radius: 6px;
    color: #60A5FA;
    left: 16px;
}

QPushButton {
    background-color: #1A3459;
    border: 1px solid #2E5083;
    border-radius: 8px;
    color: #F8FAFC;
    padding: 9px 18px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #2563EB;
    border-color: #60A5FA;
    color: #FFFFFF;
}

QPushButton#btn_connect {
    background-color: #047857;
    border: 1px solid #10B981;
    color: #FFFFFF;
    font-weight: 700;
}

QPushButton#btn_disconnect {
    background-color: #B91C1C;
    border: 1px solid #EF4444;
    color: #FFFFFF;
    font-weight: 700;
}

QPushButton#btn_clear_alarm {
    background-color: #D97706;
    border: 1px solid #F59E0B;
    color: #FFFFFF;
    font-weight: 700;
    padding: 10px 20px;
    font-size: 14px;
    border-radius: 8px;
}

QLineEdit, QComboBox, QSpinBox {
    background-color: #081528;
    border: 1px solid #1E3A66;
    border-radius: 8px;
    padding: 8px 12px;
    color: #F8FAFC;
    font-size: 13px;
    min-height: 20px;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #60A5FA;
}

QComboBox QAbstractItemView {
    background-color: #0D1D35;
    border: 1px solid #1E3A66;
    selection-background-color: #172D4D;
    selection-color: #60A5FA;
    color: #F8FAFC;
}

QTableWidget {
    background-color: #081528;
    border: 1px solid #1C335A;
    border-radius: 10px;
    gridline-color: #142742;
    color: #F0F6FC;
    font-size: 13px;
}

QHeaderView::section {
    background-color: #172D4D;
    color: #93C5FD;
    padding: 10px 8px;
    border: none;
    border-right: 1px solid #081528;
    font-weight: 700;
    font-size: 12px;
}

QSplitter::handle {
    background-color: #1C335A;
    width: 3px;
}

QStatusBar {
    background-color: #060F1E;
    border-top: 1px solid #1C335A;
    color: #93C5FD;
    padding: 4px;
}
"""

LIGHT_THEME_QSS = """
QMainWindow, QDialog {
    background-color: #F8FAFC;
    color: #0F172A;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}

QWidget {
    font-size: 14px;
    color: #1E293B;
}

QFrame#TopNavBar {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    margin-top: 26px;
    padding: 16px 14px 14px 14px;
    font-weight: 700;
    font-size: 14px;
    color: #0284C7;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 6px 14px;
    background-color: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    color: #0369A1;
    left: 16px;
}

QPushButton {
    background-color: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    color: #0F172A;
    padding: 9px 18px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #0284C7;
    border-color: #0369A1;
    color: #FFFFFF;
}

QPushButton#btn_connect {
    background-color: #10B981;
    border: 1px solid #059669;
    color: #FFFFFF;
    font-weight: 700;
}

QPushButton#btn_disconnect {
    background-color: #EF4444;
    border: 1px solid #DC2626;
    color: #FFFFFF;
    font-weight: 700;
}

QPushButton#btn_clear_alarm {
    background-color: #F59E0B;
    border: 1px solid #D97706;
    color: #FFFFFF;
    font-weight: 700;
    padding: 10px 20px;
    font-size: 14px;
    border-radius: 8px;
}

QLineEdit, QComboBox, QSpinBox {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 8px 12px;
    color: #0F172A;
    font-size: 13px;
    min-height: 20px;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #0284C7;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    selection-background-color: #F1F5F9;
    selection-color: #0284C7;
    color: #0F172A;
}

QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    gridline-color: #F1F5F9;
    color: #0F172A;
    font-size: 13px;
}

QHeaderView::section {
    background-color: #F1F5F9;
    color: #334155;
    padding: 10px 8px;
    border: none;
    border-right: 1px solid #E2E8F0;
    font-weight: 700;
    font-size: 12px;
}

QSplitter::handle {
    background-color: #E2E8F0;
    width: 3px;
}

QStatusBar {
    background-color: #F8FAFC;
    border-top: 1px solid #E2E8F0;
    color: #64748B;
    padding: 4px;
}
"""

THEMES = {
    "Koyu Gece (Siyah/Gri)": DARK_THEME_QSS,
    "AFAD Taktik (Okyanus Mavisi)": NAVY_THEME_QSS,
    "Aydınlık Mod (Beyaz/Gündüz)": LIGHT_THEME_QSS,
}


def get_theme_qss(theme_name: str) -> str:
    return THEMES.get(theme_name, DARK_THEME_QSS)
