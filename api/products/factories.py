import factory
from factory import fuzzy

from dealers.factories import DealerFactory


class ProductListing(factory.DjangoModelFactory):

    dealer = DealerFactory()
    path = factory.Sequence(lambda n: "/path/{0}".format(n))
    price = fuzzy.FuzzyDecimal(5.00, 500.00)

    class Meta:
        model = "products.ProductListing"
