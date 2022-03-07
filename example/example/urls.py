from django.conf.urls import url
from invoices.views import invoice_view


urlpatterns = [
    url(r'^$', invoice_view),
]
