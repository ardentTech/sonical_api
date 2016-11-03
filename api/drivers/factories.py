import factory

from manufacturing.factories import ManufacturerFactory


class DriverFactory(factory.DjangoModelFactory):

    manufacturer = factory.SubFactory(ManufacturerFactory)
    model = factory.Sequence(lambda n: "model-{0}".format(n))

    class Meta:
        model = "drivers.Driver"
