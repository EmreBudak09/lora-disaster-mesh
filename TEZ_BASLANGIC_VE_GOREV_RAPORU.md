# 📋 LİSANS TEZİ I: AKADEMİK DEĞERLENDİRME, RİSK ANALİZİ VE YOL HARİTASI RAPORU

**Tarih:** 13 Ekim 2026  
**Kurum:** Burdur Mehmet Akif Ersoy Üniversitesi | Mühendislik-Mimarlık Fakültesi | Bilgisayar Mühendisliği Bölümü  
**Ders:** Lisans Tezi I (2026–2027 Güz Dönemi)  
**Danışman:** Dr. Öğretim Üyesi Tülay TURAN  
**Dış Hedefler:** TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri, TEKNOFEST İnsanlık Yararına Teknoloji  

---

## 👥 Ekip ve Görev Dağılımı

| Öğrenci Adı | Görev Alanı | Sorumluluk ve Çıktılar |
| :--- | :--- | :--- |
| **Emre BUDAK** *(Kaptan)* | Sistem Mimarisi & Gömülü DSP | ESP32 Firmware, arduinoFFT ile düdük tespiti, ritmik vuruş filtreleme, telemetri paketleyici (packer), GitHub koordinasyonu. |
| **Qusai NAAJEH** | Ağ Katmanı & Haberleşme | LoRa 433 MHz Mesh yönlendirme (routing/multi-hop), paket iletimi, gecikme/kayıp analizleri, BLE/Wi-Fi acil durum köprüsü. |
| **Ali Arda DURAN** | İstasyon Arayüzü & Entegrasyon | AFAD İzleme İstasyonu (PyQt/PySide tabanlı CBS/telemetri paneli), Sahte Veri Simülatörü (Mock Generator), IP67 buat kutusu ve sensör entegrasyonu. |

---

## 🎯 Projenin Çekirdek Felsefesi ve Amacı

Deprem gibi afetlerde GSM baz istasyonları ve enerji altyapısı çöker. Bu çalışmada, harici hiçbir altyapıya ihtiyaç duymadan enkaz altından akustik (düdük/ritmik vuruş) ve mekanik (sismik eğim/çökme) belirtileri toplayan, bunları uçta analiz eden ve çok sekmeli (multi-hop) LoRa ağı üzerinden arama-kurtarma ekiplerine ulaştıran otonom bir sistem kurulacaktır.

> **Kritik Kural:** LoRa dar bantlı bir teknolojidir; merkeze **asla ham ses akışı (audio streaming) yapılmayacaktır.** Uç cihaz (ESP32) FFT ve filtreleme ile tespiti yerel olarak yapacak, ağ üzerinden sadece **11 baytlık hafif alarm/telemetri paketleri** iletilecektir.

---

## ⚠️ Kritik Teknik Uyarılar ve Risk Analizi

### 1. 433 MHz Frekansı ve Anten Boyutu (Donanım/Entegrasyon)
* **Avantaj:** 433 MHz, 868 MHz'e kıyasla daha uzun dalga boyuna (~69 cm) sahiptir; moloz, betonarme ve toprak altından geçerken sinyal sönümlenmesi daha azdır.
* **Risk:** En verimli çeyrek dalga boyu anten boyutu **yaklaşık 17.3 cm** tutmaktadır. Bu anten standart IP67 buat kutularının içine düz sığmaz.
* **Çözüm:** Kutunun içerisine verimi düşük spiral yay anten koymak yerine; buat kutusu contalı bir rekorla delinmeli, **kutu dışına SMA konnektör ile 17 cm kauçuk çubuk anten** monte edilmelidir.

### 2. ESP32 Dahili ADC ve Mikrofon Gürültüsü (Sinyal İşleme)
* **Risk:** MAX4466 analog çıkışlı bir modüldür. ESP32'nin dahili ADC'si lineer değildir ve özellikle LoRa modülü yayın yaparken besleme hattından kaynaklı yüksek elektriksel gürültü oluşur. Bu gürültü FFT'de sahte tepeler (false peak) oluşturabilir.
* **Çözüm:** Düdük sesleri genellikle 2.5 kHz – 3.5 kHz aralığındadır. Nyquist kuralına göre örnekleme frekansı en az **8 kHz** olmalıdır. Mikrofon okumaları ana döngüde (`loop`) serbest bırakılmamalı; `Timer Interrupt` veya `I2S/DMA` yardımıyla sabit frekansta örneklenmelidir.

