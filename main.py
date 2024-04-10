# TODO: Разработать модели данных для валидации ответов. Модели должны соответствовать
# структуре данных, возвращаемых API.
# TODO: Модель для объекта произведения искусства (ID, название, автор, дата)
# TODO: Модель для списка произведений искусства
# Написать тесты с Pytest, которые вызывают API и проверяют:
    # TODO: Получение информации о произв-ии искусства по идентификатору
    # TODO: То, что API возвращает корректный HTTP статус
    # TODO: Убедиться, что возвр-мые данные соотв-уют модели Pydantic для объекта
    # TODO: Обработку запроса с несуществ-им идентификатором
# Поиск произведений искусства (тоже тест с Pytest):
    # TODO: Поиск по ключевому слову возвращает коррект. результаты
    # TODO: Структура ответа соотв-ует ожиданиями и валидируется с Pydantic
    # TODO: Добавить логирование (запросов, ответов, ошибок)
# Доп проверки:
    # TODO: Ограничение на кол-во возвращаемых результатов
    # TODO: Работа фильтрации и сортировки результатов поиска (если предусмотрено API)

import requests
#payload = {}
url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
response = requests.get(url)
print(response.text)
