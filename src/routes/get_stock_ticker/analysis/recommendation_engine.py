from typing import List, Dict, Any
from datetime import datetime
from src.util.types import RecommendationType, get_signal_description
from .macd_analyzer import analyze_macd_current
from .rsi_analyzer import analyze_rsi_current, get_rsi_confirmation_bonus
from .bollinger_analyzer import analyze_bollinger_current

def generate_current_recommendation(macd_entries: List[Dict[str, Any]], 
                                  rsi_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate current recommendation based on latest data"""
    if not macd_entries:
        # Return a default HOLD recommendation instead of None
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'HOLD',
            'description': get_signal_description('HOLD'),
            'confidence': 50,
            'reasoning': ['Insufficient data for analysis'],
            'technical_factors': ['No technical signals available']
        }
    
    # Get MACD analysis
    macd_analysis = analyze_macd_current(macd_entries)
    recommendation: RecommendationType = macd_analysis['recommendation']
    confidence = macd_analysis['confidence']
    reasoning = []
    technical_factors = []
    
    # Add MACD reasoning
    if macd_analysis['macd_value'] > macd_analysis['signal_value']:
        if macd_analysis['histogram'] > 0.3:
            reasoning.extend(['MACD line significantly above signal line', 'Strong positive histogram momentum'])
            technical_factors.append('Strong MACD bullish crossover')
        elif macd_analysis['histogram'] > 0.1:
            reasoning.extend(['MACD line above signal line', 'Positive histogram momentum'])
            technical_factors.append('MACD bullish crossover')
        else:
            reasoning.extend(['MACD line above signal line', 'Declining histogram momentum'])
            technical_factors.append('Weak MACD bullish signal')
    elif macd_analysis['macd_value'] < macd_analysis['signal_value']:
        if macd_analysis['histogram'] < -0.3:
            reasoning.extend(['MACD line significantly below signal line', 'Strong negative histogram momentum'])
            technical_factors.append('Strong MACD bearish crossover')
        elif macd_analysis['histogram'] < -0.1:
            reasoning.extend(['MACD line below signal line', 'Negative histogram momentum'])
            technical_factors.append('MACD bearish crossover')
        else:
            reasoning.extend(['MACD line below signal line', 'Improving histogram momentum'])
            technical_factors.append('Weak MACD bearish signal')
    else:
        reasoning.extend(['MACD line at signal line', 'Neutral momentum'])
        technical_factors.append('MACD neutral position')
    
    # RSI Confirmation
    if rsi_entries:
        latest_rsi = rsi_entries[-1]
        rsi_value = latest_rsi.get('value', 50)
        rsi_bonus = get_rsi_confirmation_bonus(rsi_value, recommendation)
        
        if rsi_bonus['confidence_boost'] > 0:
            confidence += rsi_bonus['confidence_boost']
            reasoning.append(rsi_bonus['reasoning'])
            technical_factors.append(rsi_bonus['technical_factor'])
            
            # Upgrade recommendation if RSI provides strong confirmation
            if rsi_value < 30 and recommendation == 'OUTPERFORM':
                recommendation = 'BUY'
            elif rsi_value > 70 and recommendation == 'UNDERPERFORM':
                recommendation = 'SELL'
    
    confidence = min(confidence, 95)  # Cap at 95%
    
    return {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': recommendation,
        'description': get_signal_description(recommendation),
        'confidence': confidence,
        'reasoning': reasoning,
        'technical_factors': technical_factors
    }

def analyze_technical_indicators(macd_entries: List[Dict[str, Any]], 
                               rsi_entries: List[Dict[str, Any]], 
                               bollinger_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze technical indicators and provide recommendations"""
    # Get individual analyses
    macd_analysis = analyze_macd_current(macd_entries)
    rsi_analysis = analyze_rsi_current(rsi_entries)
    bollinger_analysis = analyze_bollinger_current(bollinger_entries)
    
    return {
        'macd_recommendation': macd_analysis['recommendation'],
        'macd_analysis': macd_analysis['analysis'],
        'rsi_recommendation': rsi_analysis['recommendation'],
        'rsi_analysis': rsi_analysis['analysis'],
        'bollinger_recommendation': bollinger_analysis['recommendation'],
        'bollinger_analysis': bollinger_analysis['analysis']
    } 