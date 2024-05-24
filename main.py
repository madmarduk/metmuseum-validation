# TODO: Выбрать строки из модели, которые будут обязательными
# Доп проверки:
    # TODO: Работа фильтрации и сортировки результатов поиска (если предусмотрено API)
# FIXME: Maybe cut back on using redundant temporary vars that are being replaced

import requests
import logging
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from random import randint

# TODO: Разобраться....
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('log.txt')
console_handler = logging.StreamHandler()
file_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


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
    # FIXME: Просто предложение самому себе в будущем, но возможно здесь стоит обращаться к get_artworks() (но я не уверен, потом на подумать)
    url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
    try:
        obj_ids_response = requests.get(url)
        logger.info(f"Отправлен запрос списка объектов на сервер музея")
        obj_ids_response.raise_for_status()
        logger.info(f"Получен ответ от сервера музея")
        obj_ids = obj_ids_response.json()
        return_id = obj_ids['objectIDs'][randint(1, len(obj_ids['objectIDs']))]
        logger.info(f"Получен случайный ID: {return_id}")
        return return_id
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при получении случайного ID: {e}")
        raise


def get_artworks():
    """Retrieves list of artwork objects"""
    url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
    try:
        response = requests.get(url)
        logger.info(f"Отправлен запрос списка объектов на сервер музея")
        response.raise_for_status()
        logger.info(f"Получен ответ от сервера музея")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при получении списка произведения искусств: {e}")


def validate_artworks_list(artworks_list):
    """
    Validates a list of artworks.
    
    Args:
        artworks_list (Response): The response object containing the list of artworks.
    
    Returns:
        artworks: The validated list of artworks.
    """
    try:
        artworks_list_json = artworks_list.json()
        artworks = ArtworksList.model_validate(artworks_list_json)
        logger.info(f"Успешная валидация списка объектов")
        return artworks
    except Exception as e:
        logger.error(f"Ошибка валидации списка произведений искусства: {e}")



def get_artwork_object(obj_id):
    """
    Retrieves an artwork object from the Met Museum API based on the provided object ID.

    Args:
        obj_id (int): The ID of the artwork object to retrieve.

    Returns:
        response: The response object of an artwork from the API.

    Raises:
        requests.exceptions.RequestException: If there is an error making the API request.
    """
    url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(obj_id)    
    try:
        response = requests.get(url)
        logger.info(f"Отправлен запрос на сервер на получение объекта с ID {obj_id}")
        response.raise_for_status()
        logger.info(f"Получено произведение искусства с ID {obj_id}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при получении произведения искусства с ID {obj_id}")
        raise


def validate_artwork(artwork_object):
    """
    Validates an artwork object from response object.

    Args:
        artwork_object (Artwork): The artwork object to be validated.

    Returns:
        artwork: The validated artwork object.
    """
    try:
        artwork_object_json = artwork_object.json()
        artwork = Artwork.model_validate(artwork_object_json)
        return artwork
    except Exception as e:
        logger.error(f"Ошибка валидации произведения искусства: {e}")
    

def query_search(keyword):
    """
    Make a search request to API using given keyword.

    Args:
        keyword (str): The keyword to search for.

    Returns:
        response (requests.Response): The response object containing the search results.
    """
    url = "https://collectionapi.metmuseum.org/public/collection/v1/search?q=" + str(keyword)
    try:
        response = requests.get(url)
        logger.info(f"Отправлен запрос на поиск по запросу {keyword}")
        response.raise_for_status()
        logger.info(f"Поиск по '{keyword}' вернул {response.json().get('total')} результатов")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при поиске по запросу '{keyword}: {e}")
        raise


# url = "https://collectionapi.metmuseum.org/public/collection/v1/search?q=sunflowers"
# response = requests.get(url)
# print(response.json())