import factory


class ManufacturerFactory(factory.DjangoModelFactory):

    name = factory.Sequence(lambda n: "name-{0}".format(n))

    class Meta:
        model = "manufacturing.Manufacturer"


class MaterialFactory(factory.DjangoModelFactory):

    name = factory.Sequence(lambda n: "name-{0}".format(n))

    class Meta:
        model = "manufacturing.Material"
