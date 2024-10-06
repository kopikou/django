from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from artists.models import Artist,Show,Type,Income,Expenses
from artists.serializers import ArtistCreateSerializer, ArtistSerializer, ExpensesCreateSerializer, IncomeCreateSerializer, ShowCreateSerializer,ShowSerializer,TypeSerializer,IncomeSerializer,ExpensesSerializer

class ArtistsViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ArtistCreateSerializer
        return super().get_serializer_class()

class ShowViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ShowCreateSerializer
        return super().get_serializer_class()

class TypeViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class IncomeViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return IncomeCreateSerializer
        return super().get_serializer_class()

class ExpenseViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer    

    def get_serializer_class(self):
        if self.action == 'create':
            return ExpensesCreateSerializer
        return super().get_serializer_class()