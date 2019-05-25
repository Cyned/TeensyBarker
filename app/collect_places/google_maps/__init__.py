from config import SUBSTITUTE

if not SUBSTITUTE:
    from collect_places.google_maps.service import GoogleMapService
else:
    from collect_places.google_maps.substitute import GoogleMapService

__all__ = [
    'GoogleMapService',
]
