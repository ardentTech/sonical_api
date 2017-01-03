from django.conf import settings


class ModeMixin(object):
    """
    Convenient and human-friendly access to the app-wide Django DEBUG setting
    """

    DEV_MODE = "dev"
    PRO_MODE = "pro"

    def __init__(self):
        self.mode = self.DEV_MODE if settings.DEBUG else self.PRO_MODE

    def dev_mode(self):
        return self.mode == self.DEV_MODE

    def get_mode(self):
        return self.mode

    def pro_mode(self):
        return self.mode == self.PRO_MODE