### 3. Paket Boyutu ve Havada Kalma Süresi (Time-on-Air)
* **Risk:** LoRa üzerinde JSON veya uzun metin göndermek havada kalma süresini uçurur, paket çarpışmalarına (collision) yol açar ve bataryayı hızla tüketir.
* **Çözüm:** Ağ üzerindeki tüm iletişim **11 Baytlık sabit C Struct (Binary)** formatında yürütülmelidir.

---

## 📡 Standart Telemetri Bayt Protokolü (v1.0)

Arayüz, gömülü yazılım ve LoRa katmanının ortak konuşacağı paket yapısı:

```c
typedef struct __attribute__((packed)) {
    uint8_t  header;       // 0xAA (Paket başlangıç baytı)
    uint8_t  node_id;      // 1: Enkaz Düğümü, 2: Röle, 3: Gateway
    uint8_t  msg_type;     // 0x01: Durum/Kalp Atışı, 0x02: Düdük Alarmı, 0x03: Sismik Çökme
    int8_t   pitch;        // MPU-6050 Eğim açısı (-90 ile +90 derece)
    int8_t   roll;         // MPU-6050 Dönme açısı (-90 ile +90 derece)
    uint16_t peak_freq;    // Tespit edilen baskın ses frekansı (Hz cinsinden)
    uint8_t  confidence;   // Algılama doğruluk yüzdesi (%0 - %100)
    uint8_t  hop_count;    // Sekme sayısı (TTL / Mesh takibi için)
    uint8_t  battery;      // Batarya seviyesi (%)
    uint8_t  checksum;     // XOR / CRC8 kontrol baytı
} TelemetryPacket;
```
*Toplam Boyut: Yalnızca 11 Bayt.*

---

## 🗓️ İlk 2 Hafta İçin Kişisel Eylem Planı

### 🔹 Ali Arda DURAN (İstasyon Arayüzü & Simülatör)
1. **Sahte Veri Simülatörü (`mock_telemetry.py`):** Donanım tedariğini beklemeden, yukarıdaki 11 baytlık paketi üreten ve sanal seri porta/UDP soketine periyodik ve alarm senaryolu veri basan simülatörü kodlamak.
2. **PyQt / PySide AFAD İzleme Arayüzü:**
   * 3 düğümün ağ durumunu ve bağlantı kalitesini gösteren panel.
   * MPU-6050 sismik açılarını gösteren yönelim göstergesi.
   * Düdük/vuruş algılandığında kırmızı flaşlı acil durum alarm bildirim penceresi.
3. **Mekanik Kutu Tasarımı:** IP67 buat kutusu ölçülerinin belirlenmesi ve SMA anten çıkış planlaması.

### 🔹 Emre BUDAK (DSP & Gömülü Yazılım / Kaptan)
1. **Örnekleme Altyapısı:** ESP32 üzerinde MAX4466 ile minimum 8 kHz örnekleme hızına sahip ADC zamanlayıcısını kurmak.
2. **arduinoFFT Algoritması:** Test düdüğü ile laboratuvar ortamında 2.5–3.5 kHz aralığındaki tepe frekansı yakalama testlerini yapmak.
3. **Paketleyici (Packer):** Algılanan frekans ve MPU-6050 verilerini 11 baytlık `TelemetryPacket` yapısına dönüştüren fonksiyonu hazırlamak.
4. **GitHub:** Ortak çalışma reposunu açıp dallanma (branch) kurallarını belirlemek.

### 🔹 Qusai NAAJEH (LoRa Mesh & Ağ Katmanı)
1. **P2P Donanım Testi:** İki ESP32 ve Ra-02 (433 MHz) modülü arasında SPI bağlantılarını kurup temel paket alıp-verme testini yapmak.
2. **RF Karakterizasyonu:** SF (Spreading Factor) değerlerine göre RSSI, SNR ve havada kalma süresi (ToA) ölçümlerini çıkarmak.
3. **Mesh Yönlendirme Taslağı:** Paketi aldığında `hop_count` değerini 1 artıran, aynı paketi mükerrer iletmeyen (duplicate packet rejection) basit aktarma kuralını yazmak.

---

## 🚀 Ekip Ortak Kararları (Pazartesi Gündemi)
* [ ] 11 Baytlık Telemetri protokolünün ekipçe onaylanması.
* [ ] GitHub deposunun açılması ve ilk commit'lerin atılması.
* [ ] TÜBİTAK 2209-A başvuru takvimi için proje metni taslağının bölünmesi.
