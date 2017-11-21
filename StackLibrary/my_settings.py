from library.models import LibrarySettings
try:
    SETTINGS = LibrarySettings.objects.get_settings()
except Exception:
    SETTINGS = None