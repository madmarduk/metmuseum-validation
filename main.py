# TODO: Разработать модели данных для валидации ответов Pydantic. Модели должны соответствовать
# структуре данных, возвращаемых API.
# TODO: Модель для списка произведений искусства
# Написать тесты с Pytest, которые вызывают API и проверяют:
    # TODO: Получение информации о произв-ии искусства по идентификатору
    # TODO: То, что API возвращает корректный HTTP статус
    # TODO: Убедиться, что возвр-мые данные соответствуют модели Pydantic для объекта
    # TODO: Обработку запроса с несуществ-им идентификатором
# Поиск произведений искусства (тоже тест с Pytest):
    # TODO: Поиск по ключевому слову возвращает коррект. результаты
    # TODO: Структура ответа соответствует ожиданиями и валидируется с Pydantic
    # TODO: Добавить логирование (запросов, ответов, ошибок)
# Доп проверки:
    # TODO: Ограничение на кол-во возвращаемых результатов
    # TODO: Работа фильтрации и сортировки результатов поиска (если предусмотрено API)

import requests
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from random import randint

class Artwork(BaseModel):
    objectID: int
    isHighlight: Optional[bool]
    accessionNumber: Optional[str]
    accessionYear: Optional[str]
    isPublicDomain: Optional[bool]
    primaryImage: Optional[str]
    primaryImageSmall: Optional[str]
    additionalImages: Optional[list]
    constituents: Optional[list]
    department: Optional[str]
    objectName: Optional[str]
    title: Optional[str]
    culture: Optional[str]
    period: Optional[str]
    dynasty: Optional[str]
    reign: Optional[str]
    portfolio: Optional[str]
    artistRole: Optional[str]
    artistPrefix: Optional[str]
    artistDisplayName: Optional[str]
    artistDisplayBio: Optional[str]
    artistSuffix: Optional[str]
    artistAlphaSort: Optional[str]
    artistNationality: Optional[str]
    artistBeginDate: Optional[str]
    artistEndDate: Optional[str]
    artistGender: Optional[str]
    artistWikidata_URL: Optional[str]
    artistULAN_URL: Optional[str]
    objectDate: Optional[str]
    objectBeginDate: Optional[int]
    objectEndDate: Optional[int]
    medium: Optional[str]
    dimensions: Optional[str]
    dimensionsParsed: Optional[dict] = None
    measurements: Optional[list]
    creditLine: Optional[str]
    geographyType: Optional[str]
    city: Optional[str]
    state: Optional[str]
    county: Optional[str]
    country: Optional[str]
    region: Optional[str]
    subregion: Optional[str]
    locale: Optional[str]
    locus: Optional[str]
    excavation: Optional[str]
    river: Optional[str]
    classification: Optional[str]
    rightsAndReproduction: Optional[str]
    linkResource: Optional[str]
    metadataDate: Optional[datetime]
    repository: Optional[str]
    objectURL: Optional[str]
    tags: Optional[list]
    objectWikidata_URL: Optional[str]
    isTimelineWork: Optional[bool]
    GalleryNumber: Optional[str]

def random_object_id():
    """
    Generates a random object ID by selecting a random ID from the list of available object IDs.

    Returns:
        str: The randomly selected object ID.

    Raises:
        requests.exceptions.RequestException: If there is an error making the API request.
    """
    obj_ids_response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
    obj_ids = obj_ids_response.json()
    return_id = obj_ids['objectIDs'][randint(1, len(obj_ids['objectIDs']))]
    return return_id

# Object request:
# https://collectionapi.metmuseum.org/public/collection/v1/objects/[objectID]

# TODO: Выбрать строки из модели, которые будут обязательными
obj_id = random_object_id()
url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(obj_id)
response = requests.get(url)
artwork_data = response.json()
artwork = Artwork.model_validate(artwork_data)
#print(artwork)