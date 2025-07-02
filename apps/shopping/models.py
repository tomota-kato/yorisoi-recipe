from django.db import models
from django.contrib.auth.models import User
from apps.menus.models import WeeklyMenu
from apps.ingredients.models import Ingredient
from datetime import datetime, timedelta


class ShoppingList(models.Model):
    """買い物リスト"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="ユーザー"
    )
    name = models.CharField(
        max_length=100, 
        verbose_name="買い物リスト名",
        help_text="例: 6/15(水)の買い物"
    )
    target_date = models.DateField(
        verbose_name="買い物予定日",
        help_text="買い物に行く予定の日"
    )
    
    # 関連する献立（複数の週献立から生成される場合がある）
    weekly_menus = models.ManyToManyField(
        WeeklyMenu,
        blank=True,
        verbose_name="対象献立",
        help_text="この買い物リストの対象となる週献立"
    )
    
    # 自動生成関連
    is_auto_generated = models.BooleanField(
        default=False, 
        verbose_name="自動生成",
        help_text="システムによって自動生成されたリストかどうか"
    )
    generation_period_start = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="生成対象期間開始",
        help_text="リスト生成時の対象期間の開始日"
    )
    generation_period_end = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="生成対象期間終了", 
        help_text="リスト生成時の対象期間の終了日"
    )
    
    # 通知関連
    is_notified = models.BooleanField(
        default=False, 
        verbose_name="通知済み",
        help_text="ユーザーに通知済みかどうか"
    )
    notification_sent_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="通知送信日時"
    )
    
    # 買い物状況
    is_completed = models.BooleanField(
        default=False, 
        verbose_name="買い物完了",
        help_text="買い物が完了したかどうか"
    )
    completed_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="完了日時"
    )
    
    notes = models.TextField(
        blank=True, 
        verbose_name="メモ",
        help_text="買い物時の注意点など"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "買い物リスト"
        verbose_name_plural = "買い物リスト"
        ordering = ['-target_date', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.target_date})"

    @property
    def total_items(self):
        """アイテム総数を取得"""
        return self.items.count()

    @property
    def completed_items(self):
        """完了済みアイテム数を取得"""
        return self.items.filter(is_purchased=True).count()

    @property
    def completion_rate(self):
        """完了率を取得"""
        if self.total_items == 0:
            return 0
        return round((self.completed_items / self.total_items) * 100, 1)


class ShoppingListItem(models.Model):
    """買い物リストのアイテム"""
    CATEGORY_CHOICES = [
        ('vegetables', '野菜'),
        ('fruits', '果物'),
        ('meat', '肉類'),
        ('fish', '魚介類'),
        ('dairy', '乳製品'),
        ('grains', '穀物・主食'),
        ('seasonings', '調味料'),
        ('beverages', '飲み物'),
        ('snacks', 'お菓子'),
        ('frozen', '冷凍食品'),
        ('others', 'その他'),
    ]

    shopping_list = models.ForeignKey(
        ShoppingList, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="買い物リスト"
    )
    ingredient = models.ForeignKey(
        Ingredient, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="材料",
        help_text="登録済み材料の場合"
    )
    
    # 手動追加の場合
    custom_name = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="カスタム名",
        help_text="材料マスタにない場合の名前"
    )
    
    quantity = models.CharField(
        max_length=50, 
        verbose_name="必要量",
        help_text="例: 2個、300g、1パック"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='others',
        verbose_name="カテゴリ"
    )
    
    # 購入状況
    is_purchased = models.BooleanField(
        default=False, 
        verbose_name="購入済み"
    )
    purchased_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="購入日時"
    )
    actual_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="実際の価格"
    )
    
    # 表示順序とプライオリティ
    order = models.PositiveIntegerField(
        default=1, 
        verbose_name="表示順序"
    )
    priority = models.CharField(
        max_length=10,
        choices=[
            ('high', '高'),
            ('medium', '中'),
            ('low', '低'),
        ],
        default='medium',
        verbose_name="優先度"
    )
    
    notes = models.TextField(
        blank=True, 
        verbose_name="メモ",
        help_text="特売情報、代替品など"
    )

    class Meta:
        verbose_name = "買い物アイテム"
        verbose_name_plural = "買い物アイテム"
        ordering = ['category', 'order', 'id']

    def __str__(self):
        name = self.ingredient.name if self.ingredient else self.custom_name
        return f"{self.shopping_list.name} - {name}: {self.quantity}"

    @property
    def display_name(self):
        """表示用の名前を取得"""
        return self.ingredient.name if self.ingredient else self.custom_name

    def mark_as_purchased(self):
        """購入済みとしてマーク"""
        self.is_purchased = True
        self.purchased_at = datetime.now()
        self.save()


class ShoppingNotification(models.Model):
    """買い物通知ログ"""
    NOTIFICATION_TYPES = [
        ('reminder', 'リマインダー'),
        ('list_ready', 'リスト作成完了'),
        ('weekly_prep', '週次準備'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="ユーザー"
    )
    shopping_list = models.ForeignKey(
        ShoppingList, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="買い物リスト"
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name="通知タイプ"
    )
    title = models.CharField(
        max_length=100, 
        verbose_name="通知タイトル"
    )
    message = models.TextField(
        verbose_name="通知メッセージ"
    )
    is_sent = models.BooleanField(
        default=False, 
        verbose_name="送信済み"
    )
    sent_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="送信日時"
    )
    error_message = models.TextField(
        blank=True, 
        verbose_name="エラーメッセージ",
        help_text="送信に失敗した場合のエラー内容"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    class Meta:
        verbose_name = "買い物通知"
        verbose_name_plural = "買い物通知"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.created_at.strftime('%Y/%m/%d %H:%M')})" 