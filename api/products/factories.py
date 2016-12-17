import factory
from factory import fuzzy


class DealerFactory(factory.DjangoModelFactory):

    name = factory.Sequence(lambda n: "name-{0}".format(n))

    class Meta:
        model = "products.Dealer"


class ProductListing(factory.DjangoModelFactory):

    dealer = DealerFactory()
    path = factory.Sequence(lambda n: "/path/{0}".format(n))
    price = fuzzy.FuzzyDecimal(5.00, 500.00)

    class Meta:
        model = "products.ProductListing"
