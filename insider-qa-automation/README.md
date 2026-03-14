# Insider QA Test Otomasyon Projesi

**Hazırlayan:** Alperen Yılmaz

Insider (insiderone.com) kariyer sayfası üzerinde QA iş ilanlarını test eden
Selenium tabanlı otomasyon projesidir. Proje **Page Object Model (POM)** deseni
kullanılarak Python ve pytest ile geliştirilmiştir.

---

## Kurulum

```bash
# sanal ortam olustur ve aktif et
python -m venv venv
venv\Scripts\activate        # windows
# source venv/bin/activate   # mac/linux

# bagimliliklari yukle
pip install -r requirements.txt
```

## Testleri Calistirma

```bash
# Chrome ile calistir (varsayilan)
pytest tests/test_insider_kariyer.py --browser=chrome

# Firefox ile calistir
pytest tests/test_insider_kariyer.py --browser=firefox
```

Tarayici secimi `--browser` parametresi ile yapilir. Desteklenen tarayicilar: **chrome**, **firefox**.

## Proje Yapisi

```
insider-qa-automation/
├── pages/
│   ├── __init__.py
│   ├── base_sayfa.py            # temel sayfa sinifi (ortak metodlar)
│   ├── anasayfa.py              # insider ana sayfa islemleri
│   ├── kariyer_sayfasi.py       # kariyer sayfasi navigasyonu ve filtreleme
│   └── is_listesi_sayfasi.py    # is ilanlari dogrulama ve lever yonlendirme
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # tarayici fixture, screenshot hook
│   └── test_insider_kariyer.py  # test senaryosu
├── screenshots/                 # hata durumunda alinan ekran goruntuleri
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## Test Senaryosu

| Adim | Aciklama |
|------|----------|
| 1 | insiderone.com ana sayfasini ac, navigasyon/hero/footer kontrolu yap |
| 2 | Kariyer sayfasina git → Explore open roles → See all teams → Quality Assurance → See all QA jobs → Istanbul + QA filtreleri uygula |
| 3 | Listelenen her ilanin pozisyon, departman ve lokasyon bilgilerini dogrula |
| 4 | View Role butonuna tikla, Lever basvuru formuna yonlendirildigini kontrol et |

## Onemli Notlar

- Test basarisiz olursa otomatik olarak `screenshots/` klasorune ekran goruntusu kaydedilir
- Tarayici secimi `--browser` parametresi ile yapilir (chrome / firefox)
- WebDriver surumu `webdriver-manager` ile otomatik yonetilir
- Proje POM (Page Object Model) desenine uygun olarak tasarlanmistir
