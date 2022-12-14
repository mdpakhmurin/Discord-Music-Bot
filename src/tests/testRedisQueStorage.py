if __name__ == '__main__':
    import os
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from zope.interface.verify import verifyObject

from MusicBot.model.Queue.IQue import IQue
from MusicBot.model.Queue.IQueStorage import IQueStorage
from MusicBot.model.Queue.RedisQueStorage import RedisQueStorage

class TestRedisQueStorage(unittest.TestCase):
    def setUp(self):
        self.storage = RedisQueStorage()

    def test_IQueStorage_implemented(self):
        self.assertTrue(verifyObject(IQueStorage, self.storage))

    def test_get_que(self):
        que = self.storage.get_que('__test__0')
        que.clear()
        self.assertTrue(verifyObject(IQue, que))
        que.push_back('some value')

        que = self.storage.get_que('__test__1')
        self.assertTrue(verifyObject(IQue, que))
        que.clear()
        self.assertFalse(que.peek_front(), 'some value')

        que = self.storage.get_que('__test__0')
        self.assertTrue(verifyObject(IQue, que))
        self.assertTrue(que.peek_front(), 'some value')

        que.clear()
        

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
