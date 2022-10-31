import unittest

from zope.interface.verify import verifyObject

from model.MusicSearcher.IMusicSearcher import IMusicSearcher
from model.MusicSearcher.YTMusicSearcher import YTMusicSearcher
from model.IMusic import IMusic


class TestYTMusicSearcher(unittest.TestCase):
    def setUp(self):
        self.searcher = YTMusicSearcher()

    def test_IMusicBase_implemented(self):
        self.assertTrue(verifyObject(IMusicSearcher, self.searcher))

    def test_searchable(self):
        music_name = "riCk Asly - nEVr Goa GiVe YOU __Up"
        self.assertTrue(music_name)

        music_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertTrue(music_link)

    def test_search(self):
        music_name = "riCk Asly - nEVr Goa GiVe YOU __Up"
        search_result = self.searcher.search(music_name)
        self.assertEqual(len(search_result), 1)
        self.assertTrue(verifyObject(IMusic, search_result[0]))

        music_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        search_result = self.searcher.search(music_name)
        self.assertEqual(len(search_result), 1)
        self.assertTrue(verifyObject(IMusic, search_result[0]))

        music_name = "https://music.yandex.ru/album/17975287/track/90737980"
        search_result = self.searcher.search(music_name)
        self.assertEqual(len(search_result), 0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()