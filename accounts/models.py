from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """ユーザープロフィール拡張"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='ユーザー')
    bio = models.TextField('自己紹介', max_length=500, blank=True)
    avatar = models.ImageField('アバター', upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField('生年月日', blank=True, null=True)
    
    # 設定
    email_notifications = models.BooleanField('メール通知', default=True)
    favorite_cuisine = models.CharField('好きな料理ジャンル', max_length=100, blank=True)
    dietary_restrictions = models.CharField('食事制限', max_length=200, blank=True)
    
    # メタデータ
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'ユーザープロフィール'
        verbose_name_plural = 'ユーザープロフィール'

    def __str__(self):
        return f"{self.user.username}のプロフィール"

    @property
    def full_name(self):
        """フルネームを取得"""
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ユーザー作成時にプロフィールを自動作成"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """ユーザー保存時にプロフィールも保存"""
    instance.userprofile.save()
