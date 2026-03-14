from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_sayfa import BaseSayfa
import time


class KariyerSayfasi(BaseSayfa):
    """
    Insider kariyer sayfasi icin sayfa nesnesi.
    Careers sayfasinda acik rollere gitme, tum takimlari gorme
    ve Quality Assurance departmanina navigasyon islemlerini yapar.

    Akis:
    1) insiderone.com/careers acilir
    2) 'Explore open roles' ile roller bolumune scroll yapilir
    3) 'See all teams' ile tum takimlar acilir
    4) Quality Assurance kartindaki link ile lever jobs sayfasina gidilir
    """

    KARIYER_URL = "https://insiderone.com/careers/"

    # --- Sayfa Elemanlari ---
    # careers sayfasindaki butonlar
    ROLLERI_INCELE_BTN = (By.CSS_SELECTOR, "a.inso-btn.inso-btn-primary[href='#open-roles']")
    TUM_TAKIMLARI_GOR_BTN = (By.CSS_SELECTOR, "a.inso-btn.see-more")

    # QA takim karti - see all teams'den sonra gorunur olur
    QA_TAKIM_LINK = (By.CSS_SELECTOR, "a.insiderone-icon-cards-grid-item-btn[href*='Quality']")

    # kullanicinin verdigi xpath (yedek olarak)
    QA_TAKIM_LINK_XPATH = (By.XPATH, '//*[@id="open-roles"]/div/div/div/div[3]/div[7]/div[3]/div/a')

    def kariyer_sayfasini_ac(self):
        """Insider kariyer sayfasini ac"""
        self.url_ac(self.KARIYER_URL)

    def qa_kariyerine_git(self):
        """
        Kariyer sayfasindan QA is ilanlarina ulasmak icin:
        1) 'Explore open roles' butonuna tikla (roller bolumune scroll yapar)
        2) 'See all teams' butonuna tikla (tum departtmanlar gorunur olur)
        3) Quality Assurance kartindaki linke tikla (lever sayfasina gider)
        """
        # 1. explore open roles butonuna tikla
        time.sleep(2)
        rolleri_incele = self.wait.until(
            EC.element_to_be_clickable(self.ROLLERI_INCELE_BTN)
        )
        self.elemente_kaydir(rolleri_incele)
        time.sleep(1)
        self.js_ile_tikla(self.ROLLERI_INCELE_BTN)
        time.sleep(2)

        # 2. see all teams butonuna tikla
        tum_takimlar = self.wait.until(
            EC.element_to_be_clickable(self.TUM_TAKIMLARI_GOR_BTN)
        )
        self.elemente_kaydir(tum_takimlar)
        time.sleep(1)
        self.js_ile_tikla(self.TUM_TAKIMLARI_GOR_BTN)
        time.sleep(2)

        # 3. quality assurance kartina tikla
        # once css selector ile dene, olmazsa xpath ile dene
        try:
            qa_link = self.wait.until(
                EC.presence_of_element_located(self.QA_TAKIM_LINK)
            )
        except Exception:
            qa_link = self.wait.until(
                EC.presence_of_element_located(self.QA_TAKIM_LINK_XPATH)
            )

        self.elemente_kaydir(qa_link)
        time.sleep(1)
        qa_link.click()
        time.sleep(3)
