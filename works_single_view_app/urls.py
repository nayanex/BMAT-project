from django.urls import path
from works_single_view_app import views
from works_single_view_app.models import SongMetadata


home_list_view = views.HomeListView.as_view(
    queryset=SongMetadata.objects.order_by("iswc")[:20],  # :5 limits the results to the five most recent
    context_object_name="song_list",
    template_name="works_single_view_app/home.html",
)

home_list_view = views.HomeListView.as_view(
    queryset=SongMetadata.objects.filter(iswc=iswc_query)[:20],  # :5 limits the results to the five most recent
    context_object_name="requested_song",
    template_name="works_single_view_app/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("hello/<name>", views.hello_there, name="hello_there"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("song/", views.song_metadata, name="log"),
]

