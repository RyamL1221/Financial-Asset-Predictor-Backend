from typing import List, Dict, Any
from src.util.types import RecommendationType

def analyze_rsi_current(rsi_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze current RSI position and provide recommendation"""
    if not rsi_entries:
        return {
            'recommendation': 'HOLD',
            'analysis': 'No RSI data available',
            'confidence': 50
        }
    
    latest_rsi = rsi_entries[-1]
    rsi_value = latest_rsi.get('value', 50)
    
    if rsi_value < 30:
        recommendation = 'BUY'
        analysis = f"RSI at {rsi_value:.2f} indicates oversold conditions. This suggests the stock may be undervalued and could be a good buying opportunity."
        confidence = 80
    elif rsi_value < 40:
        recommendation = 'OUTPERFORM'
        analysis = f"RSI at {rsi_value:.2f} shows oversold tendencies. The stock may be approaching a buying opportunity."
        confidence = 65
    elif rsi_value > 70:
        recommendation = 'SELL'
        analysis = f"RSI at {rsi_value:.2f} indicates overbought conditions. This suggests the stock may be overvalued and could be due for a correction."
        confidence = 80
    elif rsi_value > 60:
        recommendation = 'UNDERPERFORM'
        analysis = f"RSI at {rsi_value:.2f} shows overbought tendencies. The stock may be approaching resistance levels."
        confidence = 65
    else:
        recommendation = 'HOLD'
        analysis = f"RSI at {rsi_value:.2f} is in neutral territory (40-60). No strong buy or sell signals from RSI at this time."
        confidence = 50
    
    return {
        'recommendation': recommendation,
        'analysis': analysis,
        'confidence': confidence,
        'rsi_value': rsi_value
    }

def get_rsi_confirmation_bonus(rsi_value: float, current_recommendation: RecommendationType) -> Dict[str, Any]:
    """Get RSI confirmation bonus for current recommendation"""
    bonus = {
        'confidence_boost': 0,
        'reasoning': '',
        'technical_factor': ''
    }
    
    if rsi_value < 30 and current_recommendation == 'OUTPERFORM':
        bonus['confidence_boost'] = 10
        bonus['reasoning'] = 'RSI indicates oversold conditions'
        bonus['technical_factor'] = 'RSI oversold confirmation'
    elif rsi_value > 70 and current_recommendation == 'UNDERPERFORM':
        bonus['confidence_boost'] = 10
        bonus['reasoning'] = 'RSI indicates overbought conditions'
        bonus['technical_factor'] = 'RSI overbought confirmation'
    elif rsi_value < 40 and current_recommendation == 'OUTPERFORM':
        bonus['confidence_boost'] = 5
        bonus['reasoning'] = 'RSI showing oversold tendencies'
        bonus['technical_factor'] = 'RSI oversold tendency'
    elif rsi_value > 60 and current_recommendation == 'OUTPERFORM':
        bonus['confidence_boost'] = 5
        bonus['reasoning'] = 'RSI showing overbought tendencies'
        bonus['technical_factor'] = 'RSI overbought tendency'
    
    return bonus 