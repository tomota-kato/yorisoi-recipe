from django.contrib import admin
from .models import Category, Recipe, Ingredient, Step, RecipeFavorite, RecipeRating


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 3
    fields = ['name', 'amount', 'unit', 'notes', 'order']


class StepInline(admin.TabularInline):
    model = Step
    extra = 3
    fields = ['step_number', 'description', 'cooking_time']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'author', 'cooking_time', 
        'servings', 'difficulty', 'is_public', 'created_at'
    ]
    list_filter = [
        'category', 'difficulty', 'is_public', 'created_at', 'author'
    ]
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'description', 'category', 'author')
        }),
        ('調理情報', {
            'fields': ('cooking_time', 'servings', 'difficulty')
        }),
        ('メディア', {
            'fields': ('youtube_url', 'image')
        }),
        ('設定', {
            'fields': ('is_public',)
        }),
        ('メタデータ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [IngredientInline, StepInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # 新規作成時
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'name', 'amount', 'unit', 'order']
    list_filter = ['unit', 'recipe__category']
    search_fields = ['name', 'recipe__title']
    ordering = ['recipe', 'order']


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'step_number', 'description', 'cooking_time']
    list_filter = ['recipe__category']
    search_fields = ['description', 'recipe__title']
    ordering = ['recipe', 'step_number']


@admin.register(RecipeFavorite)
class RecipeFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'created_at']
    list_filter = ['created_at', 'recipe__category']
    search_fields = ['user__username', 'recipe__title']
    ordering = ['-created_at']


@admin.register(RecipeRating)
class RecipeRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'recipe__category']
    search_fields = ['user__username', 'recipe__title', 'comment']
    ordering = ['-created_at']
