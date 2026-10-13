"""
ui/styles.py
AFAD Operasyon Merkezi Çoklu Renk Temaları (QSS)
- Koyu Gece Modu (Dark Slate)
- AFAD Taktik Modu (Navy Blue)
- Aydınlık Gündüz Modu (Clean Light)
"""

DARK_THEME_QSS = """
QMainWindow, QDialog {
    background-color: #0B0F19;
    color: #F1F5F9;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}

QWidget {
    font-size: 13px;
    color: #E2E8F0;
}

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

QPushButton {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #F8FAFC;
    padding: 7px 15px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #2563EB;
    border-color: #3B82F6;
    color: #FFFFFF;
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

QLineEdit, QComboBox, QSpinBox {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 10px;
    color: #F8FAFC;
    selection-background-color: #2563EB;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #38BDF8;
}

QComboBox QAbstractItemView {
    background-color: #0F172A;
    border: 1px solid #334155;
    selection-background-color: #1E293B;
    color: #F8FAFC;
}

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

QStatusBar {
    background-color: #0B0F19;
    border-top: 1px solid #1E293B;
    color: #94A3B8;
}
"""

NAVY_THEME_QSS = """
QMainWindow, QDialog {
    background-color: #0A192F;
    color: #E6F1FF;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}

QWidget {
    font-size: 13px;
    color: #CCD6F6;
}

QGroupBox {
    background-color: #112240;
    border: 1px solid #233554;
    border-radius: 8px;
    margin-top: 24px;
    padding: 14px 12px 12px 12px;
    font-weight: bold;
    font-size: 13px;
    color: #64FFDA;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 10px;
    background-color: #233554;
    border-radius: 4px;
    color: #64FFDA;
    left: 14px;
}

QPushButton {
    background-color: #1D3557;
    border: 1px solid #457B9D;
    border-radius: 6px;
    color: #F1FAEE;
    padding: 7px 15px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #0284C7;
    border-color: #38BDF8;
    color: #FFFFFF;
}

QPushButton#btn_connect {
    background-color: #047857;
    border-color: #10B981;
}

QPushButton#btn_disconnect {
    background-color: #B91C1C;
    border-color: #EF4444;
}

QPushButton#btn_clear_alarm {
    background-color: #B45309;
    border-color: #F59E0B;
}

QLineEdit, QComboBox, QSpinBox {
    background-color: #172A45;
    border: 1px solid #2A4365;
    border-radius: 6px;
    padding: 6px 10px;
    color: #E6F1FF;
    selection-background-color: #0284C7;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #64FFDA;
}

QComboBox QAbstractItemView {
    background-color: #172A45;
    border: 1px solid #2A4365;
    selection-background-color: #1D3557;
    color: #E6F1FF;
}

QTableWidget {
    background-color: #0D1B2A;
    border: 1px solid #1B263B;
    border-radius: 6px;
    gridline-color: #1B263B;
    color: #E0E1DD;
}

QHeaderView::section {
    background-color: #1B263B;
    color: #778DA9;
    padding: 6px 8px;
    border: none;
    border-right: 1px solid #0D1B2A;
    font-weight: bold;
    font-size: 12px;
}

QStatusBar {
    background-color: #0A192F;
    border-top: 1px solid #1B263B;
    color: #8892B0;
}
"""

LIGHT_THEME_QSS = """
QMainWindow, QDialog {
    background-color: #F1F5F9;
    color: #0F172A;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}

QWidget {
    font-size: 13px;
    color: #1E293B;
}

QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    margin-top: 24px;
    padding: 14px 12px 12px 12px;
    font-weight: bold;
    font-size: 13px;
    color: #0284C7;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 10px;
    background-color: #E2E8F0;
    border-radius: 4px;
    color: #0369A1;
    left: 14px;
}

QPushButton {
    background-color: #E2E8F0;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    color: #0F172A;
    padding: 7px 15px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #0284C7;
    border-color: #0369A1;
    color: #FFFFFF;
}

QPushButton#btn_connect {
    background-color: #10B981;
    border-color: #059669;
    color: #FFFFFF;
}

QPushButton#btn_connect:hover {
    background-color: #059669;
}

QPushButton#btn_disconnect {
    background-color: #EF4444;
    border-color: #DC2626;
    color: #FFFFFF;
}

QPushButton#btn_disconnect:hover {
    background-color: #DC2626;
}

QPushButton#btn_clear_alarm {
    background-color: #F59E0B;
    border-color: #D97706;
    color: #FFFFFF;
}

QPushButton#btn_clear_alarm:hover {
    background-color: #D97706;
}

QLineEdit, QComboBox, QSpinBox {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 6px 10px;
    color: #0F172A;
    selection-background-color: #0284C7;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #0284C7;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    selection-background-color: #E2E8F0;
    color: #0F172A;
}

QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    gridline-color: #E2E8F0;
    color: #0F172A;
    selection-background-color: #E2E8F0;
}

QHeaderView::section {
    background-color: #E2E8F0;
    color: #334155;
    padding: 6px 8px;
    border: none;
    border-right: 1px solid #FFFFFF;
    font-weight: bold;
    font-size: 12px;
}

QStatusBar {
    background-color: #F1F5F9;
    border-top: 1px solid #CBD5E1;
    color: #475569;
}
"""

THEMES = {
    "Koyu Gece (Siyah/Gri)": DARK_THEME_QSS,
    "AFAD Taktik (Okyanus Mavisi)": NAVY_THEME_QSS,
    "Aydınlık Mod (Beyaz/Gündüz)": LIGHT_THEME_QSS,
}


def get_theme_qss(theme_name: str) -> str:
    """Temanın QSS kodunu döndürür."""
    return THEMES.get(theme_name, DARK_THEME_QSS)
