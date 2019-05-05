from config import SUBSTITUTE

if not SUBSTITUTE:
    from app.google_maps.service import GoogleMapService
else:
    from app.google_maps.substitute import GoogleMapService

__all__ = [
    'GoogleMapService',
]
