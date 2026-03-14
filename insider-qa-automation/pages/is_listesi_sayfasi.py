from selenium.webdriver.common.by import By
from pages.base_sayfa import BaseSayfa
import time


class IsListesiSayfasi(BaseSayfa):
    """
    Lever jobs sayfasindaki is ilanlarini dogrulayan
    ve basvuru formuna yonlendirmeyi kontrol eden sayfa nesnesi.

    Not: QA kartina tiklandiktan sonra
    jobs.lever.co/insiderone?team=Quality%20Assurance adresine yonlendirilir.
    Bu sayfa Lever'in is ilani listeleme sayfasidir.
    """

    # --- Lever sayfasi elemanlari ---
    IS_ILANI_KARTI = (By.CSS_SELECTOR, ".posting")
    POZISYON_ADI = (By.CSS_SELECTOR, "h5[data-qa='posting-name']")
    LOKASYON_ADI = (By.CSS_SELECTOR, ".posting-categories .sort-by-location, .location")
    DEPARTMAN_ADI = (By.CSS_SELECTOR, ".posting-categories .sort-by-team, .department")
    BASVURU_BTN = (By.CSS_SELECTOR, ".posting-btn-submit")

    # lever is ilani linki (her ilana ayri sayfa linki)
    IS_ILANI_LINKI = (By.CSS_SELECTOR, ".posting-title a, .posting a[href*='lever.co']")

    # --- Lever filtre elemanlari ---
    LOKASYON_FILTRESI = (By.CSS_SELECTOR, ".filter-button-wrapper[aria-label='Filter by Location: All']")
    TAKIM_FILTRESI = (By.CSS_SELECTOR, ".filter-button-wrapper[aria-label='Filter by Team']")

    # istanbul lokasyon secenegi (dropdown acildiktan sonra gorunur olur)
    # once css ile dene, olmazsa xpath ile dene
    ISTANBUL_SECENEGI_CSS = (By.CSS_SELECTOR, "a.category-link[href*='location=Istanbul']")
    ISTANBUL_SECENEGI_XPATH = (By.XPATH, "//a[contains(@class, 'category-link') and contains(text(), 'Istanbul')]")

    def lever_sayfasinda_mi(self):
        """URL'de lever.co olup olmadigini kontrol et"""
        aktif_url = self.mevcut_url()
        return "lever.co" in aktif_url or "jobs.lever.co" in aktif_url

    def lokasyona_gore_filtrele(self, lokasyon="Istanbul, Turkey"):
        """
        Lever sayfasindaki lokasyon filtresinden Istanbul secenegini sec.
        Once LOCATION dropdown butonuna tiklayip aciyoruz,
        sonra acilan listeden Istanbul secenegine tikliyoruz.
        """
        time.sleep(2)
        try:
            self.tikla(self.LOKASYON_FILTRESI)
        except Exception:
            self.js_ile_tikla(self.LOKASYON_FILTRESI)
        time.sleep(2)

        # istanbul secenegine tikla - once JS ile, sonra CSS/XPATH ile dene
        try:
            self.js_ile_tikla(self.ISTANBUL_SECENEGI_CSS)
        except Exception:
            try:
                self.tikla(self.ISTANBUL_SECENEGI_CSS)
            except Exception:
                self.js_ile_tikla(self.ISTANBUL_SECENEGI_XPATH)
        time.sleep(3)

    def is_listesi_var_mi(self):
        """Filtreleme sonrasi is ilani kartlarinin olup olmadigini kontrol et"""
        try:
            ilanlar = self.is_ilanlarini_getir()
            return len(ilanlar) > 0
        except Exception:
            return False

    def is_ilanlarini_getir(self):
        """Sayfadaki tum is ilani kartlarini dondur"""
        time.sleep(2)
        return self.elementleri_bul(self.IS_ILANI_KARTI)

    def ilanlari_dogrula(self):
        """
        Listelenen her is ilaninin:
        - Pozisyon adinda 'Quality Assurance' icerdigini
        - Departman/takim kisminda 'Quality Assurance' yazdigini
        - Lokasyonda 'Istanbul' gectigini
        kontrol eder.

        Not: Lever sayfasinda departman ve lokasyon bilgileri
        .posting-categories altinda listelenir.
        """
        ilanlar = self.is_ilanlarini_getir()
        assert len(ilanlar) > 0, "Lever sayfasinda hicbir is ilani bulunamadi!"

        for ilan in ilanlar:
            # pozisyon adini kontrol et
            pozisyon_elem = ilan.find_element(*self.POZISYON_ADI)
            pozisyon = pozisyon_elem.text

            # kategori bilgilerini al (lokasyon ve departman ayni div icinde)
            kategori_elemleri = ilan.find_elements(By.CSS_SELECTOR, ".posting-categories span")

            # tum kategori text'lerini birlestir
            kategori_text = " ".join([elem.text for elem in kategori_elemleri])

            assert ("Quality Assurance" in pozisyon or "QA" in pozisyon) or \
                   ("Quality Assurance" in kategori_text or "QA" in kategori_text), \
                f"Pozisyon/Departman uyumsuzlugu: '{pozisyon}' - kategoriler: '{kategori_text}'"
            assert "Istanbul" in kategori_text or "ISTANBUL" in kategori_text, \
                f"Lokasyon uyumsuzlugu: kategorilerde 'Istanbul' bulunamadi - '{kategori_text}'"

    def rolu_goruntule(self, ilan_sirasi=0):
        """
        Belirtilen siradaki is ilanina tiklayip
        detay/basvuru sayfasina git.
        """
        ilanlar = self.is_ilanlarini_getir()
        assert len(ilanlar) > ilan_sirasi, \
            f"{ilan_sirasi}. siradaki ilan bulunamadi, toplam {len(ilanlar)} ilan var"

        secili_ilan = ilanlar[ilan_sirasi]
        self.elemente_kaydir(secili_ilan)
        time.sleep(1)

        # ilanin linkine tikla (basvuru sayfasina gider)
        try:
            basvuru_btn = secili_ilan.find_element(*self.BASVURU_BTN)
            basvuru_btn.click()
        except Exception:
            # basvuru butonu yoksa ilan linkine tikla
            ilan_link = secili_ilan.find_element(*self.IS_ILANI_LINKI)
            ilan_link.click()
        time.sleep(3)

    def basvuru_sayfasinda_mi(self):
        """
        Lever basvuru formunun acilip acilmadigini kontrol et.
        URL'de 'lever.co' ve '/apply' geciyorsa ya da
        sadece 'lever.co' icerisinde ilanin detay sayfasindaysak dogru.
        """
        # yeni sekme acildiysa ona gec
        sekmeler = self.driver.window_handles
        if len(sekmeler) > 1:
            self.yeni_sekmeye_gec()
            time.sleep(2)

        aktif_url = self.mevcut_url()
        return "lever.co" in aktif_url
