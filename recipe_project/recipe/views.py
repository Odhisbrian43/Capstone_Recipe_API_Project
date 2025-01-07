from accounts.models import CustomUser
from .models import Recipe
from .serializers import RecipeSerializer
from .permissions import IsOwnerOrReadOnly
from .forms.recipeform import RecipeForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics, status
from django.shortcuts import render
from django_filters import rest_framework
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db.models import Q

#The landing page(Home page) for a user apon successfull logging in.
def home(request):
    #All recipes in the database.
    recipes = Recipe.objects.all().count()
    authors = CustomUser.objects.all().count()

    context = {
        'recipes': recipes,
        'authors': authors,
    }

    #Render the home html template with the recipe data.
    return render(request, 'recipe/home.html', context=context)


# list view to display all the recipe instances.

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def recipe_list_view(request):
    #Fetch all the recipe instances.
    recipes = Recipe.objects.all()

    #Display the recipes in pages of 10 recipes per page.
    Pages = Paginator(recipes, 10)
    page_number = request.GET.get("page")
    page_obj = Pages.get_page(page_number)
    #Render the recipe instance pages through recipe_list template.
    return render(request, 'recipe/recipe_list.html', {'page_obj': page_obj})

#Detail view of a recipe.

@api_view(['GET'])
#User needs to be logged in in order to view a recipe detail.
@permission_classes([IsAuthenticatedOrReadOnly])
def recipe_detail_view(request, pk):

    try:
        #Retrieve a recipe instance using its unique primary key.
        recipe = Recipe.objects.get(pk = pk)

    except Recipe.DoesNotExist:
        #Raise error if the recipe is not found.
        raise Http404('Recipe does not exist.')
    
    #Render the recipe detail view to the respective template.
    return render(request, 'recipe/recipe_detail.html', context={'Recipe':recipe})

#List all recipe categories to aid user in category search.
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def category_list(request):
    try:
        #Retrieve all the recipe categories.
        categories = Recipe.objects.filter()
    #Use try except to raise an error message if there are no categories.
    except categories.DoesNotExist:
        raise Http404('The category list is empty.')
    return render(request, 'recipe/recipe_categories.html', context={'All categories':categories})

#Display recipe instances according to category.

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def recipe_category_view(request, self):
    #Request the user for a category to display recipes.
    query = self.request.GET.get('q')
    #Retrieve all the recipe instances in the category requested.
    recipes_category = Recipe.objects.filter(Q(category_icontains='query'))
    #Check if the category exists.
    if query is not None:
        template = loader.get_template('category_list.html')
        #Add the recipe instances to a dictionary.
        context = {
            'recipe_category_list': recipes_category,
        }
        return HttpResponse(template.render(context, request))

    else:
        return Http404('The category does not exist.')
        
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def recipe_ingredient_view(request, self):
    #Request the user for a ingredient to display recipes.
        query = self.request.GET.get('q')
        #Retrieve all the recipe instances for the ingredient requested.
        recipes_ingredient = Recipe.objects.filter(Q(ingredient_icontains='query'))
        #Check if the ingredient exists.
        if query is not None:
            template = loader.get_template('ingredient_list.html')
            #Add the recipe instances to a dictionary.
            context = {
                'recipe_ingredient_list': recipes_ingredient,
            }
            return HttpResponse(template.render(context, request))
        
#CRUD operations for recipies using django rest_framework.
#Recipe creation view.

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def create_recipe(request):
    #Empty dictionary for initial data of field names and keys.
    context = {}

    form = RecipeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('home')

    context['form'] = form
    return render(request, 'recipe/recipe_create.html', context)
    
class RecipeUpdate(APIView):
    template_name = 'recipe/recipe_update.html'
    permission_classes = [IsAuthenticatedOrReadOnly ]

    def get_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404
        
    def put(self, request, pk):
        recipe = self.get_object(pk)
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
@permission_classes([IsOwnerOrReadOnly])
def delete_recipe(self, request, pk):
    #Retrieve the recipe to be deleted.
    recipe = Recipe.objects.get(pk=pk)
    #Check if the recipe exists.
    if recipe is not None:
        try:
            #Delete the recipe then redirect user to home page.
            recipe.delete()
            return HttpResponseRedirect('home')
        except:
        #Raise error if the recipe does not exist.
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


    
#Recipe search and filter functionality.
class RecipeSearch(generics.ListAPIView):

    permission_classes = IsAuthenticatedOrReadOnly
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [rest_framework.DjangoFilterBackend]
    search_fields = ['title', 'category', 'ingredients', 'preparation_time']
    #Optional filters to refine the recipe search.
    filterset_fiels = ['cooking_time', 'preparation_time', 'servings']



