from typing import List, Dict, Any, Literal
from datetime import datetime
from src.util.types import RecommendationType, get_signal_description

def determine_buy_signal_strength(current: Dict[str, Any], previous: Dict[str, Any]) -> RecommendationType:
    """Determine buy signal strength based on MACD data"""
    histogram = current.get('histogram', 0)
    histogram_change = histogram - previous.get('histogram', 0)
    
    if histogram > 0.3 and histogram_change > 0.1:
        return 'BUY'
    elif histogram > 0.1:
        return 'OUTPERFORM'
    else:
        return 'OUTPERFORM'

def determine_sell_signal_strength(current: Dict[str, Any], previous: Dict[str, Any]) -> RecommendationType:
    """Determine sell signal strength based on MACD data"""
    histogram = current.get('histogram', 0)
    histogram_change = histogram - previous.get('histogram', 0)
    
    if histogram < -0.3 and histogram_change < -0.1:
        return 'SELL'
    elif histogram < -0.1:
        return 'UNDERPERFORM'
    else:
        return 'UNDERPERFORM'

def calculate_confidence(entry: Dict[str, Any], signal_type: Literal['BUY', 'SELL']) -> int:
    """Calculate confidence level for a signal"""
    abs_histogram = abs(entry.get('histogram', 0))
    base_confidence = min(abs_histogram * 100, 80)
    
    if signal_type == 'BUY' and entry.get('histogram', 0) > 0.2:
        return min(base_confidence + 15, 95)
    elif signal_type == 'SELL' and entry.get('histogram', 0) < -0.2:
        return min(base_confidence + 15, 95)
    
    return max(base_confidence, 50)

def generate_reasoning(entry: Dict[str, Any], signal_type: Literal['BUY', 'SELL']) -> List[str]:
    """Generate reasoning for a signal"""
    reasoning = []
    
    if signal_type == 'BUY':
        reasoning.append('MACD line crossed above signal line')
        histogram = entry.get('histogram', 0)
        if histogram > 0.2:
            reasoning.append('Strong positive histogram momentum')
        elif histogram > 0:
            reasoning.append('Positive histogram momentum')
        else:
            reasoning.append('Declining histogram momentum')
    else:
        reasoning.append('MACD line crossed below signal line')
        histogram = entry.get('histogram', 0)
        if histogram < -0.2:
            reasoning.append('Strong negative histogram momentum')
        elif histogram < 0:
            reasoning.append('Negative histogram momentum')
        else:
            reasoning.append('Improving histogram momentum')
    
    return reasoning

def get_technical_factors(entry: Dict[str, Any], signal_type: Literal['BUY', 'SELL']) -> List[str]:
    """Get technical factors for a signal"""
    factors = []
    
    if signal_type == 'BUY':
        histogram = entry.get('histogram', 0)
        if histogram > 0.3:
            factors.extend(['Strong MACD momentum', 'Bullish histogram pattern'])
        elif histogram > 0.1:
            factors.extend(['Positive MACD momentum', 'Bullish signal line crossover'])
        else:
            factors.extend(['Weak MACD momentum', 'Cautious bullish signal'])
    else:
        histogram = entry.get('histogram', 0)
        if histogram < -0.3:
            factors.extend(['Strong bearish momentum', 'Bearish histogram pattern'])
        elif histogram < -0.1:
            factors.extend(['Negative MACD momentum', 'Bearish signal line crossover'])
        else:
            factors.extend(['Weak bearish momentum', 'Cautious bearish signal'])
    
    return factors

