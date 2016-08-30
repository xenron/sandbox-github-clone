from django.test import TestCase

from .factories import PublicationFactory, AffiliationFactory, AuthorFactory

class Test_SeparateModelFile(TestCase):
    def test_CreateModelByFactory(self):
        pub1 = PublicationFactory()
        pub2 = PublicationFactory()
        pub3 = PublicationFactory()
        
        aff1 = AffiliationFactory()
        aff2 = AffiliationFactory()
        
        a = AuthorFactory.create(
            publications=(pub1, pub2, pub3),
            affiliations=(aff1, aff2)
        )
        
        assert a.name == 'Name #0'
        assert a.publications.all().count() == 3
        assert a.publications.all()[0].title == 'Title #0'
        assert a.affiliations.all().count() == 2
        assert a.affiliations.all()[0].name == 'Affiliation #0'