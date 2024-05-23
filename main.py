# TODO: Выбрать строки из модели, которые будут обязательными
# Написать тесты с Pytest, которые вызывают API и проверяют:
# Получение информации о произв-ии искусства по идентификатору
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
from typing import Optional, List
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


class ArtworksList(BaseModel):
    total: int
    objectIDs: List[int]


def get_random_object_id():
    """Returns a random object ID by selecting a random ID from the list of available object IDs."""
    obj_ids_response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
    obj_ids = obj_ids_response.json()
    return_id = obj_ids['objectIDs'][randint(1, len(obj_ids['objectIDs']))]
    return return_id


def get_artworks():
    """Returns validated list of objects in Museum"""
    response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
    artworks_list = ArtworksList.model_validate(response.json())
    return artworks_list


def get_artwork_object(obj_id):
    """
    Retrieves an artwork object from the Met Museum API based on the provided object ID.

    Parameters:
        obj_id (int): The ID of the artwork object to retrieve.

    Returns:
        response: The response object of an artwork from the API.

    Raises:
        requests.exceptions.RequestException: If there is an error making the API request.
    """
    url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(obj_id)    
    response = requests.get(url)
    return response


def validate_artwork():
    """Returns validated artwork from response object."""
    artwork_object = get_artwork_object(obj_id=get_random_object_id()) # response object
    artwork_object_json = artwork_object.json()
    artwork = Artwork.model_validate(artwork_object_json)
    return artwork
    

# FIXME: Разобраться с тем, где должна стоять переменная для ID объекта (она должна быть одной и той же и для функции теста и для вызова в main)
def test_api_status():
    """Test whether API gives correct response."""
    assert get_artwork_object(get_random_object_id()).status_code == 200

def test_api_nonexistent_id():
    # На подумать: в задании написано "Обработку запроса
    #  с несуществ-им идентификатором". Может имеется в виду другое?
    """Test case for non-existent ID."""
    assert get_artwork_object(9999999).status_code == 404


def test_artwork_validation():
    """Test whether artwork object could be validated."""
    assert validate_artwork() is not None
    

print("kek")
