from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from artists.models import Artist,Show,Type,Income,Expenses
from artists.serializers import ArtistSerializer,ShowSerializer,TypeSerializer,IncomeSerializer,ExpensesSerializer

class ArtistsViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class ShowViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

class TypeViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class IncomeViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

class ExpenseViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer    