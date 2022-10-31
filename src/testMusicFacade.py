import unittest

from zope.interface.verify import verifyObject

from MusicBot.model.MusicSearcher.IMusicSearcher import IMusicSearcher
from MusicBot.model.MusicSearcher.YTMusicSearcher import YTMusicSearcher
from MusicBot.model.IMusic import IMusic

from MusicBot.model.MusicFacade import MusicFacade, DEFAULT_MUSIC_SEARCHER, DEFAULT_QUE_STORAGE


class TestMusicFacade(unittest.TestCase):
    def setUp(self):
        self.music_facade = MusicFacade()

    def test_set_que_storage(self):
        bad_que_storage = None
        good_que_storage = DEFAULT_QUE_STORAGE

        # breaks when bad storage setted
        self.music_facade.set_que_storage(bad_que_storage)
        try:
            self.music_facade.clear_que('__test_id_0')
            self.fail()
        except:
            pass

        # doesnt break when good storage set
        self.music_facade.set_que_storage(good_que_storage)
        try:
            self.music_facade.clear_que('__test_id_0')
        except:
            self.fail()

    def test_set_music_searcher(self):
        bad_music_searcher = None
        good_music_searcher = DEFAULT_MUSIC_SEARCHER

        # breaks when bad searcher set
        self.music_facade.set_music_searcher(bad_music_searcher)
        try:
            self.music_facade.search_music('never gonna')
            self.fail()
        except:
            pass

        # doesnt break when good searcher set
        self.music_facade.set_music_searcher(good_music_searcher)
        try:
            self.music_facade.search_music('never gonna')
        except:
            self.fail()

    def test_get_pop_from_que(self):
        target_server = '__test_id'

        self.music_facade.add_to_que(target_server, 'never gonna')
        start_que_size = self.music_facade.get_que_size(target_server)

        self.music_facade.pop_que_first(target_server)
        current_que_size = self.music_facade.get_que_size(target_server)

        self.assertEqual(start_que_size - 1, current_que_size)

        self.music_facade.clear_que('__test_id')

    def test_get_peek_from_que(self):
        target_server = '__test_id'

        self.music_facade.add_to_que(target_server, 'never gonna')
        start_que_size = self.music_facade.get_que_size(target_server)

        self.music_facade.peek_que_first(target_server)
        current_que_size = self.music_facade.get_que_size(target_server)

        self.assertEqual(start_que_size, current_que_size)

        self.music_facade.clear_que(target_server)

    def test_add_and_search_are_equal(self):
        search_text = 'never gonna'
        target_server = '__test_id'

        add_result = self.music_facade.add_to_que(
            target_server, search_text)[0]
        search_result = self.music_facade.search_music(search_text)[0]

        self.assertEqual(add_result.get_author(), search_result.get_author())
        self.assertEqual(add_result.get_title(), search_result.get_title())

        self.music_facade.clear_que(target_server)

    def test_list_que(self):
        search_text_0 = 'never gonna'
        search_text_1 = 'My Arms Keep Missing You '
        target_server = '__test_id'

        # add one collection twice
        add_result = self.music_facade.add_to_que(target_server, search_text_0)
        add_result += self.music_facade.add_to_que(target_server, search_text_1)

        get_all_result = self.music_facade.list_que(target_server)

        # search and get all are equal
        for i in range(len(get_all_result)):
            is_same_author = get_all_result[i].get_author() == add_result[i].get_author()
            is_same_title = get_all_result[i].get_title() == add_result[i].get_title()

            if not is_same_author or not is_same_title:
                self.fail("list_que_all returns incorrect list")
                break

        self.music_facade.clear_que(target_server)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
