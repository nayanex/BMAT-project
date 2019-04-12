from django import forms
from works_single_view_app.models import SongMetadata


class SongMetadataForm(forms.ModelForm):
    class Meta:
        model = SongMetadata
        fields = ("title", "contributors", "iswc", "sources", "source_ids",)


class FindSongForm(forms.ModelForm):
    class Meta:
        model = SongMetadata
        fields = ("iswc",)