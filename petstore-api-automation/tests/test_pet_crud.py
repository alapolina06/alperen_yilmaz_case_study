import pytest

class TestPetCRUD:
    """Petstore API uzerindeki CRUD fonksiyonlarinin dogrulanmasi."""

    # ==========================
    # --- POZITIF SENARYOLAR ---
    # ==========================

    def test_pet_olustur_pozitif(self, api_istemcisi, ornek_pet_verisi):
        """Basarili bir sekilde yeni bir pet olusturur (CREATE)"""
        yanit = api_istemcisi.pet_olustur(ornek_pet_verisi)
        assert yanit.status_code == 200, f"Beklenmeyen durum kodu: {yanit.status_code}"
        
        gelen_veri = yanit.json()
        assert gelen_veri["name"] == ornek_pet_verisi["name"], "Olusan petin ismi eslesmiyor"
        assert gelen_veri["id"] == ornek_pet_verisi["id"], "Olusan petin ID'si eslesmiyor"

    def test_pet_getir_pozitif(self, api_istemcisi, ornek_pet_verisi):
        """Onceden olusturulan peti ID ile basariyla getirir (READ)"""
        # once peti olusturalim
        api_istemcisi.pet_olustur(ornek_pet_verisi)

        # simdi ayni id ile okuyalim
        yanit = api_istemcisi.pet_getir(ornek_pet_verisi["id"])
        
        assert yanit.status_code == 200, f"Pet okunamadi. Kod: {yanit.status_code}"
        assert yanit.json()["id"] == ornek_pet_verisi["id"], "Yanlis pet verisi dondu"

    def test_pet_guncelle_pozitif(self, api_istemcisi, ornek_pet_verisi):
        """Mevcut bir petin detaylarini gunceller (UPDATE)"""
        # once oluştur
        api_istemcisi.pet_olustur(ornek_pet_verisi)

        # ismi degistir
        guncel_veri = ornek_pet_verisi.copy()
        yeni_isim = "Yenilenmis Karabas"
        guncel_veri["name"] = yeni_isim

        # update (put) istegi
        yanit = api_istemcisi.pet_guncelle(guncel_veri)
        assert yanit.status_code == 200, f"Guncelleme basarisiz: {yanit.status_code}"

        # okuyarak degisikligi teyit et
        okunan_yanit = api_istemcisi.pet_getir(ornek_pet_verisi["id"])
        assert okunan_yanit.json()["name"] == yeni_isim, "Petin ismi guncellenememesi"

    def test_pet_sil_pozitif(self, api_istemcisi, ornek_pet_verisi):
        """Mevcut bir peti ID ile siler ve kaldirildigini dogrular (DELETE)"""
        # olustur
        api_istemcisi.pet_olustur(ornek_pet_verisi)
        pet_id = ornek_pet_verisi["id"]

        # sil
        silme_yanit = api_istemcisi.pet_sil(pet_id)
        assert silme_yanit.status_code == 200, "Pet silinemedi"

        # tekrar okumaya calis, 404 (Not Found) vermeli
        okuma_yanit = api_istemcisi.pet_getir(pet_id)
        assert okuma_yanit.status_code == 404, "Silinen pet hala okunabiliyor!"

    # ==========================
    # --- NEGATIF SENARYOLAR ---
    # ==========================

    def test_pet_olustur_negatif(self, api_istemcisi, gecersiz_pet_verisi):
        """Hatali tipte veriler iceren bir payload ile pet olusturulamaz"""
        yanit = api_istemcisi.pet_olustur(gecersiz_pet_verisi)
        
        # Petstore hatali veri geldiginde genelde HTTP 500 donuyor
        assert yanit.status_code in [400, 500], \
            f"Hatali veriye ragmen basarili dondu. Kod: {yanit.status_code}"

    def test_pet_getir_negatif(self, api_istemcisi):
        """Var olmayan veya tamamen rastgele bir ID istenirse bulunamaz"""
        # API uzerinde olmayan hayali bir ID uretiyoruz
        hayali_id = 9999999990099
        yanit = api_istemcisi.pet_getir(hayali_id)
        
        assert yanit.status_code == 404, \
            f"Var olmayan pet bulundu. Kod: {yanit.status_code}"

    def test_pet_guncelle_negatif(self, api_istemcisi, gecersiz_pet_verisi):
        """Bozuk yapida bir payload ile put (update) istegi yapilirsa basarisiz olmali"""
        yanit = api_istemcisi.pet_guncelle(gecersiz_pet_verisi)
        # Type mismatch olacagi icin hata donmeli
        assert yanit.status_code in [400, 404, 500], \
            f"Bozuk payload guncellendi olarak isaretlendi! Kod: {yanit.status_code}"

    def test_pet_sil_negatif(self, api_istemcisi):
        """Gecersiz bir ID formati dizesi silinmek istenirse hata vermeli"""
        yanit = api_istemcisi.pet_sil("BUNU_SİLEMEZSIN")
        
        # Petstore gecersiz ID stringi yolladigimizda 404 ve 400 (Bad request) durumunu donebilir
        assert yanit.status_code == 404, \
            f"Gecersiz ID formatina beklenmeyen bir kod dondu: {yanit.status_code}"
