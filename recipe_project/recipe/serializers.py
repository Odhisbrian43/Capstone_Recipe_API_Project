from rest_framework.serializers import Serializer
from .models import Recipe

class RecipeSerializer(Serializer):
    class Meta:
        model = Recipe

        Fields = '__all__'