from config import SUBSTITUTE

if not SUBSTITUTE:
    from collect_placecs.google_maps import GoogleMapService
else:
    from collect_placecs.google_maps import GoogleMapService

__all__ = [
    'GoogleMapService',
]
