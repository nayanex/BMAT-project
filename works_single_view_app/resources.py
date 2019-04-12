from import_export import resources
from works_single_view_app.models import SongMetadata


class WorksSingleViewResource(resources.ModelResource):
    class Meta:
        model = SongMetadata
