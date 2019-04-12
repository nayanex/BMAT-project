from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from works_single_view_app.forms import SongMetadataForm
from works_single_view_app.models import SongMetadata
from django.views.generic import ListView


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = SongMetadata

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context


def find_song(request):
    return render(request, "works_single_view_app/find_song.html")


def contact(request):
    return render(request, "works_single_view_app/contact.html")


def hello_there(request, name):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )


def song_metadata(request):
    form = SongMetadataForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            song = form.save(commit=False)
            song.save()
            return redirect("home")
    else:
        return render(request, "works_single_view_app/song_metadata.html", {"form": form})
