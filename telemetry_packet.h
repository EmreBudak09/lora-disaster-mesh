/**
 * @file telemetry_packet.h
 * @brief Afet Sonrası Çok Sekmeli LoRa Mesh ve Uçta Akustik Tespit Sistemi
 *        Standart 11-Baytlık İkili (Binary) Telemetri Protokol Başlık Dosyası (v1.0)
 * 
 * Bu başlık dosyası ESP32 (Arduino / PlatformIO) ve LoRa firmware tarafından kullanılır.
 */

#ifndef TELEMETRY_PACKET_H
#define TELEMETRY_PACKET_H

#include <stdint.h>

#define TELEMETRY_HEADER_BYTE   0xAA
#define TELEMETRY_PACKET_SIZE   11

// Mesaj Tipleri
typedef enum {
    MSG_TYPE_HEARTBEAT      = 0x01, // Normal Durum / Canlılık
    MSG_TYPE_ACOUSTIC_ALARM = 0x02, // Düdük veya Ritmik Vuruş Uyarısı
    MSG_TYPE_SEISMIC_ALERT  = 0x03  // Sismik Eğim / Çökme Uyarısı
} MessageType_t;

// Düğüm Rolleri
typedef enum {
    NODE_ROLE_RUBBLE        = 0x01, // Enkaz Altı Düğümü
    NODE_ROLE_RELAY         = 0x02, // Röle / Aktarıcı Düğümü
    NODE_ROLE_GATEWAY       = 0x03  // AFAD Koordinasyon İstasyonu
} NodeRole_t;

// 11 Baytlık Sıkıştırılmış C Struct (Hafıza hizalama boşlukları engellenmiştir)
typedef struct __attribute__((packed)) {
    uint8_t  header;       // 0xAA (Sabit Başlık Baytı)
    uint8_t  node_id;      // Düğüm Numarası (1: Enkaz, 2: Röle, 3: Gateway)
    uint8_t  msg_type;     // Mesaj Tipi (0x01: Kalp Atışı, 0x02: Ses Alarmı, 0x03: Sismik)
    int8_t   pitch;        // MPU-6050 Eğim Açısı (-90 ile +90 derece)
    int8_t   roll;         // MPU-6050 Dönme Açısı (-90 ile +90 derece)
    uint16_t peak_freq;    // FFT ile bulunan baskın frekans (Hz) - Little Endian
    uint8_t  confidence;   // Tespit Güven Yüzdesi (%0 - %100)
    uint8_t  hop_count;    // Sekme Sayısı (Mesh yönlendirme takibi)
    uint8_t  battery;      // Batarya Yüzdesi (%0 - %100)
    uint8_t  checksum;     // İlk 10 baytın XOR kontrol toplamı
} TelemetryPacket_t;

/**
 * @brief Paketin ilk 10 baytının XOR kontrol toplamını hesaplar.
 */
static inline uint8_t calculate_telemetry_checksum(const TelemetryPacket_t* pkt) {
    const uint8_t* ptr = (const uint8_t*)pkt;
    uint8_t chk = 0;
    for (int i = 0; i < 10; i++) {
        chk ^= ptr[i];
    }
    return chk;
}

#endif // TELEMETRY_PACKET_H
