import factory


class DealerFactory(factory.DjangoModelFactory):

    name = factory.Sequence(lambda n: "name-{0}".format(n))

    class Meta:
        model = "dealers.Dealer"
