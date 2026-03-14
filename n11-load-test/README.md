# n11 Arama Modülü Yük Testi (Load Test)

**Hazırlayan:** Alperen Yılmaz

Bu proje, Python tabanlı popüler açık kaynaklı bir yük testi aracı olan **Locust** kullanılarak geliştirilmiştir. Amacı, `https://www.n11.com/` web sitesinin **arama modülünün** davranışlarını (gelen isteklere karşı stabilitesi, header cevapları vb.) incelemektir.

Proje, temel `task` (görev) tanımlarından oluşur ve bot korumalarına karşı gerçekçi davranması adına statik `User-Agent` ve `Accept` başlıklarıyla istek (HTTP/S) oluşturur.

---

## Senaryo Özeti

1. **`on_start` metodu:** Teste başlayan her sanal kullanıcı (User) öncelikle `/` taban dizinini (Ana Sayfa) ziyaret eder. Bu sayede sunucu tarafından "gerçek bir tarayıcı girişi" yapıldığı algılanır ve gerekli "session" (çerez) verileri toplanır.
2. **`arama_yap_bilgisayar`:** En yüksek ağırlıklı `task` yöntemidir. `/arama?q=bilgisayar` sorgusu oluşturur, HTTP 200 kodu bekler ve arama motorunun tepkisini analiz eder.
3. **`arama_yap_telefon`:** Daha düşük oncelikli (%25 ihtimal) alt bir arama simülasyonudur ve farklı cihaz/kategori araması davranışını test eder.

## Kurulum ve Çalıştırma Eğitimleri

Locust projesi tek bir Python dosyası üzerinden ayağa kalkar. Projeyi lokalinizde denemek için aşağıdaki adımları kullanabilirsiniz:

### 1. Ortam Kurulumu
Klasör dizininizde bir sanal ortam oluşturarak paketi yükleyin:

```bash
# Sanal Ortam Olusturun
python -m venv venv

# Platforma göre aktive edin (Windows icindir)
venv\Scripts\activate

# Locust bagimliliklarini yukleyin
pip install -r requirements.txt
```

### 2. Arayüz ile (Web UI) Çalıştırma
Locust varsayılan olarak `localhost:8089` üzerinde web-tabanlı, detaylı raporlar veren hoş bir arayüz ile kalkar. Bu özelliği aktif edip görmek için;

```bash
locust -f locustfile.py --host=https://www.n11.com
```

- Komut sonrası web tarayıcınızdan `http://localhost:8089/` adresine gidin.
- **Kullanıcı Sayısı:** *1* 
- **Saniyede Doğan Kullanıcı:** *1* 
Olarak ayarlayarak Start (Başlat) butonuna bastığınızda detaylı davranış metrikleri gelmeye başlayacaktır.

### 3. Arayüzsüz (Headless / Konsol) Çalıştırma
Case gereksinimi doğrultusunda sistemi sadece arka planda hızlı bir konsept testi (1 kullanıcı) yapmak isterseniz konsol modunu tetikleyebilirsiniz:

```bash
# Sadece 1 sanal kullanici ile 30 saniye boyunca calistir ve ozet rapor ver
locust -f locustfile.py --host=https://www.n11.com --headless -u 1 -r 1 -t 30s
```
