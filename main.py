import logging
from datetime import datetime
from random import randint
from typing import Optional, List

import requests
from pydantic import BaseModel


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("log.txt")
console_handler = logging.StreamHandler()
file_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class Artwork(BaseModel):
    objectID: int
    isHighlight: bool
    accessionNumber: Optional[str]
    accessionYear: Optional[str]
    isPublicDomain: bool
    primaryImage: str
    primaryImageSmall: Optional[str]
    additionalImages: Optional[list]
    constituents: Optional[list]
    department: str
    objectName: str
    title: str
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
    """
    Returns a random object ID by selecting a random ID from the list of 
    available object IDs.
    """
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
        artworks_list (Response): The response object containing the
        list of artworks.
    
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
    Retrieves an artwork object from the Met Museum API based on the provided
    object ID.

    Args:
        obj_id (int): The ID of the artwork object to retrieve.

    Returns:
        response: The response object of an artwork from the API.
    """
    url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(obj_id)    
    try:
        response = requests.get(url)
        logger.info(f"Отправлен запрос на сервер на получение объекта с ID {obj_id}")
        response.raise_for_status()
        logger.info(f"Получено произведение искусства с ID {obj_id}")
        return response
    except Exception as e:
        logger.error(f"Ошибка при получении произведения искусства с ID {obj_id}")
        return response        


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


def query_search(q, isHighlight=None, title=None, tags=None, departmentId=None,
                 isOnView=None, artistOrCulture=None, medium=None, hasImages=None,
                 geoLocation=None, dateBegin=None, dateEnd=None):
    """
    Sends a search query to the Met Museum Collection API and returns the response.

    Args:
        q (str): The search query.
        isHighlight (Optional[str]): Whether to include highlighted objects
        in the search results. Defaults to None.
        title (Optional[str]): The title of the object to search for. 
        Defaults to None.
        tags (Optional[str]): The tags associated with the object to search
        for. Defaults to None.
        departmentId (Optional[str]): The department ID of the object to search
        for. Defaults to None.
        isOnView (Optional[str]): Whether the object is currently on view.
        Defaults to None.
        artistOrCulture (Optional[str]): Whether q is for artist or culture.
        Defaults to None.
        medium (Optional[str]): The medium of the object to search for.
        Defaults to None.
        hasImages (Optional[str]): Whether the object has images. 
        Defaults to None.
        geoLocation (Optional[str]): The geographic location of the object 
        to search for. Defaults to None.
        dateBegin (Optional[str]): The beginning date of the object to 
        search for. Defaults to None.
        dateEnd (Optional[str]): The ending date of the object to search for.
        Defaults to None.

    Returns:
        requests.Response: The response object containing the search results.
    """
    params = {
        'q': q,
        'isHighlight': isHighlight,
        'title': title,
        'tags': tags,
        'departmentId': departmentId,
        'isOnView': isOnView,
        'artistOrCulture': artistOrCulture,
        'medium': medium,
        'hasImages': hasImages,
        'geoLocation': geoLocation,
        'dateBegin': dateBegin,
        'dateEnd': dateEnd
    }
    
    # Something that needs to be said about query search using this API: there is
    # a bug that has it's own issue in github that tracks back to the
    # Oct 7, 2020 (https://github.com/metmuseum/openaccess/issues/36).
    # The bug is simple: get request for search endpoint yields varying 
    # results if you use different order of parameters. You can't really do
    # anything about it, maybe use different variations of a search query
    # function depending on which parameters are used. That would be pretty
    # tedious work though, so as for me, I'll just leave my code as it is
    # without considering this bug.

    # Concatenate every parameter into a string in format of 
    # [parameter]=[argument]& but skip parameter if it it's None.

    filtered_params = {k: v for k, v in params.items() if v is not None}    
    query_string = '&'.join(f'{k}={v}' for k, v in filtered_params.items())
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?{query_string}"
    try:
        response = requests.get(url)
        logger.info(f"Отправлен запрос на поиск по запросу {q}")
        response.raise_for_status()
        logger.info(f"Поиск по '{q}' вернул {response.json().get('total')} результатов")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при поиске по запросу '{q}: {e}")
        raise

