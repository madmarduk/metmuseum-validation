from main import (get_artwork_object, 
                  get_random_object_id,
                  validate_artwork,
                  validate_artworks_list,
                  query_search,
                  )
# Написать тесты с Pytest, которые вызывают API и проверяют:
# Доп проверки:
    # TODO: Работа фильтрации и сортировки результатов поиска (если предусмотрено API)


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
    # I think this is one hell of a line but for now it will be like that
    assert validate_artwork(get_artwork_object(obj_id=get_random_object_id())) is not None


def test_search_keyword():
    assert validate_artworks_list(artworks_list=query_search("sunflowers")) is not None
    assert query_search("sunflowers").status_code == 200