if __name__ == '__main__':
    import os
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from zope.interface.verify import verifyObject
import asyncio

from MusicBot.model.Scraper.Yandex.ArtistUrl2MusicInfo import ArtistUrl2MusicInfo
from MusicBot.model.Scraper.IUrl2MusicInfo import IUrl2MusicInfo
from MusicBot.model.Scraper.MusicInfo import MusicInfo


class TestYandexArtistUrl2MusicInfo(unittest.TestCase):
    def setUp(self):
        self.parser = ArtistUrl2MusicInfo() 

    def test_IUrl2MusicInfo_implemented(self):
        self.assertTrue(verifyObject(IUrl2MusicInfo, self.parser))

    def test_parse_asc(self):
        rick_url = 'https://music.yandex.ru/artist/34466' 
        result = asyncio.run(self.parser.parse_asc(rick_url))
        self.assertTrue(len(result) > 4)
        self.assertEqual(result[0].title, 'Never Gonna Give You Up')
        self.assertEqual(result[0].authors, ['Rick Astley'])

        bad_url = 'https://music.yandex.ru/artist/'
        result = asyncio.run(self.parser.parse_asc(bad_url))
        self.assertEqual(len(result), 0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
