from django.conf.urls import url

from example.views import sample_view


urlpatterns = [
    url(r'^$', sample_view),
]
