"""
main.py
AFAD İzleme İstasyonu Masaüstü Uygulaması Başlatıcı (Launcher)
Burdur Mehmet Akif Ersoy Üniversitesi | Bilgisayar Mühendisliği Lisans Tezi I
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.styles import DARK_THEME_QSS


def main():
    # Yüksek DPI ekranlar için ölçeklendirme ayarları
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("AFAD LoRa Mesh Monitor")
    app.setOrganizationName("MAKÜ Bilgisayar Mühendisliği")

    # Koyu Temayı (QSS) Tüm Uygulamaya Giydir
    app.setStyleSheet(DARK_THEME_QSS)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
