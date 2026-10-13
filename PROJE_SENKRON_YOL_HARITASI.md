# 🧭 LİSANS TEZİ MASTER SENKRONİZE ÇALIŞMA PLANI (HAFTA HAFTA)

**Proje:** Afet Sonrası Altyapısız Arama-Kurtarma İçin Çok Sekmeli (Multi-Hop) LoRa Mesh ve Uçta Akustik Tespit Sistemi  
**Ders:** Lisans Tezi I & II (2026–2027)  
**Kurum:** Burdur Mehmet Akif Ersoy Üniversitesi | Bilgisayar Mühendisliği  
**Danışman:** Dr. Öğretim Üyesi Tülay TURAN  
**Ekip:** Emre BUDAK (Kaptan), Qusai NAAJEH, Ali Arda DURAN  

---

## 🔗 Ekip Rol Dağılımı ve Görev Senkronizasyon Şeması

```
[ AŞAMA 1: Hafta 1-2 ] ──► Ortak Protokol Tanımı (11 Bayt Struct) & İzole Simülatör
       │
[ AŞAMA 2: Hafta 3-5 ] ──► Bireysel Geliştirme (FFT DSP / LoRa P2P / PyQt Arayüz)
       │
[ AŞAMA 3: Hafta 6-8 ] ──► 1. Bütünleşme: Enkaz Düğümü -> Gateway -> Arayüz (Tek Sekme)
       │
[ AŞAMA 4: Hafta 9-11] ──► 2. Bütünleşme: Multi-Hop Röle Katmanı & Ritmik Vuruş Filtresi
       │
[ AŞAMA 5: Hafta 12-13]──► Sismik Test Tablası, Saha Doğrulaması & Performans Metrikleri
       │
[ AŞAMA 6: Hafta 14+ ] ──► Tez Yazımı (Bölüm Bölüm Dağılım), TÜBİTAK Raporu & Savunma
```

---

## 📌 AŞAMA 1: Temel Mimari, Protokol Kilidi ve İzole Ortamlar (Hafta 1 – 2)
> 🔒 **Senkronizasyon Kilidi:** 11 Baytlık `TelemetryPacket` ikili C Struct yapısının onaylanması.

