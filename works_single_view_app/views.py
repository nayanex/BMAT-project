from django.shortcuts import render
from django.shortcuts import redirect
from works_single_view_app.forms import SongMetadataForm, FindSongForm
from works_single_view_app.models import SongMetadata
from django.views.generic import ListView
from django.http import HttpResponse
from django.core import serializers
from works_single_view_app.resources import WorksSingleViewResource


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = SongMetadata

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


def find_song(request):
    form = FindSongForm(request.POST or None)

    if request.method == "POST":
        print("IS FORM VALUD")
        print(form.is_valid())
        if form.is_valid():
            queryset = SongMetadata.objects.filter(iswc=form.data['iswc']).first(),
            qs_json = serializers.serialize('json', queryset)
            return HttpResponse(qs_json, content_type='application/json')
    else:
        return render(request, "works_single_view_app/find_song.html", {"form":form})


def export2csv(request):
    song_resource = WorksSingleViewResource()
    dataset = song_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="works_single_view.csv"'
    return response


def add_song_metadata(request):
    form = SongMetadataForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            song = form.save(commit=False)
            song.save()
            return redirect("home")
    else:
        return render(request, "works_single_view_app/song_metadata.html", {"form":form})