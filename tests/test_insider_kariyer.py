import pytest
import time
from pages.anasayfa import AnaSayfa
from pages.kariyer_sayfasi import KariyerSayfasi
from pages.is_listesi_sayfasi import IsListesiSayfasi


class TestInsiderKariyer:
    """
    Insider kariyer sayfasi test senaryosu.

    Test adimlari:
    1. insiderone.com ana sayfasini ac, temel bloklarin yuklendigini dogrula
    2. Kariyer sayfasina git, QA departmanini bul, Lever is ilanlari sayfasina ulas
    3. Listelenen ilanlarin pozisyon/departman/lokasyon bilgilerini kontrol et
    4. Is ilanina tiklayip Lever basvuru sayfasina yonlendirildigini dogrula
    """

    def test_insider_qa_is_ilanlari(self, driver):
        """Insider QA kariyer akisini bastan sona dogrulayan test"""

        # ====== Adim 1: Ana sayfayi ac ve kontrol et ======
        anasayfa = AnaSayfa(driver)
        anasayfa.anasayfayi_ac()
        anasayfa.cerezleri_kabul_et()

        assert anasayfa.anasayfa_acildi_mi(), \
            "Insider ana sayfasi acilamadi"
        assert anasayfa.navigasyon_yuklendi_mi(), \
            "Navigasyon bari gorunmuyor"
        assert anasayfa.hero_yuklendi_mi(), \
            "Hero bolumu yuklenemedi"
        assert anasayfa.footer_yuklendi_mi(), \
            "Footer bolumu yuklenemedi"

        # ====== Adim 2: Kariyer sayfasina git, QA departmanina ulas ======
        # explore open roles -> see all teams -> quality assurance karti
        kariyer = KariyerSayfasi(driver)
        kariyer.kariyer_sayfasini_ac()
        time.sleep(2)

        kariyer.qa_kariyerine_git()

        # QA kartina tiklandiktan sonra lever sayfasina yonlendiriliriz
        is_listesi = IsListesiSayfasi(driver)
        assert is_listesi.lever_sayfasinda_mi(), \
            f"Lever sayfasina yonlendirilemedi. URL: {driver.current_url}"

        # lokasyonu Istanbul olarak filtrele
        is_listesi.lokasyona_gore_filtrele("Istanbul, Turkey")

        # filtreleme sonrasi is ilanlarinin gorunurlugunu kontrol et
        assert is_listesi.is_listesi_var_mi(), \
            "Filtreleme sonrasi is ilanlari listesi gorunmuyor"

        # ====== Adim 3: Is ilanlarinin iceriklerini dogrula ======
        is_listesi.ilanlari_dogrula()

        # ====== Adim 4: Is ilanina tiklayip basvuru sayfasini kontrol et ======
        is_listesi.rolu_goruntule(ilan_sirasi=0)

        assert is_listesi.basvuru_sayfasinda_mi(), \
            f"Lever basvuru sayfasi acilamadi. URL: {driver.current_url}"
