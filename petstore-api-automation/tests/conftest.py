import pytest
from api.pet_istemcisi import PetIstemcisi
import random


@pytest.fixture(scope="session")
def api_istemcisi():
    """Tum testler boyunca ayni PetIstemcisi objesini dondurur"""
    return PetIstemcisi()


@pytest.fixture(scope="function")
def rastgele_pet_id():
    """Her test icin farkli bir ID olusturur ve cakismazligi garanti eder"""
    return random.randint(1000000, 9999999)


@pytest.fixture(scope="function")
def ornek_pet_verisi(rastgele_pet_id):
    """Testlerde kullanilacak standart ve dogru bir pet payload'i dondurur"""
    return {
        "id": rastgele_pet_id,
        "category": {
            "id": 1,
            "name": "Kopekler"
        },
        "name": "Karabas",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 1,
                "name": "Sevimli"
            }
        ],
        "status": "available"
    }


@pytest.fixture(scope="function")
def gecersiz_pet_verisi():
    """
    Negatif senaryolar icin hatali formatta bir payload dondurur.
    Ornegin ID bir harf veya beklenen formattan farkli.
    Not: Petstore API'si validation kismi biraz zayiftir ama
    tip (type) hatalarinda 500 veya 400 donebilir.
    """
    return {
        "id": "HATALI_ID_FORMATI",  # tamsayi olmali
        "name": ["Dizi icinde isim"], # string olmali
        "status": "bilinmiyor"
    }
