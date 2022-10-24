import unittest

from zope.interface.verify import verifyObject

from IMusicBase import IMusicBase
from YTMusicBase import YTMusicBase
from IMusic import IMusic


class TestChatMusicQue(unittest.TestCase):
    def setUp(self):
        self.music_base = YTMusicBase()

    def test_IMusicBase_implemented(self):
        self.assertTrue(verifyObject(IMusicBase, self.music_base))

    def searchable(self):
        music_name = "riCk Asly - nEVr Goa GiVe YOU __Up"
        self.assertTrue(music_name)

        music_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertTrue(music_link)

    def search(self):
        music_name = "riCk Asly - nEVr Goa GiVe YOU __Up"
        search_result = self.music_base.parse(music_name)
        self.assertEqual(len(search_result), 1)
        self.assertTrue(verifyObject(search_result[0], self.IMusic))

        music_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        search_result = self.music_base.parse(music_name)
        self.assertEqual(len(search_result), 1)
        self.assertTrue(verifyObject(search_result[0], self.IMusic))

        music_name = "https://music.yandex.ru/album/17975287/track/90737980"
        search_result = self.music_base.parse(music_name)
        self.assertEqual(len(search_result), 0)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
