import factory
from factory.fuzzy import FuzzyDecimal

from manufacturing.factories import ManufacturerFactory


class DriverFactory(factory.DjangoModelFactory):

    dc_resistance = FuzzyDecimal(1.00, 16.00)
    manufacturer = factory.SubFactory(ManufacturerFactory)
    model = factory.Sequence(lambda n: "model-{0}".format(n))
    nominal_diameter = FuzzyDecimal(50.00, 400.00)
    resonant_frequency = FuzzyDecimal(20.00, 20000.00)
    sensitivity = FuzzyDecimal(80.00, 102.50)

    class Meta:
        model = "drivers.Driver"
