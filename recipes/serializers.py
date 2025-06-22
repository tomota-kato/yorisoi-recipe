from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Recipe, Ingredient, Step, RecipeFavorite, RecipeRating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'amount', 'unit', 'notes', 'order']


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'step_number', 'description', 'image', 'cooking_time']


class RecipeListSerializer(serializers.ModelSerializer):
    """レシピ一覧用のシリアライザー（軽量版）"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    favorite_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'image', 'cooking_time', 
            'servings', 'difficulty', 'category', 'author', 
            'favorite_count', 'created_at', 'updated_at'
        ]


class RecipeDetailSerializer(serializers.ModelSerializer):
    """レシピ詳細用のシリアライザー（完全版）"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    steps = StepSerializer(many=True, read_only=True)
    favorite_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'youtube_url', 'image',
            'cooking_time', 'servings', 'difficulty', 'category',
            'author', 'ingredients', 'steps', 'favorite_count',
            'created_at', 'updated_at', 'is_public'
        ]


class RecipeCreateSerializer(serializers.ModelSerializer):
    """レシピ作成用のシリアライザー"""
    ingredients = IngredientSerializer(many=True, required=False)
    steps = StepSerializer(many=True, required=False)
    
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'youtube_url', 'image',
            'cooking_time', 'servings', 'difficulty', 'category',
            'ingredients', 'steps', 'is_public'
        ]
    
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        steps_data = validated_data.pop('steps', [])
        
        # レシピを作成
        recipe = Recipe.objects.create(**validated_data)
        
        # 材料を作成
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        
        # 手順を作成
        for step_data in steps_data:
            Step.objects.create(recipe=recipe, **step_data)
        
        return recipe
    
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        steps_data = validated_data.pop('steps', [])
        
        # レシピ基本情報を更新
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 既存の材料と手順を削除
        instance.ingredients.all().delete()
        instance.steps.all().delete()
        
        # 新しい材料を作成
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=instance, **ingredient_data)
        
        # 新しい手順を作成
        for step_data in steps_data:
            Step.objects.create(recipe=instance, **step_data)
        
        return instance


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    recipe = RecipeListSerializer(read_only=True)
    
    class Meta:
        model = RecipeFavorite
        fields = ['id', 'recipe', 'created_at']


class RecipeRatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    recipe = RecipeListSerializer(read_only=True)
    
    class Meta:
        model = RecipeRating
        fields = ['id', 'user', 'recipe', 'rating', 'comment', 'created_at', 'updated_at'] 