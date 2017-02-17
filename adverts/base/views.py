from django.views.generic import ListView, DetailView
from .models import Advert


class AdvertListView(ListView):
    template_name = 'advert_list.html'
    model = Advert

    def get_queryset(self):
        return super().get_queryset().with_visits_count()


class AdvertDetailView(DetailView):
    template_name = 'advert_detail.html'
    model = Advert

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.add_visit(self.request.user_hash)
        return response

    def get_queryset(self):
        return super().get_queryset().with_visits_count()