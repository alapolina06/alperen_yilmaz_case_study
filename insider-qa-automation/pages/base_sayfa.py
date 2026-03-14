from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class BaseSayfa:
    """
    Tum sayfa nesnelerinin miras aldigi temel sinif.
    Ortak islemleri (tiklama, bekleme, scroll vs.) burada tanimliyoruz
    ki her sayfada tekrar tekrar yazmayalim.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def url_ac(self, url):
        """Verilen URL'yi tarayicida ac"""
        self.driver.get(url)

    def element_bul(self, locator):
        """Tek bir element bul, DOM'da varlik kontrolu yapar"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def elementleri_bul(self, locator):
        """Birden fazla element bul"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def tikla(self, locator):
        """Elemente tiklanabilir olmasini bekle ve tikla"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def js_ile_tikla(self, locator):
        """
        Normal click calismiyorsa javascript ile tiklama yap.
        Bazi elementler baska elementlerin arkasinda kalabiliyor,
        bu durumda JS click ise yariyor.
        """
        element = self.element_bul(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def gorunur_mu(self, locator, sure=10):
        """Elementin sayfada gorunur olup olmadigini kontrol et"""
        try:
            bekleme = WebDriverWait(self.driver, sure)
            bekleme.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def elemente_kaydir(self, element):
        """Sayfayi verilen elemente dogru kaydir"""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        time.sleep(0.5)

    def uzerine_gel(self, element):
        """Mouse ile elementin uzerine gel (hover)"""
        aksiyon = ActionChains(self.driver)
        aksiyon.move_to_element(element).perform()

    def mevcut_url(self):
        """Tarayicidaki aktif URL'yi dondur"""
        return self.driver.current_url

    def yeni_sekmeye_gec(self):
        """En son acilan sekmeye gec"""
        sekmeler = self.driver.window_handles
        self.driver.switch_to.window(sekmeler[-1])

    def url_icerik_kontrolu(self, metin, sure=15):
        """URL'nin belirli bir metin icermesini bekle"""
        WebDriverWait(self.driver, sure).until(EC.url_contains(metin))
