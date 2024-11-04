from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets

from artists.models import Artist,Show,Type,Income,Expenses
from artists.serializers import ArtistCreateSerializer, ArtistSerializer, ExpensesCreateSerializer, IncomeCreateSerializer, ShowCreateSerializer,ShowSerializer,TypeSerializer,IncomeSerializer,ExpensesSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
class UsersViewset(mixins.RetrieveModelMixin, 
    mixins.ListModelMixin, 
    GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileViewSet(GenericViewSet):
    @action(detail=False, methods=['get'], url_path='info')
    def get_info(self, request, *args, **kwargs):
        return Response({
            "is_superuser": self.request.user.is_superuser,
            "is_authenticated": self.request.user.is_authenticated,
            "id": self.request.user.id
        })

class ArtistsViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return ArtistCreateSerializer
        return super().get_serializer_class()
    def get_queryset(self):
        qs = super().get_queryset()

        show = self.request.query_params.get('show')
        user = self.request.query_params.get('user')
        if show:
            qs = qs.filter(show=show)
        if user:
            qs = qs.filter(user=user)
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        return qs

class ShowViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return ShowCreateSerializer
        return super().get_serializer_class()
    def get_queryset(self):
        qs = super().get_queryset()

        if(not self.request.user.is_superuser):
            qs = qs.filter(user=self.request.user)
        return qs

class TypeViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    def get_queryset(self):
        qs = super().get_queryset()

        if(not self.request.user.is_superuser):
            qs = qs.filter(user=self.request.user)
        return qs

class IncomeViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return IncomeCreateSerializer
        return super().get_serializer_class()
    def get_queryset(self):
        qs = super().get_queryset()

        if(not self.request.user.is_superuser):
            qs = qs.filter(user=self.request.user)
        return qs

class ExpenseViewset(mixins.CreateModelMixin,
    mixins.UpdateModelMixin, 
    mixins.RetrieveModelMixin,                
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer    

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return ExpensesCreateSerializer
        return super().get_serializer_class()
    def get_queryset(self):
        qs = super().get_queryset()

        if(not self.request.user.is_superuser):
            qs = qs.filter(user=self.request.user)
        return qs