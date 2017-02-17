from django.conf.urls import url
from .views import AdvertListView, AdvertDetailView

urlpatterns = [
    url(r'^$', AdvertListView.as_view(), name='advert-list'),
    url(r'^(?P<pk>\d+)/$', AdvertDetailView.as_view(), name='advert-detail')
]
