import unittest

from zope.interface.verify import verifyObject

from RedisChatMusicQue import RedisChatMusicQue
from IChat import IChat
from IQue import IQue


class TestChatMusicQue(unittest.TestCase):
    def setUp(self):
        self.que = RedisChatMusicQue('____test___id')
        self.que.clear()

    def test_ique_implemented(self):
        self.assertTrue(verifyObject(IQue, self.que))

    def test_ichat_implemented(self):
        self.assertTrue(verifyObject(IChat, self.que))

    def test_chat_id(self):
        self.assertEqual(self.que.chat_id(), '____test___id')

    def test_push(self):
        self.assertEqual(self.que.size(), 0)

        self.que.push_back('zero')
        self.assertEqual(self.que.size(), 1)

        self.que.push_back(1)
        self.assertEqual(self.que.size(), 2)

        self.que.push_back([2, 2])
        self.assertEqual(self.que.size(), 3)

        self.que.push_back({3, 3, 3})
        self.assertEqual(self.que.size(), 4)

        self.que.push_back(44444444)
        self.assertEqual(self.que.size(), 5)

    def test_peek_first(self):
        self.que.push_back('zero')
        self.que.push_back(1)

        self.assertEqual(self.que.peek_front(), 'zero')

    def test_peek_front(self):
        self.que.push_back('zero')
        self.que.push_back(1)

        self.assertEqual(self.que.peek_front(), 'zero')
        self.assertEqual(self.que.size(), 2)

    def test_pop_front(self):
        self.que.push_back('zero')
        self.que.push_back(1)

        self.assertEqual(self.que.pop_front(), 'zero')
        self.assertEqual(self.que.size(), 1)

        self.assertEqual(self.que.pop_front(), 1)
        self.assertEqual(self.que.size(), 0)

    def test_clear(self):
        self.que.push_back('zero')
        self.que.push_back(1)

        self.que.clear()

        self.assertEqual(self.que.size(), 0)

    def test_que_with_same_id_has_same_elems(self):
        self.que.push_back("new element")

        new_que = RedisChatMusicQue('____test___id')
        self.assertEqual(self.que.peek_front(), new_que.peek_front())

    def tearDown(self):
        self.que.clear()


if __name__ == "__main__":
    unittest.main()
