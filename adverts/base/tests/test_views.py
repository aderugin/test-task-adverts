from model_mommy import mommy

from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory, Client, override_settings

from adverts.base.views import AdvertListView
from adverts.base.models import Advert


class AdvertListViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        mommy.make('base.Advert', _quantity=2)

    def test_get(self):
        request = self.factory.get(reverse('advert-list'))
        response = AdvertListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['advert_list'].count(), 2)


class AdvertDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.advert = mommy.make('base.Advert')

    @override_settings(DEBUG=True)
    def test_get(self):
        response = self.client.get(reverse('advert-detail', args=(self.advert.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Advert.objects.with_visits_count().get(id=self.advert.id).visits_count, 1
        )
