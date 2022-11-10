if __name__ == '__main__':
    import os
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from zope.interface.verify import verifyObject
import asyncio

from MusicBot.model.Scraper.Yandex.YandexUrl2MusicInfo import YandexUrl2MusicInfo 
from MusicBot.model.Scraper.IUrl2MusicInfo import IUrl2MusicInfo
from MusicBot.model.Scraper.MusicInfo import MusicInfo


class TestYandexSingleTrackUrl2MusicInfo(unittest.TestCase):
    def setUp(self):
        self.parser = YandexUrl2MusicInfo()

    def test_IUrl2MusicInfo_implemented(self):
        self.assertTrue(verifyObject(IUrl2MusicInfo, self.parser))

    def test_parse_asc(self):
        rick_albom_url = 'https://music.yandex.ru/album/9046986'
        result = asyncio.run(self.parser.parse_asc(rick_albom_url))
        second_result = result[1]
        self.assertEqual(second_result.title, 'Never Gonna Give You Up')
        self.assertEqual(second_result.authors, ['Rick Astley'])

        rick_artist_url = 'https://music.yandex.ru/artist/34466' 
        result = asyncio.run(self.parser.parse_asc(rick_artist_url))
        self.assertTrue(len(result) > 4)
        self.assertEqual(result[0].title, 'Never Gonna Give You Up')
        self.assertEqual(result[0].authors, ['Rick Astley'])

        playlist_url = 'https://music.yandex.ru/users/MehMessGo/playlists/3'
        result = asyncio.run(self.parser.parse_asc(playlist_url))
        self.assertTrue(len(result) > 4)

        never_gonna_url = 'https://music.yandex.ru/album/9046986/track/609676'
        result = asyncio.run(self.parser.parse_asc(never_gonna_url))[0]
        self.assertEqual(result.title, 'Never Gonna Give You Up')
        self.assertEqual(result.authors, ['Rick Astley'])

        bad_url = 'https://music.yandex.ru/'
        result = asyncio.run(self.parser.parse_asc(bad_url))
        self.assertEqual(len(result), 0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
