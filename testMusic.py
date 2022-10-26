import unittest

from zope.interface.verify import verifyObject

from model.IMusic import IMusic
from model.Music import Music


class TestMusic(unittest.TestCase):
    def setUp(self):
        self.author = "Rick Astley"
        self.title = "Rick Astley - Never Gonna Give You Up (Official Music Video)"
        self.link = "https://32323fsq/wqqw"

        self.music = Music(self.author, self.title, self.link)

    def test_IMusic_implemented(self):
        self.assertTrue(verifyObject(IMusic, self.music))

    def test_get_author(self):
        self.assertEqual(self.music.get_author(), self.author)

    def test_get_title(self):
        self.assertEqual(self.music.get_title(), self.title)

    def test_get_link(self):
        self.assertEqual(self.music.get_link(), self.link)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
