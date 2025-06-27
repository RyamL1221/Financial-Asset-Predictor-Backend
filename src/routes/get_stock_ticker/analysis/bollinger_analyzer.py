from typing import List, Dict, Any
from src.util.types import RecommendationType

def analyze_bollinger_current(bollinger_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze current Bollinger Bands position and provide recommendation"""
    if not bollinger_entries:
        return {
            'recommendation': 'HOLD',
            'analysis': 'No Bollinger Bands data available',
            'confidence': 50
        }
    
    latest_bollinger = bollinger_entries[-1]
    upper_band = float(latest_bollinger.get('upper_band', 0))
    middle_band = float(latest_bollinger.get('middle_band', 0))
    lower_band = float(latest_bollinger.get('lower_band', 0))
    
    # Analyze band width and volatility
    band_width = upper_band - lower_band
    average_band_width = (upper_band + lower_band) / 2
    volatility_ratio = band_width / average_band_width if average_band_width > 0 else 0
    
    if volatility_ratio > 0.1:
        recommendation = 'HOLD'
        analysis = f"Bollinger Bands show high volatility ({(volatility_ratio * 100):.1f}% band width). This suggests increased market uncertainty. Consider waiting for clearer signals."
        confidence = 60
    elif volatility_ratio < 0.05:
        recommendation = 'OUTPERFORM'
        analysis = f"Bollinger Bands show low volatility ({(volatility_ratio * 100):.1f}% band width). This suggests a potential breakout may be imminent."
        confidence = 70
    else:
        recommendation = 'HOLD'
        analysis = f"Bollinger Bands show normal volatility ({(volatility_ratio * 100):.1f}% band width). No significant breakout signals at this time."
        confidence = 50
    
    return {
        'recommendation': recommendation,
        'analysis': analysis,
        'confidence': confidence,
        'upper_band': upper_band,
        'middle_band': middle_band,
        'lower_band': lower_band,
        'volatility_ratio': volatility_ratio
    } 