# 🏇 Kombine Sistem Bahis Simülatörü

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://kombine-sistem-hesaplayici.streamlit.app)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Kombine Sistem Bahis Simülatörü**, at yarışı ve spor bahislerindeki kombine sistem kuponlarının olası tüm kombinasyonlarını, kolon bedellerini ve anlık kazanç senaryolarını hesaplamak için geliştirilmiş etkileşimli bir web uygulamasıdır.

---

## 🚀 Öne Çıkan Özellikler

- **🎯 Esnek Sistem Motoru:** Kupondaki at sayısına göre Sistem 1'den başlayarak tüm kombinasyonları anında üretir. Alt yapı Sistem 7'ye kadar hazırdır; ancak İdare'nin (United Racing) güncel kombine bahis limiti gereği arayüzde şu an **Sistem 4**'e kadar açık — limit yükseltildiğinde tek bir ayarla yeniden genişletilebilir.
- **🎟️ Çift Görünüm Modu:** Kombinasyonları hem modern **Dijital Bilet (Kart)** mimarisinde hem de **Genişletilmiş Tablo** formatında inceleme imkanı.
- **🏷️ Akıllı Durum Rozetleri (Status-Aware):** Her at ve kolon için *Geldi (Kazandı ✅)*, *Bekliyor (⏳)*, *Yattı (Kaybetti ❌)* ve *Koşmaz (İade ↩️)* durumlarının bireysel ve zincirleme görselleştirilmesi.
- **🔍 Akıllı Filtreleme:** Canlı kalan, yalnızca kazanan, bekleyen, kaybeden veya iade edilen kolonları tek tıkla filtreleme.
- **🐎 Genişletilmiş Bahis Türleri:** Ganyan, İkili Bahis, Sıralı İkili Bahis ve **"Kim Geçer?"** dahil güncel bahis türü seçenekleri.
- **💰 Gelişmiş Finansal Kokpit:**
  - **✅ Garantilenen Kazanç:** Sonucu kesinleşen kombinasyonlardan elde edilen net tutar.
  - **⏳ Maksimum Olası Kazanç:** Devam eden/bekleyen tüm atların gelmesi durumundaki potansiyel ikramiye.
  - **📈 Dinamik ROI & Net Bakiye Analizi:** Kupon maliyetine oranla anlık kâr/zarar ve getiri yüzdesi (% ROI).
- **✨ Dahili Rehber & Versiyon Notları:** Uygulama içi modal pencereler (`@st.dialog`) ile kullanım rehberi ve sürüm notları.

---

## 🛠️ Kullanılan Teknolojiler

- **Python** — Temel mantık ve kombinasyon hesaplama motoru (`itertools`)
- **Streamlit** — Etkileşimli web arayüzü, Session State ve Modal yönetimi
- **Pandas** — Kombinasyon matrislerinin veri yapısı ve filtrelemesi
- **Streamlit-Analytics2** — Gizlilik odaklı kullanım analitiği

---

## 💻 Lokal Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1. Depoyu klonlayın:
   ```bash
   git clone [https://github.com/anilsanli/kombine-sistem-hesaplayici.git](https://github.com/anilsanli/kombine-sistem-hesaplayici.git)
   cd kombine-sistem-hesaplayici