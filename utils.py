from astroquery.jplhorizons import Horizons
import pandas as pd
from datetime import datetime, timedelta

# 定義行星資料
PLANETS = {
    '水星': '199',
    '金星': '299',
    '地球': '399',
    '火星': '499',
    '木星': '599',
    '土星': '699',
    '天王星': '799',
    '海王星': '899'
}

def get_planet_data(planet_id: str, start_date: str, end_date: str):
    """
    取得行星位置資料
    
    Args:
        planet_id: JPL Horizons 系統中的行星 ID
        start_date: 開始日期 (YYYY-MM-DD)
        end_date: 結束日期 (YYYY-MM-DD)
    
    Returns:
        ephemerides table
    """
    try:
        # 建立 Horizons 物件（觀測位置設為地心）
        obj = Horizons(
            id=planet_id,
            location='@sun',
            epochs={
                'start': start_date,
                'stop': end_date,
                'step': '1d'
            }
        )
        
        # 獲取星曆表
        eph = obj.ephemerides()
        return eph
        
    except Exception as e:
        print(f"獲取行星資料時發生錯誤: {str(e)}")
        return None

def format_hover_text(row):
    """格式化滑鼠懸停時顯示的文字"""
    return (
        f"日期: {row['datetime_str']}<br>"
        f"赤經: {row['RA']:.2f}°<br>"
        f"赤緯: {row['DEC']:.2f}°<br>"
        f"距離: {row['delta']:.2f} AU"
    )