| Kişi | Görevler | Haftalık Çıktı |
| :--- | :--- | :--- |
| **Emre BUDAK** | • Donanım sipariş listesinin kontrolü.<br>• `telemetry_packet.h` C Struct kodunun yazılması ve GitHub'a yüklenmesi.<br>• arduinoFFT için frekans çözünürlüğü ve örnekleme penceresi analizi. | `telemetry_packet.h` dosyası & GitHub ilk commit |
| **Qusai NAAJEH** | • ESP32 - Ra-02 SPI pin bağlantı şemasının hazırlanması.<br>• 433 MHz ISM bandı frekans (433.175 MHz), BW (125 kHz) ve SF parametrelerinin tespiti. | SPI bağlantı şeması & LoRa RF konfigürasyon taslağı |
| **Ali Arda DURAN** | • `mock_telemetry.py` (Sahte veri simülatörü) kodlanması (11 baytlık paketi sanal seri port/UDP'ye basan script).<br>• PyQt5/PySide6 arayüz iskeletinin kurulması.<br>• IP67 buat kutusu ve SMA anten sipariş ölçüleri. | Çalışan Sahte Veri Simülatörü & İlk Arayüz Penceresi |

---

## 📌 AŞAMA 2: Bireysel Modül Geliştirme & İzole Testler (Hafta 3 – 5)
> 🔒 **Senkronizasyon Kilidi:** Donanımların gelmesiyle bağımsız birim testlerinin tamamlanması.

| Kişi | Görevler | Haftalık Çıktı |
| :--- | :--- | :--- |
| **Emre BUDAK** | • ESP32 dahili ADC ile MAX4466 üzerinden 8 kHz zamanlayıcı (Timer Interrupt) tabanlı örnekleme.<br>• Test düdüğü ile 2.5–3.5 kHz aralığındaki tepe frekansı yakalama.<br>• MPU-6050 I2C sürücüsü ile açı (pitch/roll) okuma. | Düdük frekansını ekrana yazdıran ESP32 Firmware taslağı |
| **Qusai NAAJEH** | • İki adet ESP32 + Ra-02 arasında noktadan noktaya (P2P) ilk veri iletimi.<br>• SF7–SF10 yayılma faktörlerinde RSSI, SNR ve havada kalma süresi (ToA) ölçümü. | İki düğüm arası çalışan P2P LoRa bağlantısı ve test logları |
| **Ali Arda DURAN** | • AFAD İzleme Arayüzünün geliştirilmesi (Ağ düğüm durumları, sismik açı ibresi, kırmızı flaşlı acil durum alarm kutusu).<br>• Simülatör üzerinden saniyede 10 paket basılarak arayüz donma/stres testi. | Simülatörle canlı veri gösteren dinamik AFAD paneli |

---

## 📌 AŞAMA 3: İlk Entegrasyon - Milestone 1 (Hafta 6 – 8)
> 🔒 **Senkronizasyon Kilidi:** Enkaz Düğümü ➔ AFAD Gateway ➔ Bilgisayar Arayüzü (Sekmesiz doğrudan hat).

| Kişi | Görevler | Haftalık Çıktı |
| :--- | :--- | :--- |
| **Emre BUDAK** | • FFT ve MPU-6050 verisini Qusai'nin LoRa verici fonksiyonuna besleme.<br>• Düdük algılandığında otomatik alarm paketini havaya fırlatma. | Enkaz Düğümü Verici Firmware v1.0 |
| **Qusai NAAJEH** | • AFAD Gateway ESP32'sinin gelen LoRa paketini USB Seri Port (UART) üzerinden bilgisayara aktarması. | Gateway Alıcı Firmware v1.0 |
| **Ali Arda DURAN** | • Arayüzü Gateway'in gerçek USB portuna bağlama; masada çalınan düdüğün ekrana gerçek alarm olarak düşmesini sağlama.<br>• IP67 buat kutusuna devreleri, pili ve dış SMA anteni monte etme. | Gerçek donanımla çalışan uçtan uca sistem & 1. Donanım Kutusu |

---

## 📌 AŞAMA 4: Çok Sekmeli (Multi-Hop) Mesh ve Röle (Hafta 9 – 11)
> 🔒 **Senkronizasyon Kilidi:** Enkaz Düğümü ➔ Röle Düğümü ➔ Gateway ➔ Arayüz (2 Sekmeli İletim).

| Kişi | Görevler | Haftalık Çıktı |
| :--- | :--- | :--- |
| **Emre BUDAK** | • Enkaz altında ritmik vuruş (taş/çekiç darbeleri) zamanlama filtreleme algoritması.<br>• Arka plan gürültüsü (siren/iş makinesi) için dinamik eşikleme. | Ritmik Vuruş & Gürültü Filtreli Firmware v2.0 |
| **Qusai NAAJEH** | • 3. düğüm olan `Röle Düğümü` yazılımı.<br>• Paketi duyunca `Hop_Count` değerini 1 artırıp tekrar yayan yönlendirme.<br>• Aynı paketi sonsuz döngüye sokmayan mükerrer paket engelleme (Duplicate Rejection). | Çok sekmeli çalışan Röle Firmware'i |
| **Ali Arda DURAN** | • Arayüzde çok sekmeli topoloji grafiği (paketin hangi röleden geldiğini görselleştirme).<br>• Uçtan uca iletim gecikmesi (Latency) ölçüm sayacı. | Mesh topolojisini ve gecikmeyi canlı gösteren arayüz |

---

## 📌 AŞAMA 5: Sismik Tabla, Saha Testleri ve Başarım Ölçümü (Hafta 12 – 13)
> 🔒 **Senkronizasyon Kilidi:** Başarı ölçütlerinin sayısal olarak kanıtlanması ve deney logları.

* **Fiziksel Test Düzeneği (Ali Arda):** Titreşim motorlu strafor sismik test tablasının hazırlanması.
* **Deney 1 - Ses/Gürültü Ayrımı (Emre & Ekip):**
  * Siren ve rüzgar sesinde Yanlış Alarm Oranı (Hedef: %0).
  * Düdük ve ritmik darbede Doğru Tespit Oranı (Hedef: Minimum %90).
* **Deney 2 - İletim Başarısı & Gecikme (Qusai & Ekip):**
  * 1 sekme (Röle üzerinden) ile Paket Teslim Oranı (PDR - Hedef: %100 veya sıfır veri kaybı).
  * Alarm iletim gecikmesi (Hedef: 2 saniyenin altı).
* **Deney 3 - Sismik Çökme (Ali Arda & Ekip):**
  * Tablanın titreştirilip kutunun devrilmesi anında MPU-6050 eğim alarmının ekrana düşme testi.

---

## 📌 AŞAMA 6: Tez Yazımı, Raporlama ve Savunma Provası (Hafta 14+)
> 🔒 **Senkronizasyon Kilidi:** IEEE/Üniversite tez şablonunun eksiksiz doldurulması.

| Tez Bölümü | Sorumlu Yazar | İçerik ve Kapsam |
| :--- | :--- | :--- |
| **Bölüm 1 & 2: Giriş ve Literatür** | **Tüm Ekip** | Afet haberleşmesi sorunları, mevcut çözümler, literatür boşluğu. |
| **Bölüm 3: Uçta Akustik Tespit ve Sinyal İşleme** | **Emre BUDAK** | MAX4466, ADC örnekleme, arduinoFFT, frekans tepe analizi, ritmik vuruş filtresi ve akış şemaları. |
| **Bölüm 4: Çok Sekmeli LoRa Mesh Protokolü** | **Qusai NAAJEH** | 433 MHz Ra-02 RF analizi, ToA hesabı, 11 baytlık struct, çok sekmeli yönlendirme algoritması, PDR sonuçları. |
| **Bölüm 5: İzleme İstasyonu Arayüzü ve Entegrasyon** | **Ali Arda DURAN** | PyQt mimarisi, sahte veri simülatörü, IP67 kutu tasarımı, sismik tabla deneyleri, gecikme grafikleri. |
| **Bölüm 6: Sonuç ve Gelecek Çalışmalar** | **Tüm Ekip** | Sistemin kısıtları, başarımı, 2209-A nihai çıktısı. |
| **Savunma Hazırlığı** | **Tüm Ekip** | Canlı sistem demosu provası, jüri soru-cevap simülasyonu. |
