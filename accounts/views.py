from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
import json
from .models import UserProfile


class UserProfileAPIView(APIView):
    """ユーザープロフィールAPI"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """プロフィール情報を取得"""
        try:
            profile = request.user.userprofile
            data = {
                'user_id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'full_name': profile.full_name,
                'bio': profile.bio,
                'avatar': profile.avatar.url if profile.avatar else None,
                'birth_date': profile.birth_date,
                'email_notifications': profile.email_notifications,
                'favorite_cuisine': profile.favorite_cuisine,
                'dietary_restrictions': profile.dietary_restrictions,
                'created_at': profile.created_at,
                'updated_at': profile.updated_at,
            }
            return Response(data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'プロフィールが見つかりません'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request):
        """プロフィール情報を更新"""
        try:
            profile = request.user.userprofile
            data = request.data
            
            # ユーザー基本情報の更新
            if 'first_name' in data:
                request.user.first_name = data['first_name']
            if 'last_name' in data:
                request.user.last_name = data['last_name']
            request.user.save()
            
            # プロフィール情報の更新
            if 'bio' in data:
                profile.bio = data['bio']
            if 'birth_date' in data:
                profile.birth_date = data['birth_date']
            if 'email_notifications' in data:
                profile.email_notifications = data['email_notifications']
            if 'favorite_cuisine' in data:
                profile.favorite_cuisine = data['favorite_cuisine']
            if 'dietary_restrictions' in data:
                profile.dietary_restrictions = data['dietary_restrictions']
            
            profile.save()
            
            return Response(
                {'message': 'プロフィールを更新しました'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'プロフィールの更新に失敗しました: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """ユーザー登録API"""
    try:
        data = request.data
        
        # 必須フィールドの確認
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return Response(
                    {'error': f'{field}は必須です'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # ユーザー名の重複チェック
        if User.objects.filter(username=data['username']).exists():
            return Response(
                {'error': 'このユーザー名は既に使用されています'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # メールアドレスの重複チェック
        if User.objects.filter(email=data['email']).exists():
            return Response(
                {'error': 'このメールアドレスは既に使用されています'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # ユーザー作成
        with transaction.atomic():
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', '')
            )
            
            # プロフィールは自動的に作成される（signalによる）
            
            return Response(
                {
                    'message': 'ユーザー登録が完了しました',
                    'user_id': user.id,
                    'username': user.username
                }, 
                status=status.HTTP_201_CREATED
            )
            
    except Exception as e:
        return Response(
            {'error': f'ユーザー登録に失敗しました: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# HTML画面用のビュー
def login_view(request):
    """ログイン画面"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'auth/login.html')


def register_view(request):
    """新規登録画面"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'auth/register.html')


def dashboard_view(request):
    """ダッシュボード画面"""
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html', {
        'user': request.user,
    })


# 基本的なAPI（JSONレスポンス）
@csrf_exempt
def login_api(request):
    """ログインAPI（簡易版）"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'message': 'ログインしました',
                    'user_id': user.id,
                    'username': user.username
                })
            else:
                return JsonResponse({'error': 'ユーザー名またはパスワードが正しくありません'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'POSTメソッドが必要です'}, status=405)


@csrf_exempt
def logout_api(request):
    """ログアウトAPI（簡易版）"""
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'ログアウトしました'})
    
    return JsonResponse({'error': 'POSTメソッドが必要です'}, status=405)
