from django.urls import path, include
from tizer.views import TizerListApiView
urlpatterns = [
    path("", TizerListApiView.as_view())
]
