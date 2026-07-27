import allure
import jsonschema
import requests
from .Schemas.pet_schema import PET_SCHEMA
import pytest

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответ не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответ не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение несуществующего питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответ не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания нового питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response.json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответ не совпал с ожидаемым"
            jsonschema.validate(response.json, PET_SCHEMA)

        with allure.step("Проверка параметров питомцев в ответе"):
            assert response.json["id"] == payload["id"], "id питомца не совпал с ожидаемым"
            assert response.json["name"] == payload["name"], "имя питомца не совпало с ожидаемым"
            assert response.json["status"] == payload["status"], "статус питомца не совпал с ожидаемым"


    @allure.title("Добавление нового питомца c полными данными")
    def test_add_full_pet(self):
        with allure.step("Подготовка данных для создания нового питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [
                    {
                    "id": 0,
                    "name": "string"
                    }
                ],
                "status": "available"
                }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response.json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответ не совпал с ожидаемым"
            jsonschema.validate(response.json, PET_SCHEMA)

        with allure.step("Проверка параметров питомцев в ответе"):
            assert response.json["id"] == payload["id"], "id питомца не совпал с ожидаемым"
            assert response.json["name"] == payload["name"], "имя питомца не совпало с ожидаемым"
            assert response.json["category"]["id"] == payload["category"]["id"], "id категории не совпал с ожидаемым"
            assert response.json["category"]["name"] == payload["category"]["name"], "имя категории не совпало с ожидаемым"
            assert response.json["photoUrls"] == payload["photoUrls"], "ссылки на фотографии не совпали с ожидаемыми"
            assert response.json["tags"][0]["id"] == payload["tags"][0]["id"], "id тэга не совпал с ожидаемыми"
            assert response.json["tags"][0]["name"] == payload["tags"][0]["name"], "имя тэга не совпало с ожидаемыми"
            assert response.json["status"] == payload["status"], "статус питомца не совпал с ожидаемым"


    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответ не совпал с ожидаемым"
            assert response.json()["id"] == pet_id, "id питомца не совпал с ожидаемым"


    @allure.title("Обновление информации о питомце")
    def test_update_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления питомца"):
            payload2 = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка запроса на обновление питомца"):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload2)
            response.json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответ не совпал с ожидаемым"

        with allure.step("Проверка параметров питомцев в ответе"):
            assert response.json["id"] == pet_id, "id питомца не совпал с ожидаемым"
            assert response.json["name"] == payload2["name"], "имя питомца не совпало с ожидаемым"
            assert response.json["status"] == payload2["status"], "статус питомца не совпал с ожидаемым"


    @allure.title("Удаление питомца по ID")
    def test_delete_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление питомца"):
            delete_response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert delete_response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            get_response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка, что питомец больше недоступен по ID"):
            assert get_response.status_code == 404, "Код ответа не совпал с ожидаемым"


    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold", 200),
            ("stolen", 400),
            ("", 400)
        ]
    )
    def test_get_pets_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response = requests.get(url=f"{BASE_URL}/pet/findByStatus", params={"status": status})
            pets = response.json()

        with allure.step("Проверка содержимого ответа для корректного запроса"):
            if response.status_code == 200:
                assert isinstance(pets, list)
                assert len(pets) > 0, "Список питомцев пуст"
                for pet in pets:
                    assert pet["status"] == status, "статус питомца не совпал с ожидаемым"

        with allure.step("Проверка содержимого ответа для НЕкорректного запроса"):
            if response.status_code == 400:
                assert isinstance(pets, dict)
                assert "Input error" in pets["message"]

