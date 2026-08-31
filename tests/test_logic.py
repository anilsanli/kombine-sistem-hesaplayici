import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic import (  # noqa: E402
    AKTIF_MAKS_AT_SAYISI,
    BAHIS_TURLERI,
    DURUM_BEKLIYOR,
    DURUM_GELDI,
    DURUM_IADE,
    DURUM_YATTI,
    TEKNIK_MAKS_AT_SAYISI,
    hesapla_bahis_sayisi,
    hesapla_kupon_bedeli,
    hesapla_sistem_gruplari,
)


def at(ad, oran, durum, bahis_turu="Ganyan"):
    return {"ad": ad, "bahis_turu": bahis_turu, "oran": oran, "durum": durum}


class TestHesaplaBahisSayisi(unittest.TestCase):
    def test_secili_sistemlere_gore_kolon_sayisi(self):
        secili = {1: True, 2: True, 3: True, 4: False}
        # C(4,1) + C(4,2) + C(4,3) = 4 + 6 + 4 = 14
        self.assertEqual(hesapla_bahis_sayisi(4, secili), 14)

    def test_hicbir_sistem_secili_degilse_sifir(self):
        secili = {1: False, 2: False}
        self.assertEqual(hesapla_bahis_sayisi(2, secili), 0)


class TestHesaplaKuponBedeli(unittest.TestCase):
    def test_misli_ile_carpim(self):
        self.assertEqual(hesapla_kupon_bedeli(14, 2), 28.0)

    def test_varsayilan_birim_fiyat_bir_tl(self):
        self.assertEqual(hesapla_kupon_bedeli(10, 1), 10.0)


class TestHesaplaSistemGruplari(unittest.TestCase):
    def test_tum_atlar_geldi_ise_kazandi(self):
        atlar = [at("A", 2.0, DURUM_GELDI), at("B", 3.0, DURUM_GELDI)]
        gruplar = hesapla_sistem_gruplari(atlar, 2, {2: True}, misli=1)
        row = gruplar[2].iloc[0]
        self.assertEqual(row["Durum"], "Kazandı")
        self.assertAlmostEqual(row["Tahmini Kazanç"], 6.0)

    def test_bir_at_yatti_ise_kolon_kaybeder(self):
        atlar = [at("A", 2.0, DURUM_GELDI), at("B", 3.0, DURUM_YATTI)]
        gruplar = hesapla_sistem_gruplari(atlar, 2, {2: True}, misli=1)
        row = gruplar[2].iloc[0]
        self.assertEqual(row["Durum"], "Kaybetti")
        self.assertEqual(row["Tahmini Kazanç"], 0.0)

    def test_bekleyen_at_varsa_kolon_bekliyor(self):
        atlar = [at("A", 2.0, DURUM_GELDI), at("B", 3.0, DURUM_BEKLIYOR)]
        gruplar = hesapla_sistem_gruplari(atlar, 2, {2: True}, misli=1)
        row = gruplar[2].iloc[0]
        self.assertEqual(row["Durum"], "Bekliyor")
        self.assertAlmostEqual(row["Tahmini Kazanç"], 6.0)

    def test_tum_atlar_iade_ise_kolon_iade_edilir(self):
        # Regresyon testi: önceden bu kombinasyon yanlışlıkla "Kazandı" olarak
        # işaretleniyor ve kazanç = 1 * misli gösteriliyordu.
        atlar = [at("A", 5.0, DURUM_IADE), at("B", 3.0, DURUM_IADE)]
        gruplar = hesapla_sistem_gruplari(atlar, 2, {2: True}, misli=1)
        row = gruplar[2].iloc[0]
        self.assertEqual(row["Durum"], "İade")
        self.assertEqual(row["DurumClass"], "refund")

    def test_iade_at_diger_atlarin_oranini_etkilemez(self):
        # İade edilen at, kolon oranı hesaplamasından tamamen dışlanmalı (x1).
        atlar = [at("A", 4.0, DURUM_GELDI), at("B", 99.0, DURUM_IADE)]
        gruplar = hesapla_sistem_gruplari(atlar, 2, {2: True}, misli=1)
        row = gruplar[2].iloc[0]
        self.assertEqual(row["Durum"], "Kazandı")
        self.assertAlmostEqual(row["Kolon Oranı"], 4.0)
        self.assertAlmostEqual(row["Tahmini Kazanç"], 4.0)

    def test_tek_at_iade_ise_sistem_1_iade_gosterir(self):
        atlar = [at("A", 5.0, DURUM_IADE)]
        gruplar = hesapla_sistem_gruplari(atlar, 1, {1: True}, misli=1)
        row = gruplar[1].iloc[0]
        self.assertEqual(row["Durum"], "İade")

    def test_yatti_iade_ile_birlikteyse_yine_kaybeder(self):
        atlar = [at("A", 5.0, DURUM_YATTI), at("B", 3.0, DURUM_IADE)]
        gruplar = hesapla_sistem_gruplari(atlar, 2, {2: True}, misli=1)
        row = gruplar[2].iloc[0]
        self.assertEqual(row["Durum"], "Kaybetti")

    def test_secili_olmayan_sistem_sonuca_dahil_edilmez(self):
        atlar = [at("A", 2.0, DURUM_GELDI), at("B", 3.0, DURUM_GELDI)]
        gruplar = hesapla_sistem_gruplari(atlar, 2, {1: True, 2: False}, misli=1)
        self.assertNotIn(2, gruplar)
        self.assertIn(1, gruplar)
        self.assertEqual(len(gruplar[1]), 2)


class TestSistemLimitVeBahisTurleri(unittest.TestCase):
    def test_kim_gecer_bahis_turu_listede(self):
        self.assertIn("Kim Geçer?", BAHIS_TURLERI)

    def test_aktif_limit_teknik_limiti_asamaz(self):
        # İdare limiti (AKTIF_MAKS_AT_SAYISI) her zaman alt yapının
        # desteklediği teknik üst sınırı (TEKNIK_MAKS_AT_SAYISI) aşmamalı.
        self.assertLessEqual(AKTIF_MAKS_AT_SAYISI, TEKNIK_MAKS_AT_SAYISI)
        self.assertGreaterEqual(AKTIF_MAKS_AT_SAYISI, 2)


if __name__ == "__main__":
    unittest.main()
