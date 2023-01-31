from src import crawl_hh


def test_1():
    url = "https://hh.ru/search/vacancy?text=python&salary=&clusters=true&area=1001&area=2&ored_clusters=true&enable_snippets=true"
    result = crawl_hh.get_data(url)
    assert result > 0
