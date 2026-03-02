#LaunchDarkly APIクライアント

LaunchDarklyのためのPythonクライアントです。機能フラグ管理機能を提供します。

## 概要

LaunchDarklyは機能フラグ管理プラットフォームです。このクライアントはAPIを介してLaunchDarklyにアクセスします。

## インストール

```bash
pip install requests
```

または：

```bash
pip install -r requirements.txt
```

## API キー発行

1. [LaunchDarkly]（https://launchdarkly.com/)에서アカウントの作成
2. API キー発行
3. 発行された鍵を安全に保存

##使用法

### 初期化

```python
from launchdarkly import LaunchDarklyClient, LaunchDarklyError

client = LaunchDarklyClient(
    access_token="YOUR_API_KEY",
    timeout=30
)
```

###主な機能

- flags
- projects
- environments

### 例

```python
# 프로젝트 조회
projects = client.get_projects()

# 플래그 조회
flags = client.get_flags("my-project")

# 특정 플래그 조회
flag = client.get_flag("my-project", "my-flag", environment_key="production")

# 플래그 생성
flag = client.create_flag(
    "my-project",
    "my-flag",
    name="My Flag",
    description="A feature flag"
)

# 환경 조회
environments = client.get_environments("my-project")
```

## エラー処理

```python
try:
    flags = client.get_flags("my-project")
except LaunchDarklyAuthenticationError:
    print("인증 실패")
except LaunchDarklyRateLimitError:
    print("속도 제한 초과")
except LaunchDarklyError as e:
    print(f"요청 실패: {str(e)}")
```

##ライセンス

MIT License

## サポート

- [LaunchDarkly Documentation](https://docs.launchdarkly.com/)