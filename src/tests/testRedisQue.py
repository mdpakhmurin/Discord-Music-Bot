if __name__ == '__main__':
    import os
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from zope.interface.verify import verifyObject

from MusicBot.model.Queue.RedisQue import RedisQue
from MusicBot.model.Queue.IQue import IQue

class TestRedisQue(unittest.TestCase):
    def setUp(self):
        self.que = RedisQue('____test___id')
        self.que.clear()

    def test_ique_implemented(self):
        self.assertTrue(verifyObject(IQue, self.que))

    def test_id(self):
        self.assertEqual(self.que.get_id(), '____test___id')

    def test_push(self):
        self.assertEqual(self.que.get_size(), 0)

        self.que.push_back('zero')
        self.assertEqual(self.que.get_size(), 1)

        self.que.push_back(1)
        self.assertEqual(self.que.get_size(), 2)

        self.que.push_back([2, 2])
        self.assertEqual(self.que.get_size(), 3)

        self.que.push_back({3, 3, 3})
        self.assertEqual(self.que.get_size(), 4)

        self.que.push_back(44444444)
        self.assertEqual(self.que.get_size(), 5)

    def test_peek_front(self):
        self.que.push_back('zero')
        self.que.push_back(1)

        self.assertEqual(self.que.peek_front(), 'zero')
        self.assertEqual(self.que.get_size(), 2)

    def test_peek_empty(self):
        self.que.peek_front()

    def test_pop_front(self):
        self.que.push_back('zero')
        self.que.push_back(1)

        self.assertEqual(self.que.pop_front(), 'zero')
        self.assertEqual(self.que.get_size(), 1)

        self.assertEqual(self.que.pop_front(), 1)
        self.assertEqual(self.que.get_size(), 0)

    def test_pop_empty(self):
        self.que.pop_front()

    def test_clear(self):
        self.que.push_back('zero')
        self.que.push_back(1)

        self.que.clear()

        self.assertEqual(self.que.get_size(), 0)

    def test_que_with_same_id_has_same_elems(self):
        self.que.push_back("new element")

        new_que = RedisQue('____test___id')
        self.assertEqual(self.que.peek_front(), new_que.peek_front())

    def test_get_all(self):
        pushElems = [1111, 222, '333']

        for el in pushElems:
            self.que.push_back(el)
        
        getElems = self.que.get_all()

        sameEl = set(pushElems) & set(getElems)
        self.assertEqual(len(sameEl), len(pushElems))

    def tearDown(self):
        self.que.clear()


if __name__ == "__main__":
    unittest.main()
