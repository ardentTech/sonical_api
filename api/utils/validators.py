from os.path import isfile

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_file_path(value):
    if not isfile(value):
        raise ValidationError(_("{0} does not exist".format(value)))
