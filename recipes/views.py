from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import models
from .models import Category, Recipe, Ingredient, Step, RecipeFavorite, RecipeRating
from .serializers import (
    CategorySerializer, RecipeListSerializer, RecipeDetailSerializer,
    RecipeCreateSerializer, RecipeFavoriteSerializer, RecipeRatingSerializer
)


class CategoryListView(generics.ListCreateAPIView):
    """カテゴリ一覧・作成API"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """カテゴリ詳細・更新・削除API"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RecipeListView(generics.ListCreateAPIView):
    """レシピ一覧・作成API"""
    queryset = Recipe.objects.filter(is_public=True)
    serializer_class = RecipeListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'author']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'cooking_time', 'favorite_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateSerializer
        return RecipeListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """レシピ詳細・更新・削除API"""
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RecipeCreateSerializer
        return RecipeDetailSerializer

    def get_queryset(self):
        """作成者または公開レシピのみ取得"""
        if self.request.user.is_authenticated:
            return Recipe.objects.filter(
                models.Q(author=self.request.user) | models.Q(is_public=True)
            )
        return Recipe.objects.filter(is_public=True)


class MyRecipeListView(generics.ListAPIView):
    """自分のレシピ一覧API"""
    serializer_class = RecipeListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)


class FavoriteRecipeListView(generics.ListAPIView):
    """お気に入りレシピ一覧API"""
    serializer_class = RecipeFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RecipeFavorite.objects.filter(user=self.request.user)


@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def toggle_favorite(request, recipe_id):
    """レシピのお気に入り切り替えAPI"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if request.method == 'POST':
        favorite, created = RecipeFavorite.objects.get_or_create(
            user=request.user, recipe=recipe
        )
        if created:
            return Response({'message': 'お気に入りに追加しました'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '既にお気に入りに登録済みです'}, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        try:
            favorite = RecipeFavorite.objects.get(user=request.user, recipe=recipe)
            favorite.delete()
            return Response({'message': 'お気に入りから削除しました'}, status=status.HTTP_200_OK)
        except RecipeFavorite.DoesNotExist:
            return Response({'message': 'お気に入りに登録されていません'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def recipe_rating(request, recipe_id):
    """レシピ評価API"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if request.method == 'POST':
        serializer = RecipeRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        try:
            rating = RecipeRating.objects.get(user=request.user, recipe=recipe)
            serializer = RecipeRatingSerializer(rating, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except RecipeRating.DoesNotExist:
            return Response({'message': '評価が見つかりません'}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'DELETE':
        try:
            rating = RecipeRating.objects.get(user=request.user, recipe=recipe)
            rating.delete()
            return Response({'message': '評価を削除しました'}, status=status.HTTP_200_OK)
        except RecipeRating.DoesNotExist:
            return Response({'message': '評価が見つかりません'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def recipe_stats(request):
    """レシピ統計API"""
    stats = {
        'total_recipes': Recipe.objects.filter(is_public=True).count(),
        'total_categories': Category.objects.count(),
        'total_users': User.objects.count(),
        'recent_recipes': RecipeListSerializer(
            Recipe.objects.filter(is_public=True)[:5], 
            many=True, 
            context={'request': request}
        ).data
    }
    return Response(stats)
