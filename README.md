# 🏇 Kombine Sistem Bahis Simülatörü

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Kombine Sistem Bahis Simülatörü**, at yarışı ve spor bahislerindeki kombine sistem kuponlarının olası tüm kombinasyonlarını, kolon bedellerini ve anlık kazanç senaryolarını hesaplamak için geliştirilmiş etkileşimli bir web uygulamasıdır.

---

## 🚀 Öne Çıkan Özellikler

- **🎯 Esnek Sistem Hesaplama:** Kuponda yer alan at sayısına göre Sistem 1, Sistem 2, Sistem 3 ve Sistem 4 kombinasyonlarını anında üretir.
- **📊 3 Aşamalı Durum Takibi:** Her bir at için *Geldi (Kazandı)*, *Bekliyor*, *Yattı (Kaybetti)* ve *Koşmaz (İade)* durumları seçilebilir.
- **💰 İki Aşamalı İkramiye Analizi:**
  - **✅ Garantilenen Kazanç:** Sonucu netleşen kombinasyonlardan elde edilen kesinleşmiş tutar.
  - **⏳ Maksimum Olası Kazanç:** Koşusu devam eden/bekleyen tüm atların gelmesi durumunda ulaşılabilecek toplam ikramiye.
- **🎨 Görsel ve İntuitif UI:** Kazanan (yeşil), bekleyen (sarı) ve yatan (kırmızı) kombinasyonlar için dinamik tablo renklendirmesi.
- **🌗 Tam Cihaz Uyumlu Tasarım:** Karanlık mod (Dark Mode) ve açık mod çakışmalarını önleyen özel CSS ve tema mimarisi.

---

## 🛠️ Kullanılan Teknolojiler

- **Python** — Temel mantık ve kombinasyon hesaplama motoru (`itertools`)
- **Streamlit** — Etkileşimli web arayüzü ve session state yönetimi
- **Pandas** — Kombinasyon tablolarının veri yapısı ve filtrelemesi

---

## 💻 Lokal Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/anilsanli/kombine-sistem-hesaplayici.git
   cd kombine-sistem-hesaplayici
   ```

2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Uygulamayı başlatın:
   ```bash
   streamlit run app.py
   ```

---

## 📂 Proje Yapısı

```text
├── .streamlit/
│   └── config.toml      # Açık tema zorlaması ve arayüz konfigürasyonu
├── app.py               # Uygulamanın tüm arayüz ve hesaplama kodları
├── requirements.txt     # Bağımlılık listesi (streamlit, pandas)
└── README.md            # Proje dokümantasyonu
```

---

## 👨‍💻 Geliştirici

**Anıl Şanlı**  
Data Analyst / Data Science Masters Student

- **LinkedIn:** [https://www.linkedin.com/in/anilsanli](https://www.linkedin.com/in/anilsanli)
- **GitHub:** [https://github.com/anilsanli](https://github.com/anilsanli)

---

## 📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.
