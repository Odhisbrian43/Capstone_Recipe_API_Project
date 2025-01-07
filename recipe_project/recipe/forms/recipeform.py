from django import forms
from recipe.models import Recipe

#Form for creating a recipe.
class RecipeForm(forms.ModelForm):

    #Meta class.
    class Meta():
        #Model to be used.
        model = Recipe

        #Fields to be included in the form.
        fields = '__all__'