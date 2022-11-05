import unittest
from zope.interface.verify import verifyObject
import asyncio

from MusicBot.model.Scraper.Yandex.SingleTrackUrl2MusicInfo import SingleTrackUrl2MusicInfo
from MusicBot.model.Scraper.IUrl2MusicInfo import IUrl2MusicInfo
from MusicBot.model.Scraper.MusicInfo import MusicInfo


class TestYandexSingleTrackUrl2MusicInfo(unittest.TestCase):
    def setUp(self):
        self.parser = SingleTrackUrl2MusicInfo()

    def test_IUrl2MusicInfo_implemented(self):
        self.assertTrue(verifyObject(IUrl2MusicInfo, self.parser))

    def test_parse_asc(self):
        never_gonna_url = 'https://music.yandex.ru/album/9046986/track/609676'
        result = asyncio.run(self.parser.parse_asc(never_gonna_url))[0]
        self.assertEqual(result.title, 'Never Gonna Give You Up')
        self.assertEqual(result.authors, ['Rick Astley'])

        drink_blood_url = 'https://music.yandex.ru/album/2354505/track/20650200'
        result = asyncio.run(self.parser.parse_asc(drink_blood_url))[0]
        self.assertEqual(result.title, 'We Drink Your Blood')
        self.assertEqual(result.authors, ['Powerwolf'])

        multiple_authors_url = 'https://music.yandex.ru/album/23873783/track/108301604'
        result = asyncio.run(self.parser.parse_asc(multiple_authors_url))[0]
        self.assertEqual(len(result.authors), 2)

        bad_url = 'https://music.yandex.ru/'
        result = asyncio.run(self.parser.parse_asc(bad_url))
        self.assertEqual(len(result), 0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
