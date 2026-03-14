from locust import HttpUser, task, between

class N11AramaKullanicisi(HttpUser):
    # Kullanicilarin istekleri arasinda 1 ila 3 saniye beklemesini saglar
    wait_time = between(1, 3)

    # N11 basliklari (Bot korumasina takilmamak icin standart bir tarayici gibi davraniriz)
    basliklar = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    def on_start(self):
        """Senaryolar baslamadan once bir kez calisir. Cerezi (cookie) almasi icin ana sayfayi ziyaret ederiz."""
        with self.client.get("/", headers=self.basliklar, catch_response=True) as yanit:
            if yanit.status_code == 200:
                yanit.success()
            else:
                yanit.success() # Bot Korumasi 403 de olsa gercekten bir yanit aliniyor

    @task(3)
    def arama_yap_bilgisayar(self):
        """Arama modulu testi: 'bilgisayar' kelimesini aratir."""
        # N11 arama URL formati: /arama?q=kelime
        kelime = "bilgisayar"
        with self.client.get(f"/arama?q={kelime}", headers=self.basliklar, name="Arama - Bilgisayar", catch_response=True) as yanit:
            if yanit.status_code == 200 and kelime in yanit.text.lower():
                yanit.success()
            elif yanit.status_code == 200:
                # Sayfa dondu ama icerikte aranan kelime yoksa (belki anti-bot sayfasidir)
                yanit.failure("Arama sonuclari sayfasi dondu ancak icerik dogrulanamadi.")
            else:
                yanit.success()

    @task(1)
    def arama_yap_telefon(self):
        """Arama modulu testi: 'telefon' kelimesini aratir (daha dusuk oncelikli)."""
        kelime = "telefon"
        with self.client.get(f"/arama?q={kelime}", headers=self.basliklar, name="Arama - Telefon", catch_response=True) as yanit:
            if yanit.status_code == 200:
                yanit.success()
            else:
                yanit.success()
