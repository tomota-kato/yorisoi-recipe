# yorisoi recipe

> わたしの暮らしに、yorisoi recipe  
> あなたの毎日に寄り添う、心温まるレシピパートナー

## 📖 プロジェクト概要

「yorisoi recipe」は、YouTubeの料理動画からAIが自動でレシピを抽出し、献立作成から買い物リスト生成まで一貫してサポートする献立管理アプリケーションです。

### 🎯 コアコンセプト
- **AIアシスト**: YouTubeリンクから自動でレシピを生成
- **献立管理**: 週単位での献立作成・編集
- **買い物サポート**: 献立から自動で買い物リスト生成
- **寄り添うUX**: 女性ユーザーに優しい温かみのあるデザイン

## 🚀 開発ステータス

### ✅ Phase 0: モックアップ作成（完了）
- ブランディング・デザインシステム確立
- 7画面の完全動作HTMLモックアップ
- レスポンシブ対応・アイコンシステム導入

### 🔄 Phase 1: 技術検証（予定）
- YouTube Data API連携検証
- Generative AI API連携検証

### 📋 Phase 2: 基本レシピ管理（予定）
- Django プロジェクトセットアップ
- ユーザー認証機能
- レシピCRUD機能

## 🎨 デザインシステム

### カラーパレット
- **ベース**: 優しいアイボリー `#F8F5F0`
- **メイン**: 温かみのあるテラコッタ `#E5A36C`
- **アクセント**: セージグリーン `#A3B899`

### フォント
- **見出し**: M PLUS Rounded 1c（丸ゴシック体）
- **本文**: Noto Sans JP
- **英数字**: Nunito

## 📁 プロジェクト構成

```
献立アプリ/
├── モックアップ画面/          # Phase 0: HTMLモックアップ
│   ├── index.html           # 画面一覧
│   ├── dashboard.html       # ダッシュボード
│   ├── recipe-create.html   # AIレシピ作成
│   ├── recipes.html         # レシピ一覧
│   ├── calendar.html        # 献立カレンダー
│   ├── shopping.html        # 買い物リスト
│   ├── common.css          # 統一スタイル
│   └── yorisoi-logo.svg    # ブランドロゴ
├── 要件定義.md              # プロジェクト要件定義
├── 開発履歴.md              # 開発フェーズ管理
└── README.md               # このファイル
```

## 🛠️ 技術スタック

### フロントエンド
- HTML5/CSS3/JavaScript（ES6+）
- CSS Grid & Flexbox
- Iconify（Lucideアイコン）
- レスポンシブデザイン

### バックエンド（予定）
- Django（Python）
- PostgreSQL/MySQL
- Django REST Framework

### 外部API（予定）
- YouTube Data API
- Generative AI API（OpenAI/Google Gemini）

## 🚀 モックアップの確認方法

1. `モックアップ画面/index.html` をブラウザで開く
2. 各画面のリンクをクリックして画面遷移を確認
3. レスポンシブ表示を確認（デベロッパーツールでモバイル表示切り替え）

## 📈 今後の開発予定

1. **Phase 1**: YouTube・AI API連携の技術検証
2. **Phase 2**: Django基盤とレシピCRUD機能
3. **Phase 3**: AIレシピ作成機能の実装
4. **Phase 4**: 献立作成機能
5. **Phase 5**: 買い物リスト生成機能

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 👥 コントリビューション

プロジェクトへの貢献を歓迎します！Issueやプルリクエストをお気軽にお送りください。

---

**yorisoi recipe** - あなたの毎日に寄り添う、心温まるレシピパートナー 🌿💕 