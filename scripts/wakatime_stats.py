"""Read WakaTime stats with OAuth, without exposing credentials in diagnostics."""
from urllib.error import HTTPError, URLError


def load_weekly(fetch, access_token='', legacy_key=''):
    credential = (access_token or legacy_key).strip()
    if not credential:
        return None, 'WakaTime 尚未連接', '連接 WakaTime 後自動顯示最近 7 天的編碼時間。'
    try:
        response = fetch(
            'https://api.wakatime.com/api/v1/users/current/stats/last_7_days',
            headers={'Authorization': 'Bearer ' + credential, 'Accept': 'application/json'},
        )
        weekly = response['data']
        if not isinstance(weekly, dict) or not isinstance(weekly.get('languages'), list):
            raise ValueError('Invalid statistics response')
        if weekly.get('is_up_to_date') is False:
            return weekly, 'WakaTime · 統計更新中', 'WakaTime 正在計算最近 7 天的編碼時間。'
        return weekly, '最近 7 天 · WakaTime', '在已啟用 WakaTime 的編輯器中編碼後自動累積。'
    except HTTPError as error:
        # Never log response bodies or exception messages: they may contain secrets.
        print(f'::warning::WakaTime stats request returned HTTP {error.code}')
        if error.code in (401, 403):
            return None, 'WakaTime 需要更新授權', '請在 Actions secret 中設定個人 OAuth token。'
        if error.code == 429:
            return None, 'WakaTime 稍後重試', '請求暫時受限，將於下次自動更新時重試。'
    except (URLError, TimeoutError, OSError):
        print('::warning::WakaTime stats request failed: network unavailable')
    except (KeyError, TypeError, ValueError):
        print('::warning::WakaTime returned an invalid statistics response')
    return None, 'WakaTime 暫時無法更新', '統計讀取失敗，將於下次自動更新時重試。'
