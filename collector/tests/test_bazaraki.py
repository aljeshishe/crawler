from src import crawl_bazaraki


def test_1():
    url = "https://www.bazaraki.com/real-estate-to-rent/houses/lemesos-district-limassol/"
    result = crawl_bazaraki.get_data(url)
    print(result)
    assert result > 0
