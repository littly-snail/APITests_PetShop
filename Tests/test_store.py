import allure
import jsonschema
import requests
from .Schemas.order_schema import ORDER_SCHEMA
from .Schemas.inventory_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_create_order(self):
        with allure.step("Подготовка данных для создания заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            n_order = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответ не совпал с ожидаемым"
            jsonschema.validate(n_order, ORDER_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert n_order["id"] == payload["id"], "id заказа не совпал с ожидаемым"
            assert n_order["petId"] == payload["petId"], "id питомца не совпал с ожидаемым"
            assert n_order["quantity"] == payload["quantity"], "количество в заказе не совпало с ожидаемым"
            assert n_order["status"] == payload["status"], "статус заказа не совпал с ожидаемым"
            assert n_order["complete"] == payload["complete"], "отметка выполнения не совпала с ожидаемой"


    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        with allure.step("Получение ID созданного в фикстуре заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответ не совпал с ожидаемым"
            assert response.json()["id"] == order_id, "id заказа не совпал с ожидаемым"


    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Получение ID созданного в фикстуре заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление заказа"):
            delete_response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert delete_response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            get_response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка, что заказ больше недоступен по ID"):
            assert get_response.status_code == 404, "Код ответа не совпал с ожидаемым"


    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение несуществующего заказа"):
            order_id = 9999
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответ не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Order not found", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответ не совпал с ожидаемым"
            assert isinstance(response.json(), dict)
            jsonschema.validate(response.json(), INVENTORY_SCHEMA)