from django.urls import path
from works_single_view_app import views
from works_single_view_app.models import SongMetadata


home_list_view = views.HomeListView.as_view(
    queryset=SongMetadata.objects.order_by("iswc")[:20],
    context_object_name="song_list",
    template_name="works_single_view_app/home.html",
)


urlpatterns = [
    path("", home_list_view, name="home"),
    path("find_song/", views.find_song, name="find_song"),
    path("export2csv/", views.export2csv, name="export2csv"),
    path("add_song_metadata/", views.add_song_metadata, name="add_song_metadata"),
]
