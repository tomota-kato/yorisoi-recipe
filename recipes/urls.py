from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    # カテゴリ関連
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # レシピ関連
    path('recipes/', views.RecipeListView.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipes/my/', views.MyRecipeListView.as_view(), name='my-recipe-list'),
    
    # お気に入り関連
    path('favorites/', views.FavoriteRecipeListView.as_view(), name='favorite-list'),
    path('recipes/<int:recipe_id>/favorite/', views.toggle_favorite, name='toggle-favorite'),
    
    # 評価関連
    path('recipes/<int:recipe_id>/rating/', views.recipe_rating, name='recipe-rating'),
    
    # 統計
    path('stats/', views.recipe_stats, name='recipe-stats'),
] 