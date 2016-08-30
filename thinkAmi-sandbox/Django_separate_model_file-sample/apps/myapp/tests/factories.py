import factory
from ..models import Publication, Author
from apps.outsideapp.models import Affiliation

class PublicationFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Title #{}'.format(n))
    class Meta:
        model = Publication
        
class AffiliationFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Affiliation #{}'.format(n))
    class Meta:
        model = Affiliation
        
class AuthorFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Name #{}'.format(n))
    class Meta:
        model = Author
        
    @factory.post_generation
    def publications(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for publication in extracted:
                self.publications.add(publication)
                
    @factory.post_generation
    def affiliations(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for affiliation in extracted:
                self.affiliations.add(affiliation)