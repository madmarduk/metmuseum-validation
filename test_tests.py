from main import (get_artwork_object, get_random_object_id,
                  validate_artwork, validate_artworks_list,
                  query_search, logger
                  )

import requests


def test_api_status():
    """Test whether API gives correct response for existent and nonexistent ID."""
    try:   
        assert get_artwork_object(get_random_object_id()).status_code == 200
        assert get_artwork_object(9999999).status_code == 404
    except AssertionError as e:
        logger.error(f"{e}")
        raise


def test_artwork_validation():
    """Test whether artwork object could be validated."""
    # I think this is one hell of a line but for now it will be like that
    try:
        assert validate_artwork(get_artwork_object(obj_id=get_random_object_id())) is not None
    except AssertionError as e:
        logger.error(f"{e}")
        raise


def test_search_keyword():
    artworks_list=query_search(q="sunflowers")
    try:
        assert validate_artworks_list(artworks_list) is not None
        assert artworks_list.status_code == 200
    except AssertionError as e:
        logger.error(f"{e}")
        raise


def test_search_highlight():
    artworks_list=query_search(q="sunflowers", isHighlight="true")
    try:
        assert validate_artworks_list(artworks_list) is not None
        assert artworks_list.status_code == 200
    except AssertionError as e:
        logger.error(f"{e}")
        raise


def test_search_department():
    artworks_list=query_search(q="cat", departmentId="6")
    try:
        assert validate_artworks_list(artworks_list) is not None
        assert artworks_list.status_code == 200
    except AssertionError as e:
        logger.error(f"{e}")
        raise


def test_search_on_view():
    artworks_list=query_search(q="sunflower", isOnView="true")
    try:
        assert validate_artworks_list(artworks_list) is not None
        assert artworks_list.status_code == 200
    except AssertionError as e:
        logger.error(f"{e}")
        raise


def test_search_artist_or_culture():
    # artworks_list=query_search(q="french", artistOrCulture="true") <== this won't work 
    # because API requires orbitrary order of parameters that you have to somehow guess
    artworks_list = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q=french")
    logger.info(f"Отправлен запрос на поиск по запросу french, artistOrCulture=true")
    logger.info(f"Поиск по 'french' вернул {artworks_list.json().get('total')} результатов")
    try:
        assert validate_artworks_list(artworks_list) is not None
        assert artworks_list.status_code == 200
    except AssertionError as e:
        logger.error(f"{e}")
        raise


def test_search_medium():
    artworks_list=query_search(q="quilt", medium="Quilts|Silk|Bedcovers")
    try:
        assert validate_artworks_list(artworks_list) is not None
        assert artworks_list.status_code == 200
    except AssertionError as e:
        logger.error(f"{e}")
        raise


def test_search_has_images():
    artworks_list=query_search(q="Auguste Renoir", hasImages="true")
    try:
        assert validate_artworks_list(artworks_list) is not None
        assert artworks_list.status_code == 200
    except AssertionError as e:
        logger.error(f"{e}")
        raise


def test_search_geo_location():
    artworks_list=query_search(q="flowers", geoLocation="France")
    try:
        assert validate_artworks_list(artworks_list) is not None
        assert artworks_list.status_code == 200
    except AssertionError as e:
        logger.error(f"{e}")
        raise


def test_search_date_range():
    artworks_list=query_search(q="African", dateBegin="1700", dateEnd="1800")
    try:
        assert validate_artworks_list(artworks_list) is not None
        assert artworks_list.status_code == 200
    except AssertionError as e:
        logger.error(f"{e}")
        raise