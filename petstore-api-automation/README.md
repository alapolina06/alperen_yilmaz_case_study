# Petstore API Test Otomasyon Projesi

**Hazırlayan:** Alperen Yılmaz

Swagger UI üzerinde sağlanan (https://petstore.swagger.io/) **Pet** endpointlerinin otomatik olarak test edilmesini sağlayan otomasyon script'idir. Python ve `requests` ile geliştirilmiş olup, test koşucusu olarak `pytest` kullanılmış, testler tamamen **Türkçe yapılandırılmıştır**.

---

## Kurulum ve Çalıştırma

### Bağımlılıkların Yüklenmesi
Projeyi çalıştırmadan önce izole bir sanal ortam oluşturmanız önerilir:

```bash
# sanal ortam oluştur ve başlat
python -m venv venv
venv\Scripts\activate   # Windows icindir. (Mac/Linux için: source venv/bin/activate)

# projeye özgü bağımlılıkları yükle (requests ve pytest)
pip install -r requirements.txt
```

### Testleri Çalıştırma
Tüm testler `tests/` dizininin altındadır. Pytest komutunu kullanarak testi başlatabilirsiniz:

```bash
pytest
```
veya daha detaylı çıktı (verbose) için:
```bash
pytest -v
```

## Proje Klasör Planı

```
petstore-api-automation/
├── api/
│   ├── __init__.py
│   └── pet_istemcisi.py      # HTTP Request'lerini barindan POM benzeri API sinifi
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Rastgele test verisi ureten ve API client saglayan fixturelar
│   └── test_pet_crud.py      # Pozitif ve negatif Pet API senaryolari 
├── requirements.txt          # Proje bağımlılıkları
├── pytest.ini                # Pytest konfigürasyon dosyasi
├── .gitignore                # Git çöp kutusu dosyaları koruyucu
└── README.md                 # Detayli proje kullanım ve analiz rehberi
```

## Senaryolar

Her bir CRUD işlemi 2 koşula göre doğrulanır:

1. **Pozitif Senaryo (Happy Path):** Doğru veriler (payload / path param) kullanıldığında dönen `200` cevaplarını ve body doğrulamasını kontrol eder.
   - P1: Yeni (eşsiz ID'li) hayvan oluştur (Create)
   - P2: ID ile oluşturulan hayvanı hatasız getir (Read)
   - P3: Mevcut hayvanın herhangi bir parametresini değiştir (Update)
   - P4: Silinen hayvancığın daha sonradan çağrıldığında 404 (Not Found) ile gelmemesini teyit et (Delete)

2. **Negatif Senaryo (Exception Handling):** Sistemin bozuk isteklere, geçersiz (tipik olmayan JSON) veri türlerine beklendiği gibi hata verdiğini denetler. 
   - N1: Hatalı format verisiyle Post 
   - N2: Var olmayan ID'yle Get 
   - N3: Yıkıksal payload ile Put
   - N4: Kabul edilemeyecek silme denemesi
