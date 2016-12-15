import factory

from manufacturing.factories import ManufacturerFactory


class DriverFactory(factory.DjangoModelFactory):

    manufacturer = factory.SubFactory(ManufacturerFactory)
    model = factory.Sequence(lambda n: "model-{0}".format(n))

    class Meta:
        model = "drivers.Driver"


class DriverGroupFactory(factory.DjangoModelFactory):

    name = factory.Sequence(lambda n: "name-{0}".format(n))

    class Meta:
        model = "drivers.DriverGroup"

    @factory.post_generation
    def drivers(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for driver in extracted:
                self.drivers.add(driver)