def analyze_macd_signals(macd_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analyze MACD signals and generate recommendations"""
    signals = []
    
    for i in range(1, len(macd_entries)):
        current = macd_entries[i]
        previous = macd_entries[i - 1]
        
        # Check for MACD line crossing above signal line (BUY signals)
        if (previous.get('value', 0) <= previous.get('signal', 0) and 
            current.get('value', 0) > current.get('signal', 0)):
            
            signal_type = determine_buy_signal_strength(current, previous)
            confidence = calculate_confidence(current, 'BUY')
            reasoning = generate_reasoning(current, 'BUY')
            technical_factors = get_technical_factors(current, 'BUY')
            
            signals.append({
                'type': signal_type,
                'description': get_signal_description(signal_type),
                'confidence': confidence,
                'reasoning': reasoning,
                'technical_factors': technical_factors
            })
        
        # Check for MACD line crossing below signal line (SELL signals)
        if (previous.get('value', 0) >= previous.get('signal', 0) and 
            current.get('value', 0) < current.get('signal', 0)):
            
            signal_type = determine_sell_signal_strength(current, previous)
            confidence = calculate_confidence(current, 'SELL')
            reasoning = generate_reasoning(current, 'SELL')
            technical_factors = get_technical_factors(current, 'SELL')
            
            signals.append({
                'type': signal_type,
                'description': get_signal_description(signal_type),
                'confidence': confidence,
                'reasoning': reasoning,
                'technical_factors': technical_factors
            })
    
    # Keep only the most recent signals (last 5)
    return signals[-5:] if len(signals) > 5 else signals

def analyze_macd_current(macd_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze current MACD position and provide recommendation"""
    if not macd_entries:
        return {
            'recommendation': 'HOLD',
            'analysis': 'No MACD data available',
            'confidence': 50
        }
    
    latest_macd = macd_entries[-1]
    macd_value = latest_macd.get('value', 0)
    signal_value = latest_macd.get('signal', 0)
    histogram = latest_macd.get('histogram', 0)
    
    if macd_value > signal_value:
        # MACD is above signal line (bullish)
        if histogram > 0.3:
            recommendation = 'BUY'
            confidence = 85
            analysis = f"MACD line at {macd_value:.4f} is significantly above signal line at {signal_value:.4f} with strong positive histogram momentum ({histogram:.4f}). This indicates strong bullish momentum."
        elif histogram > 0.1:
            recommendation = 'OUTPERFORM'
            confidence = 70
            analysis = f"MACD line at {macd_value:.4f} is above signal line at {signal_value:.4f} with positive histogram momentum ({histogram:.4f}). This indicates bullish momentum."
        else:
            recommendation = 'OUTPERFORM'
            confidence = 60
            analysis = f"MACD line at {macd_value:.4f} is above signal line at {signal_value:.4f} but with declining histogram momentum ({histogram:.4f}). This indicates weak bullish momentum."
    elif macd_value < signal_value:
        # MACD is below signal line (bearish)
        if histogram < -0.3:
            recommendation = 'SELL'
            confidence = 85
            analysis = f"MACD line at {macd_value:.4f} is significantly below signal line at {signal_value:.4f} with strong negative histogram momentum ({histogram:.4f}). This indicates strong bearish momentum."
        elif histogram < -0.1:
            recommendation = 'UNDERPERFORM'
            confidence = 70
            analysis = f"MACD line at {macd_value:.4f} is below signal line at {signal_value:.4f} with negative histogram momentum ({histogram:.4f}). This indicates bearish momentum."
        else:
            recommendation = 'UNDERPERFORM'
            confidence = 60
            analysis = f"MACD line at {macd_value:.4f} is below signal line at {signal_value:.4f} but with improving histogram momentum ({histogram:.4f}). This indicates weak bearish momentum."
    else:
        # MACD equals signal line
        recommendation = 'HOLD'
        confidence = 50
        analysis = f"MACD line at {macd_value:.4f} is at signal line at {signal_value:.4f} with neutral histogram ({histogram:.4f}). This indicates neutral momentum."
    
    return {
        'recommendation': recommendation,
        'analysis': analysis,
        'confidence': confidence,
        'macd_value': macd_value,
        'signal_value': signal_value,
        'histogram': histogram
    } 