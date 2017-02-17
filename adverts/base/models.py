from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache


class AdvertQuerySet(models.QuerySet):
    def with_visits_count(self):
        return self.annotate(_visits_count=models.Count('visits'))


class Advert(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    text = models.TextField(verbose_name='Текст')

    objects = AdvertQuerySet.as_manager()

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'advert-detail', (self.id,)

    def add_visit(self, user_hash):
        assert isinstance(user_hash, str)
        try:
            self.visits.filter(user_hash=user_hash).get()
        except ObjectDoesNotExist:
            pass
        else:
            return None
        advert_cached_visits = cache.get(self._cache_key, [])
        if user_hash not in advert_cached_visits:
            advert_cached_visits.append(user_hash)
            cache.set(self._cache_key, advert_cached_visits, timeout=None)

    @property
    def visits_count(self):
        if not hasattr(self, '_visits_count'):
            raise Exception('Use it only with Advert.objects.with_visits_count()')
        return self._visits_count + len(cache.get(self._cache_key, []))

    @property
    def _cache_key(self):
        return 'advert.%s' % self.id


class AdvertVisitManager(models.Manager):
    def create_from_cache(self):
        cache_keys = cache.keys('advert.*')
        cached_visits = cache.get_many(cache_keys)
        for_bulk = []
        for key, user_hash_list in cached_visits.items():
            for user_hash in user_hash_list:
                for_bulk.append(AdvertVisit(
                    advert_id=int(key.split('.')[1]),
                    user_hash=user_hash
                ))
        self.bulk_create(for_bulk)
        cache.delete_many(cache_keys)


class AdvertVisit(models.Model):
    advert = models.ForeignKey(Advert, related_name='visits')
    user_hash = models.CharField(max_length=100)

    objects = AdvertVisitManager()

    class Meta:
        unique_together = ('advert', 'user_hash')
