from django.conf import settings
from django.contrib.auth import get_user_model

import factory


class UserFactory(factory.django.DjangoModelFactory):

    email = factory.Sequence(lambda n: "admin-{0}@test.com".format(n))
    password = factory.PostGenerationMethodCall(
        "set_password", settings.SONICAL_DEFAULT_PASSWORD)

    class Meta:
        model = get_user_model()
