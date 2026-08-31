"""Kombine sistem bahis hesaplama motoru.

Bu modül saf (Streamlit'e bağımlı olmayan) hesaplama fonksiyonlarını içerir,
bu sayede birim testlerle doğrulanabilir.
"""
from itertools import combinations

import pandas as pd

# Durum sabitleri
DURUM_BEKLIYOR = "Bekliyor"
DURUM_GELDI = "Geldi (Kazandı)"
DURUM_YATTI = "Yattı (Kaybetti)"
DURUM_IADE = "Koşmaz (İade)"

DURUM_SECENEKLERI = [DURUM_BEKLIYOR, DURUM_GELDI, DURUM_YATTI, DURUM_IADE]

BAHIS_TURLERI = [
    "Ganyan",
    "İlk 2",
    "İlk 3",
    "İlk 4",
    "İkili Bahis",
    "Sıralı İkili Bahis",
    "Kim Geçer?",
]

VARSAYILAN_ORANLAR = [5.50, 1.70, 25.00, 12.00, 3.50, 8.00, 15.00]

# Kolon birim fiyatı bu proje kapsamında sabittir (1 TL).
KOLON_BIRIM_FIYATI = 1.0

# İdare (United Racing), kombine sistem bahislerinde bir süreliğine Sistem
# 7'ye kadar izin verdikten kısa süre sonra bunu geri çekip yeniden 4 ayakla
# sınırladı. Ne zaman tekrar yükseltileceği belirsiz olduğu için alt yapı
# (hesaplama motoru, varsayılan oran/durum dizileri) 7'ye kadar hazır
# tutuluyor; arayüzde şu an yalnızca AKTIF_MAKS_AT_SAYISI kadarı açık.
# İdare limiti değiştiğinde tek yapılması gereken bu sabiti güncellemek.
AKTIF_MAKS_AT_SAYISI = 4
TEKNIK_MAKS_AT_SAYISI = 7

# Durum -> ikon eşlemesi
_DURUM_IKON = {
    DURUM_GELDI: "✅",
    DURUM_YATTI: "❌",
    DURUM_IADE: "↩️",
}


def durum_ikon(durum):
    """Bir atın durumuna göre gösterilecek ikonu döndürür."""
    return _DURUM_IKON.get(durum, "⏳")


def hesapla_bahis_sayisi(at_sayisi, secili_sistemler):
    """Seçili sistemlere göre toplam kolon (bahis) sayısını hesaplar."""
    toplam_kolon = 0
    at_dummy = list(range(at_sayisi))
    for r in range(1, at_sayisi + 1):
        if secili_sistemler.get(r, False):
            toplam_kolon += len(list(combinations(at_dummy, r)))
    return toplam_kolon


def hesapla_kupon_bedeli(bahis_sayisi, misli, birim_fiyat=KOLON_BIRIM_FIYATI):
    """Toplam kupon bedelini hesaplar."""
    return bahis_sayisi * birim_fiyat * misli


def hesapla_sistem_gruplari(at_listesi, col_count, secili_sistemler, misli):
    """Her sistem (r) için tüm kombinasyonları ve durumlarını hesaplar.

    Döndürülen değer: {sistem_no: pandas.DataFrame} sözlüğü.
    """
    gruplanmis_kombinasyonlar = {}

    for r in range(1, col_count + 1):
        if not secili_sistemler.get(r, False):
            continue

        kombinasyon_listesi = []

        for comb in combinations(at_listesi, r):
            kolon_orani = 1.0
            has_yatti = False
            has_bekliyor = False
            # Kombinasyondaki TÜM atlar "Koşmaz (İade)" ise kolon iade edilir;
            # tek bir Yattı/Bekliyor/Geldi atı bile bu durumu geçersiz kılar.
            tum_iade = True

            at_obj_listesi = []
            for at in comb:
                at_obj_listesi.append(
                    {
                        "ad": at["ad"],
                        "bahis_turu": at["bahis_turu"],
                        "durum": at["durum"],
                        "oran": at["oran"],
                    }
                )

                if at["durum"] == DURUM_YATTI:
                    has_yatti = True
                    tum_iade = False
                elif at["durum"] == DURUM_BEKLIYOR:
                    has_bekliyor = True
                    tum_iade = False
                    kolon_orani *= at["oran"]
                elif at["durum"] == DURUM_IADE:
                    pass  # oran etkisi yok (x1), tum_iade korunur
                else:  # DURUM_GELDI
                    tum_iade = False
                    kolon_orani *= at["oran"]

            if has_yatti:
                durum_str = "Kaybetti"
                durum_class = "lost"
                kazanc = 0.00
            elif has_bekliyor:
                durum_str = "Bekliyor"
                durum_class = "pending"
                kazanc = round(kolon_orani * misli, 2)
            elif tum_iade:
                durum_str = "İade"
                durum_class = "refund"
                kazanc = round(kolon_orani * misli, 2)
            else:
                durum_str = "Kazandı"
                durum_class = "won"
                kazanc = round(kolon_orani * misli, 2)

            kombinasyon_listesi.append(
                {
                    "Sistem": f"Sistem {r}",
                    "AtObjeleri": at_obj_listesi,
                    "Kolon Oranı": (
                        round(kolon_orani, 2) if not has_yatti else 0.00
                    ),
                    "Durum": durum_str,
                    "DurumClass": durum_class,
                    "Tahmini Kazanç": kazanc,
                }
            )

        gruplanmis_kombinasyonlar[r] = pd.DataFrame(kombinasyon_listesi)

    return gruplanmis_kombinasyonlar


def hesapla_ozet(df):
    """Bir DataFrame için kesinleşen / bekleyen / iade tutarlarını özetler."""
    if df.empty:
        return {"kesinlesen": 0.0, "bekleyen": 0.0, "iade": 0.0}

    kesinlesen = df.loc[df["Durum"] == "Kazandı", "Tahmini Kazanç"].sum()
    bekleyen = df.loc[df["Durum"] == "Bekliyor", "Tahmini Kazanç"].sum()
    iade = df.loc[df["Durum"] == "İade", "Tahmini Kazanç"].sum()
    return {
        "kesinlesen": float(kesinlesen),
        "bekleyen": float(bekleyen),
        "iade": float(iade),
    }
