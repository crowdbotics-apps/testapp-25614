from django.apps import AppConfig
from django.conf import settings


class GolabConfig(AppConfig):
    name = 'golab'

    def ready(self):
        # import golab.signals
        if not settings.DEBUG:
            try:
                import golab.signals  # noqa F401
            except ImportError:
                pass
