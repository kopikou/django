from rest_framework import serializers
from artists.models import Artist, Show,Type,Income,Expenses

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"

class ShowSerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)
    class Meta:
        model = Show
        fields = "__all__"

class ShowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = "__all__"

class IncomeSerializer(serializers.ModelSerializer):
    show = ShowSerializer(read_only=True)
    class Meta:
        model = Income
        fields = "__all__"

class IncomeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"

class ArtistSerializer(serializers.ModelSerializer):
    show = ShowSerializer(read_only=True)
    class Meta:
        model = Artist
        fields = "__all__"


class ArtistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class ExpensesSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    income = IncomeSerializer(read_only=True)
    class Meta:
        model = Expenses
        fields = "__all__"

class ExpensesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = "__all__"