from rest_framework import serializers
from artists.models import Artist, Show,Type,Income,Expenses
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','is_superuser']

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ShowSerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)
    class Meta:
        model = Show
        fields = "__all__"

class ShowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = "__all__"
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class IncomeSerializer(serializers.ModelSerializer):
    show = ShowSerializer(read_only=True)
    class Meta:
        model = Income
        fields = "__all__"

class IncomeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ArtistSerializer(serializers.ModelSerializer):
    show = ShowSerializer(read_only=True)

    class Meta:
        model = Artist
        fields = "__all__"


class ArtistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

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
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)