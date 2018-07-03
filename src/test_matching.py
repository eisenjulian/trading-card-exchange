from unittest import TestCase
from fakeredis import FakeStrictRedis
import redis
from mock import patch

import matching
import database as db


class TestMatching(TestCase):
    def test_nocycle(self):
        db.db.flushall()
        db.add_wanted('jose', [1, 2, 3])
        db.add_wanted('pablo', [1, 2, 3])
        db.add_collection('jose', [4, 5])
        db.add_collection('pablo', [4, 5])
        assert list(matching.compute_match()) == []

    def test_all_happy(self):
        db.db.flushall()
        db.add_wanted('jose', [1, 2])
        db.add_wanted('pablo', [3, 4])
        db.add_collection('jose', [3, 4])
        db.add_collection('pablo', [1, 2])
        assert len(list(matching.compute_match())) == 4
