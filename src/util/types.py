from typing import List, Dict, Any, Optional, Literal

# Type definitions for stock analysis
RecommendationType = Literal['BUY', 'SELL', 'HOLD', 'UNDERPERFORM', 'OUTPERFORM']

class RecommendationScale:
    def __init__(self, type: RecommendationType, name: str, alias: str, description: str, 
                 expected_return: str, risk_level: str, time_horizon: str, 
                 color: str, background_color: str):
        self.type = type
        self.name = name
        self.alias = alias
        self.description = description
        self.expected_return = expected_return
        self.risk_level = risk_level
        self.time_horizon = time_horizon
        self.color = color
        self.background_color = background_color

# Recommendation scale definition
RECOMMENDATION_SCALE = [
    RecommendationScale(
        'BUY', 'Buy', 'Strong Buy / On the Recommended List',
        'A recommendation to purchase a specific security. Also known as strong buy and "on the recommended list."',
        '15%+ above market', 'Low to Medium', '3-12 months',
        '#22543d', '#c6f6d5'
    ),
    RecommendationScale(
        'OUTPERFORM', 'Outperform', 'Moderate Buy / Accumulate / Overweight',
        'A stock is expected to do slightly better than the market return. Also known as "moderate buy," "accumulate," and "overweight."',
        '5-15% above market', 'Medium', '3-6 months',
        '#38a169', '#9ae6b4'
    ),
    RecommendationScale(
        'HOLD', 'Hold', 'Neutral / Market-perform',
        'A company with a hold recommendation is expected to perform at the same pace as comparable companies or in line with the market.',
        'Market performance', 'Medium', '1-6 months',
        '#4a5568', '#f7fafc'
    ),
    RecommendationScale(
        'UNDERPERFORM', 'Underperform', 'Moderate Sell / Weak Hold / Underweight',
        'A stock is expected to do slightly worse than the overall stock market return. Also known as "moderate sell," "weak hold," and "underweight."',
        '5-15% below market', 'Medium', '1-6 months',
        '#ed8936', '#fffaf0'
    ),
    RecommendationScale(
        'SELL', 'Sell', 'Strong Sell',
        'A recommendation to sell a security or to liquidate an asset. Also known as strong sell.',
        '15%+ below market', 'Medium to High', '1-3 months',
        '#e53e3e', '#fed7d7'
    )
]

def get_recommendation_scale(type: RecommendationType) -> Optional[RecommendationScale]:
    """Get recommendation scale by type"""
    for scale in RECOMMENDATION_SCALE:
        if scale.type == type:
            return scale
    return None

def get_signal_description(type: RecommendationType) -> str:
    """Get signal description by type"""
    scale = get_recommendation_scale(type)
    return scale.description if scale else 'Neutral position' 