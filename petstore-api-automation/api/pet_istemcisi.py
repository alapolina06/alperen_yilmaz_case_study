import requests


class PetIstemcisi:
    """
    Petstore Swagger API'si uzerindeki 'pet' endpoint'lerine
    istek atmak icin kullanilan araci sinif.
    """

    TABAN_URL = "https://petstore.swagger.io/v2"

    def __init__(self):
        self.basliklar = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def pet_olustur(self, veri):
        """POST /pet - Yeni bir pet olusturur"""
        url = f"{self.TABAN_URL}/pet"
        yanit = requests.post(url, json=veri, headers=self.basliklar)
        return yanit

    def pet_getir(self, pet_id):
        """GET /pet/{petId} - ID'si verilen peti getirir"""
        url = f"{self.TABAN_URL}/pet/{pet_id}"
        yanit = requests.get(url, headers=self.basliklar)
        return yanit

    def pet_guncelle(self, veri):
        """PUT /pet - Mevcut bir peti gunceller"""
        url = f"{self.TABAN_URL}/pet"
        yanit = requests.put(url, json=veri, headers=self.basliklar)
        return yanit

    def pet_sil(self, pet_id):
        """DELETE /pet/{petId} - ID'si verilen peti siler"""
        url = f"{self.TABAN_URL}/pet/{pet_id}"
        yanit = requests.delete(url, headers=self.basliklar)
        return yanit
