from typing import List, Dict, Any
from .macd_analyzer import analyze_macd_signals
from .recommendation_engine import generate_current_recommendation, analyze_technical_indicators
from src.util.types import RECOMMENDATION_SCALE

def perform_stock_analysis(macd_values: List[Dict[str, Any]], 
                          rsi_values: List[Dict[str, Any]], 
                          bollinger_band_values: List[Dict[str, Any]],
                          eps: Dict[str, Any]) -> Dict[str, Any]:
    """Perform comprehensive stock analysis and return analysis results"""
    
    # Reverse entries to chronological order (past → future)
    macd_entries = list(reversed(macd_values)) if macd_values else []
    rsi_entries = list(reversed(rsi_values)) if rsi_values else []
    bollinger_entries = list(reversed(bollinger_band_values)) if bollinger_band_values else []
    
    # Perform analysis
    macd_signals = analyze_macd_signals(macd_entries)
    current_recommendation = generate_current_recommendation(macd_entries, rsi_entries)
    technical_analysis = analyze_technical_indicators(macd_entries, rsi_entries, bollinger_entries)
    
    # Calculate EPS metrics
    current_eps = None
    eps_growth = None
    if eps and eps.get('current'):
        current_eps = eps['current'].get('0y')
        next_year_eps = eps['current'].get('+1y')
        if current_eps and next_year_eps and current_eps != 0:
            eps_growth = ((next_year_eps - current_eps) / current_eps) * 100
    
    # Prepare analysis response
    analysis_response = {
        "eps_analysis": {
            "current": current_eps,
            "growth_percentage": eps_growth
        },
        "macd_signals": macd_signals,
        "current_recommendation": current_recommendation,
        "technical_analysis": technical_analysis,
        "recommendation_scale": [
            {
                'type': scale.type,
                'name': scale.name,
                'alias': scale.alias,
                'description': scale.description,
                'expected_return': scale.expected_return,
                'risk_level': scale.risk_level,
                'time_horizon': scale.time_horizon,
                'color': scale.color,
                'background_color': scale.background_color
            } for scale in RECOMMENDATION_SCALE
        ]
    }
    
    return analysis_response 