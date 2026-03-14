from selenium.webdriver.common.by import By
from pages.base_sayfa import BaseSayfa


class AnaSayfa(BaseSayfa):
    """
    Insider ana sayfa (insiderone.com) icin sayfa nesnesi.
    Ana sayfanin acildigini ve temel bloklarin yuklendigini dogrular.
    """

    URL = "https://insiderone.com/"

    # --- Sayfa Elemanlari (Locator'lar) ---
    NAV_BAR = (By.CSS_SELECTOR, "nav, #navigation, .navbar")
    HERO_BOLUMU = (By.CSS_SELECTOR, "#hero-section, .hero-section, [class*='hero'], header + section, header + div > section")
    FOOTER = (By.CSS_SELECTOR, "footer")
    CEREZ_KABUL_BTN = (By.CSS_SELECTOR, "#wt-cli-accept-all-btn, [id*='accept'], a[id*='cookie']")

    def anasayfayi_ac(self):
        """insiderone.com adresini ac"""
        self.url_ac(self.URL)

    def cerezleri_kabul_et(self):
        """Cerez uyari banner'i cikiyorsa kabul et"""
        try:
            self.tikla(self.CEREZ_KABUL_BTN)
        except Exception:
            # cerez banneri her zaman cikmiyor, hata vermeden devam et
            pass

    def anasayfa_acildi_mi(self):
        """URL'de insiderone.com olup olmadigini kontrol et"""
        return "insiderone.com" in self.mevcut_url()

    def navigasyon_yuklendi_mi(self):
        """Ust navigasyon barinin gorunur oldugunu dogrula"""
        return self.gorunur_mu(self.NAV_BAR)

    def hero_yuklendi_mi(self):
        """Hero (ana gorsel) bolumunun yuklenmesini kontrol et"""
        return self.gorunur_mu(self.HERO_BOLUMU)

    def footer_yuklendi_mi(self):
        """Sayfanin alt kismindaki footer'in yuklendigini dogrula"""
        return self.gorunur_mu(self.FOOTER, sure=15)
