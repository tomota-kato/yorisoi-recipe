from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    """材料マスタ"""
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="材料名",
        help_text="材料の名前（例: 玉ねぎ、鶏胸肉）"
    )
    category = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="カテゴリ",
        help_text="材料のカテゴリ（例: 野菜、肉類、調味料）"
    )
    unit = models.CharField(
        max_length=20, 
        default="個", 
        verbose_name="単位",
        help_text="材料の基本単位（例: 個、g、ml）"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "材料"
        verbose_name_plural = "材料"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.unit})"


class UserInventory(models.Model):
    """ユーザーの在庫管理（オプション機能）"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="ユーザー"
    )
    ingredient = models.ForeignKey(
        Ingredient, 
        on_delete=models.CASCADE, 
        verbose_name="材料"
    )
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="在庫数量"
    )
    expiry_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="賞味期限"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "在庫"
        verbose_name_plural = "在庫"
        unique_together = ['user', 'ingredient']

    def __str__(self):
        return f"{self.user.username} - {self.ingredient.name}: {self.quantity}{self.ingredient.unit}" 