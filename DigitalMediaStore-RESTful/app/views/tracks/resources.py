from flask.views import MethodView
from flask_smorest import Page

from app.extensions.api import CursorPage  # noqa:F401
from app.extensions.api import Blueprint
from app.models import Track

from .schemas import TrackSchema

blp = Blueprint("Tracks", __name__, url_prefix="/api/tracks", description="API endpoints about artists")


@blp.route("/")
class Tracks(MethodView):
    @blp.etag
    # @blp.arguments(TrackQueryArgsSchema, location="query")
    @blp.response(200, TrackSchema(many=True))
    @blp.paginate(Page)
    @blp.doc(description="Get information for multiple tracks")
    def get(self):
        """List tracks"""
        ret = Track.find_all()
        return ret

    @blp.etag
    @blp.arguments(TrackSchema)
    @blp.response(201, TrackSchema)
    @blp.doc(description="Add information for a single tracks")
    def post(self, new_track):
        """Add a new track"""
        item = Track(**new_track)
        item.create()
        return item


@blp.route("/<int:id>")
class TrackById(MethodView):
    @blp.etag
    @blp.response(200, TrackSchema)
    @blp.doc(description="Get information for a single track")
    def get(self, id):
        """Get track by ID"""
        ret = Track.find_by_id(id)
        return ret

    @blp.etag
    @blp.arguments(TrackSchema)
    @blp.response(200, TrackSchema)
    @blp.doc(description="Update information for a Track")
    def put(self, data, id):
        """Update an existing artist"""
        item = Track.find_by_id(id)
        blp.check_etag(item, TrackSchema)
        TrackSchema().update(item, data)
        item.update()
        return item
