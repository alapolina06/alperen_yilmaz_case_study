import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    """Komut satirindan --browser parametresi alabilmek icin"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Testlerin calisacagi tarayici: chrome veya firefox"
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Her test fonksiyonu icin tarayici baslat.
    Test bitince tarayiciyi kapat.
    --browser parametresine gore Chrome veya Firefox acar.
    """
    tarayici = request.config.getoption("--browser").lower()

    if tarayici == "chrome":
        secenekler = webdriver.ChromeOptions()
        secenekler.add_argument("--start-maximized")
        secenekler.add_argument("--disable-notifications")
        surucu = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=secenekler
        )
    elif tarayici == "firefox":
        secenekler = webdriver.FirefoxOptions()
        secenekler.add_argument("--width=1920")
        secenekler.add_argument("--height=1080")
        surucu = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=secenekler
        )
    else:
        raise ValueError(f"Desteklenmeyen tarayici: {tarayici}")

    surucu.implicitly_wait(10)

    yield surucu

    surucu.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Test basarisiz olursa otomatik ekran goruntusu al.
    Goruntuler screenshots/ klasorune kaydedilir.
    """
    outcome = yield
    rapor = outcome.get_result()

    if rapor.when == "call" and rapor.failed:
        surucu = item.funcargs.get("driver", None)
        if surucu:
            ekran_goruntusu_klasoru = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "screenshots"
            )
            os.makedirs(ekran_goruntusu_klasoru, exist_ok=True)

            zaman_damgasi = datetime.now().strftime("%Y%m%d_%H%M%S")
            dosya_adi = f"{item.name}_{zaman_damgasi}.png"
            tam_yol = os.path.join(ekran_goruntusu_klasoru, dosya_adi)

            surucu.save_screenshot(tam_yol)
            print(f"\nEkran goruntusu kaydedildi: {tam_yol}")
