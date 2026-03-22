def get_weather(city: str) -> str:
    """
    查询城市的天气信息（教学演示用，支持有限的城市）。
    """
    # 硬编码的天气数据，用于教学演示
    weather_data = {
        "上海": {"desc": "晴", "temp": 18},
        "Shanghai": {"desc": "晴", "temp": 18},
        "北京": {"desc": "多云", "temp": 12},
        "Beijing": {"desc": "多云", "temp": 12},
        "广州": {"desc": "小雨", "temp": 22},
        "Guangzhou": {"desc": "小雨", "temp": 22},
        "深圳": {"desc": "小雨", "temp": 23},
        "Shenzhen": {"desc": "小雨", "temp": 23},
        "杭州": {"desc": "阴", "temp": 16},
        "Hangzhou": {"desc": "阴", "temp": 16},
    }

    if city in weather_data:
        data = weather_data[city]
        return f"{city}当前天气:{data['desc']}，气温{data['temp']}摄氏度"
    else:
        return f"错误：不支持的城市 '{city}'。目前支持的城市有：上海、北京、广州、深圳、杭州"
