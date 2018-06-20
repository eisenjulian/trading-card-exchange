from unittest import TestCase
from fakeredis import FakeStrictRedis

from matching import Matching


class TestMatching(TestCase):
    def test_nocycle(self):
        redis = FakeStrictRedis()
        redis.flushall()
        matching = Matching(redis)
        matching.add_wanted('jose', [1, 2, 3])
        matching.add_wanted('pablo', [1, 2, 3])
        matching.add_collection('jose', [4, 5])
        matching.add_collection('pablo', [4, 5])
        assert list(matching.compute_match()) == []

    def test_all_happy(self):
        redis = FakeStrictRedis()
        redis.flushall()
        matching = Matching(redis)
        matching.add_wanted('jose', [1, 2])
        matching.add_wanted('pablo', [3, 4])
        matching.add_collection('jose', [3, 4])
        matching.add_collection('pablo', [1, 2])
        assert len(list(matching.compute_match())) == 4
