from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Category, Recipe, Ingredient, Step
import random


class Command(BaseCommand):
    help = 'サンプルデータを作成します'

    def handle(self, *args, **options):
        self.stdout.write('サンプルデータを作成中...')

        # カテゴリを作成
        categories_data = [
            {'name': '和食', 'description': '日本の伝統的な料理'},
            {'name': '洋食', 'description': '西洋の料理'},
            {'name': '中華', 'description': '中国の料理'},
            {'name': 'イタリアン', 'description': 'イタリアの料理'},
            {'name': 'デザート', 'description': 'スイーツ・デザート'},
            {'name': 'サラダ', 'description': '野菜中心の料理'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'カテゴリ「{category.name}」を作成しました')

        # スーパーユーザーを取得
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                self.stdout.write(self.style.ERROR('スーパーユーザーが見つかりません'))
                return
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('スーパーユーザーが見つかりません'))
            return

        # サンプルレシピを作成
        recipes_data = [
            {
                'title': '基本の親子丼',
                'description': '鶏肉と卵で作る定番の親子丼です。',
                'category': '和食',
                'cooking_time': 20,
                'servings': 2,
                'difficulty': 1,
                'ingredients': [
                    {'name': '鶏もも肉', 'amount': '200', 'unit': 'g'},
                    {'name': '卵', 'amount': '3', 'unit': '個'},
                    {'name': '玉ねぎ', 'amount': '1/2', 'unit': '個'},
                    {'name': 'ご飯', 'amount': '2', 'unit': '杯'},
                    {'name': 'だし汁', 'amount': '150', 'unit': 'ml'},
                    {'name': '醤油', 'amount': '2', 'unit': '大さじ'},
                    {'name': 'みりん', 'amount': '1', 'unit': '大さじ'},
                    {'name': '砂糖', 'amount': '1', 'unit': '小さじ'},
                ],
                'steps': [
                    {'step_number': 1, 'description': '鶏肉を一口大に切り、玉ねぎをスライスします。'},
                    {'step_number': 2, 'description': 'フライパンにだし汁、醤油、みりん、砂糖を入れて煮立てます。'},
                    {'step_number': 3, 'description': '鶏肉と玉ねぎを加えて中火で5分程度煮ます。'},
                    {'step_number': 4, 'description': '溶き卵を回し入れ、半熟状態になったら火を止めます。'},
                    {'step_number': 5, 'description': 'ご飯の上にのせて完成です。'},
                ]
            },
            {
                'title': 'クリームパスタ',
                'description': '濃厚なクリームソースのパスタです。',
                'category': 'イタリアン',
                'cooking_time': 25,
                'servings': 2,
                'difficulty': 2,
                'ingredients': [
                    {'name': 'パスタ', 'amount': '200', 'unit': 'g'},
                    {'name': 'ベーコン', 'amount': '100', 'unit': 'g'},
                    {'name': '玉ねぎ', 'amount': '1/2', 'unit': '個'},
                    {'name': '生クリーム', 'amount': '200', 'unit': 'ml'},
                    {'name': 'パルメザンチーズ', 'amount': '50', 'unit': 'g'},
                    {'name': 'にんにく', 'amount': '2', 'unit': '片'},
                    {'name': 'オリーブオイル', 'amount': '2', 'unit': '大さじ'},
                ],
                'steps': [
                    {'step_number': 1, 'description': 'パスタを茹で始めます。'},
                    {'step_number': 2, 'description': 'ベーコンと玉ねぎ、にんにくを炒めます。'},
                    {'step_number': 3, 'description': '生クリームを加えて煮詰めます。'},
                    {'step_number': 4, 'description': '茹で上がったパスタを加えて絡めます。'},
                    {'step_number': 5, 'description': 'チーズを加えて完成です。'},
                ]
            },
            {
                'title': 'チョコレートケーキ',
                'description': 'しっとりとしたチョコレートケーキです。',
                'category': 'デザート',
                'cooking_time': 60,
                'servings': 6,
                'difficulty': 3,
                'ingredients': [
                    {'name': 'チョコレート', 'amount': '200', 'unit': 'g'},
                    {'name': 'バター', 'amount': '100', 'unit': 'g'},
                    {'name': '卵', 'amount': '3', 'unit': '個'},
                    {'name': '砂糖', 'amount': '80', 'unit': 'g'},
                    {'name': '薄力粉', 'amount': '50', 'unit': 'g'},
                    {'name': 'ココアパウダー', 'amount': '20', 'unit': 'g'},
                ],
                'steps': [
                    {'step_number': 1, 'description': 'オーブンを180度に予熱します。'},
                    {'step_number': 2, 'description': 'チョコレートとバターを湯煎で溶かします。'},
                    {'step_number': 3, 'description': '卵と砂糖を混ぜ、チョコレートを加えます。'},
                    {'step_number': 4, 'description': '粉類をふるい入れて混ぜます。'},
                    {'step_number': 5, 'description': '型に入れて40分焼きます。'},
                ]
            }
        ]

        for recipe_data in recipes_data:
            category = Category.objects.get(name=recipe_data['category'])
            
            recipe, created = Recipe.objects.get_or_create(
                title=recipe_data['title'],
                defaults={
                    'description': recipe_data['description'],
                    'category': category,
                    'cooking_time': recipe_data['cooking_time'],
                    'servings': recipe_data['servings'],
                    'difficulty': recipe_data['difficulty'],
                    'author': admin_user,
                }
            )

            if created:
                self.stdout.write(f'レシピ「{recipe.title}」を作成しました')

                # 材料を作成
                for i, ingredient_data in enumerate(recipe_data['ingredients']):
                    Ingredient.objects.create(
                        recipe=recipe,
                        name=ingredient_data['name'],
                        amount=ingredient_data['amount'],
                        unit=ingredient_data['unit'],
                        order=i + 1
                    )

                # 手順を作成
                for step_data in recipe_data['steps']:
                    Step.objects.create(
                        recipe=recipe,
                        step_number=step_data['step_number'],
                        description=step_data['description']
                    )

        self.stdout.write(
            self.style.SUCCESS('サンプルデータの作成が完了しました！')
        ) 