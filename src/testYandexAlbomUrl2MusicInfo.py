import unittest
from zope.interface.verify import verifyObject
import asyncio

from MusicBot.model.Scraper.Yandex.AlbomUrl2MusicInfo import AlbomUrl2MusicInfo
from MusicBot.model.Scraper.IUrl2MusicInfo import IUrl2MusicInfo
from MusicBot.model.Scraper.MusicInfo import MusicInfo


class TestYandexArtistUrl2MusicInfo(unittest.TestCase):
    def setUp(self):
        self.parser = AlbomUrl2MusicInfo()

    def test_IUrl2MusicInfo_implemented(self):
        self.assertTrue(verifyObject(IUrl2MusicInfo, self.parser))

    def test_parse_asc(self):
        never_gonna_url = 'https://music.yandex.ru/album/9046986'
        result = asyncio.run(self.parser.parse_asc(never_gonna_url))
        self.assertTrue(len(result) > 4)
        self.assertEqual(result[1].title, 'Never Gonna Give You Up')
        self.assertEqual(result[1].authors, ['Rick Astley'])

        multiple_authors_url = 'https://music.yandex.ru/album/23873783'
        result = asyncio.run(self.parser.parse_asc(multiple_authors_url))[0]
        self.assertEqual(len(result.authors), 2)

        bad_url = 'https://music.yand34ex.ru/al32bum/23873783'
        result = asyncio.run(self.parser.parse_asc(bad_url))
        self.assertEqual(len(result), 0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
