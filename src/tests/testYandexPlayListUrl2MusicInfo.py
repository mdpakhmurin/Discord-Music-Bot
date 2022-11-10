if __name__ == '__main__':
    import os
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from zope.interface.verify import verifyObject
import asyncio

from MusicBot.model.Scraper.Yandex.PlayListUrl2MusicInfo import PlayListUrl2MusicInfo
from MusicBot.model.Scraper.IUrl2MusicInfo import IUrl2MusicInfo
from MusicBot.model.Scraper.MusicInfo import MusicInfo


class TestYandexSingleTrackUrl2MusicInfo(unittest.TestCase):
    def setUp(self):
        self.parser = PlayListUrl2MusicInfo()

    def test_IUrl2MusicInfo_implemented(self):
        self.assertTrue(verifyObject(IUrl2MusicInfo, self.parser))

    def test_parse_asc(self):
        url = 'https://music.yandex.ru/users/MehMessGo/playlists/3'
        result = asyncio.run(self.parser.parse_asc(url))
        self.assertTrue(len(result) > 4)

        bad_url = 'https://music.yandex.ru/'
        result = asyncio.run(self.parser.parse_asc(bad_url))
        self.assertEqual(len(result), 0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
