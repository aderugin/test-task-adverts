from uuid import uuid4
from model_mommy import mommy
from django.test import TestCase
from django.core.cache import cache

from adverts.base.models import Advert, AdvertVisit


class AdvertTestCase(TestCase):
    def setUp(self):
        cache.delete_many(cache.keys('advert.*'))
        self.user_hash_list = [str(uuid4()) for _ in range(10)]
        for advert in mommy.make('base.Advert', _quantity=10)[:5]:
            for user_hash in self.user_hash_list[:5]:
                mommy.make(
                    'base.AdvertVisit',
                    user_hash=user_hash,
                    advert=advert
                )
        self.advert_list = Advert.objects.with_visits_count().order_by('-_visits_count')

    def test_add_visit(self):
        self._add_visits()
        self.assertEqual(self.advert_list[0].visits_count, 7)
        self.assertEqual(self.advert_list[9].visits_count, 1)

    def test_create_visits_from_cache(self):
        adverts_queryset = Advert.objects.with_visits_count()
        advert_1_id = self.advert_list[0].id
        advert_2_id = self.advert_list[9].id

        self._add_visits()

        self.assertEqual(
            set(cache.get('advert.%s' % advert_1_id)),
            {self.user_hash_list[6], self.user_hash_list[7]}
        )
        self.assertEqual(
            set(cache.get('advert.%s' % advert_2_id)),
            {self.user_hash_list[9]}
        )
        self.assertEqual(adverts_queryset.get(id=advert_1_id)._visits_count, 5)
        self.assertEqual(adverts_queryset.get(id=advert_2_id)._visits_count, 0)
        self.assertEqual(adverts_queryset.get(id=advert_1_id).visits_count, 7)
        self.assertEqual(adverts_queryset.get(id=advert_2_id).visits_count, 1)

        AdvertVisit.objects.create_from_cache()

        self.assertFalse(cache.keys('advert.*'))
        self.assertEqual(adverts_queryset.get(id=advert_1_id)._visits_count, 7)
        self.assertEqual(adverts_queryset.get(id=advert_2_id)._visits_count, 1)

    def _add_visits(self):
        self.advert_list[0].add_visit(self.user_hash_list[6])
        self.advert_list[0].add_visit(self.user_hash_list[7])
        self.advert_list[0].add_visit(self.user_hash_list[0])
        self.advert_list[9].add_visit(self.user_hash_list[9])
