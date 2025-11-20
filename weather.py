import requests


# 1. 地名 → 緯度 / 経度（Open-Meteo のジオコーディング）
def get_latlon(place: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": place,
        "count": 1,
        "language": "ja",
        "format": "json"
    }
    
    r = requests.get(url, params=params).json()
    
    if "results" not in r:
        return None

    result = r["results"][0]
    return result["latitude"], result["longitude"], result["name"]


# 2. 現在の天気を取得
def get_weather_api(place: str):
    pos = get_latlon(place)
    if not pos:
        return f"{place} の位置が見つかりませんでした。"

    lat, lon, loc_name = pos

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "weather_code"],
        "timezone": "Asia/Tokyo",
    }

    r = requests.get(url, params=params).json()

    temp = r["current"]["temperature_2m"]
    wcode = r["current"]["weather_code"]

    # weather_code → 日本語変換表
    weather_map = {
        0: "快晴",
        1: "晴れ",
        2: "薄曇り",
        3: "曇り",
        45: "霧",
        48: "霧（着氷性）",
        51: "霧雨",
        53: "霧雨（中）",
        55: "霧雨（強）",
        61: "弱い雨",
        63: "雨",
        65: "強い雨",
        71: "雪",
        73: "雪（中）",
        75: "大雪",
        80: "にわか雨",
        81: "雨（中）",
        82: "激しい雨",
        95: "雷雨",
        96: "雷雨（雹あり）",
        99: "雷雨（ひどい雹）",
    }

    weather = weather_map.get(wcode, f"不明（コード: {wcode}）")

    return f"{loc_name} の現在の天気：{weather}, {temp}℃"


# 3. テスト
if __name__ == "__main__":
    print(get_weather_api("東京"))