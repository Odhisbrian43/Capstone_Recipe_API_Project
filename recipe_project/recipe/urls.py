from django.urls import path, include
from . import views

#Url for the deferent views.

urlpatterns = [
    path('', view = views.home, name = 'home'),
    path('recipe_list/', view=views.recipe_list_view, name='list'),
    path('detail/<int:pk>', view=views.recipe_detail_view, name='detail'),
    path('categories/', view=views.recipe_category_view, name='category_view'),
    path('ingredients/', view=views.recipe_ingredient_view, name='ingredient_view'),
    path('search/', view=views.RecipeSearch.as_view(), name='search'),
    path(
        'crud_operations/',
        include(
            [
                path('create/', view=views.create_recipe),
                path('update/<int:pk>/', view=views.RecipeUpdate.as_view()),
                path('delete/<int:pk>/', view=views.delete_recipe, name='recipe-delete'),
            ]
        )
    )
]