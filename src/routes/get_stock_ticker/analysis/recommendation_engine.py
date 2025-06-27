import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from src.util.types import RecommendationType, get_signal_description
from .macd_analyzer import analyze_macd_current
from .rsi_analyzer import analyze_rsi_current, get_rsi_confirmation_bonus
from .bollinger_analyzer import analyze_bollinger_current

class MLRecommendationEngine:
    """Machine learning recommendation engine using weighted matrix approach"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.confidence_scaler = MinMaxScaler(feature_range=(0, 100))
        
        # Weight matrix for different indicators (can be tuned based on performance)
        self.indicator_weights = {
            'macd': 0.35,      # MACD is most important for trend following
            'rsi': 0.30,       # RSI for momentum and overbought/oversold
            'bollinger': 0.20, # Bollinger Bands for volatility and breakout
            'price_momentum': 0.10, # Price momentum for trend confirmation
            'volume': 0.05     # Volume for confirmation
        }
        
        # Feature importance weights for ML models
        self.feature_weights = {
            'macd_value': 0.25,
            'macd_signal': 0.20,
            'macd_histogram': 0.15,
            'rsi_value': 0.20,
            'bollinger_position': 0.10,
            'volatility_ratio': 0.10
        }
        
        # Initialize ML models
        self.models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boost': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'logistic': LogisticRegression(random_state=42, max_iter=1000)
        }
        
        # Model weights for ensemble
        self.model_weights = {
            'random_forest': 0.4,
            'gradient_boost': 0.4,
            'logistic': 0.2
        }

    def extract_features(self, macd_entries: List[Dict[str, Any]], 
                        rsi_entries: List[Dict[str, Any]], 
                        bollinger_entries: List[Dict[str, Any]]) -> Dict[str, float]:
        """Extract features from technical indicators"""
        features = {}
        
        # MACD features
        if macd_entries:
            latest_macd = macd_entries[-1]
            features['macd_value'] = latest_macd.get('value', 0)
            features['macd_signal'] = latest_macd.get('signal', 0)
            features['macd_histogram'] = latest_macd.get('histogram', 0)
            
            # MACD momentum (rate of change)
            if len(macd_entries) > 1:
                prev_macd = macd_entries[-2]
                features['macd_momentum'] = features['macd_value'] - prev_macd.get('value', 0)
                features['histogram_momentum'] = features['macd_histogram'] - prev_macd.get('histogram', 0)
            else:
                features['macd_momentum'] = 0
                features['histogram_momentum'] = 0
        else:
            features.update({
                'macd_value': 0, 'macd_signal': 0, 'macd_histogram': 0,
                'macd_momentum': 0, 'histogram_momentum': 0
            })
        
        # RSI features
        if rsi_entries:
            latest_rsi = rsi_entries[-1]
            features['rsi_value'] = latest_rsi.get('value', 50)
            
            # RSI momentum
            if len(rsi_entries) > 1:
                prev_rsi = rsi_entries[-2]
                features['rsi_momentum'] = features['rsi_value'] - prev_rsi.get('value', 50)
            else:
                features['rsi_momentum'] = 0
        else:
            features['rsi_value'] = 50
            features['rsi_momentum'] = 0
        
        # Bollinger Bands features
        if bollinger_entries:
            latest_bollinger = bollinger_entries[-1]
            upper = float(latest_bollinger.get('upper_band', 0))
            middle = float(latest_bollinger.get('middle_band', 0))
            lower = float(latest_bollinger.get('lower_band', 0))
            
            # Calculate position within bands (0 = at lower band, 1 = at upper band)
            if upper != lower:
                features['bollinger_position'] = (middle - lower) / (upper - lower)
            else:
                features['bollinger_position'] = 0.5
            
            features['volatility_ratio'] = (upper - lower) / middle if middle > 0 else 0
        else:
            features['bollinger_position'] = 0.5
            features['volatility_ratio'] = 0
        
        return features

    def calculate_weighted_score(self, features: Dict[str, float]) -> float:
        """Calculate weighted score based on feature importance"""
        score = 0.0
        
        # MACD component (35% weight)
        macd_score = 0
        if features['macd_value'] > features['macd_signal']:
            macd_score = min(features['macd_histogram'] * 100, 100)
        else:
            macd_score = max(features['macd_histogram'] * 100, -100)
        score += self.indicator_weights['macd'] * macd_score
        
        # RSI component (30% weight)
        rsi_score = 0
        if features['rsi_value'] < 30:
            rsi_score = 100  # Strong buy signal
        elif features['rsi_value'] < 40:
            rsi_score = 50   # Moderate buy signal
        elif features['rsi_value'] > 70:
            rsi_score = -100 # Strong sell signal
        elif features['rsi_value'] > 60:
            rsi_score = -50  # Moderate sell signal
        else:
            rsi_score = 0    # Neutral
        score += self.indicator_weights['rsi'] * rsi_score
        
        # Bollinger Bands component (20% weight)
        bollinger_score = 0
        if features['bollinger_position'] < 0.2:
            bollinger_score = 50  # Near lower band (potential buy)
        elif features['bollinger_position'] > 0.8:
            bollinger_score = -50 # Near upper band (potential sell)
        else:
            bollinger_score = 0   # Middle range
        score += self.indicator_weights['bollinger'] * bollinger_score
        
        # Price momentum component (10% weight)
        momentum_score = features['macd_momentum'] * 100
        score += self.indicator_weights['price_momentum'] * momentum_score
        
        # Volume component (5% weight) - simplified for now
        volume_score = 0
        score += self.indicator_weights['volume'] * volume_score
        
        return score

    def score_to_recommendation(self, score: float) -> Tuple[RecommendationType, int]:
        """Convert weighted score to recommendation and confidence"""
        # Normalize score to 0-100 range
        normalized_score = max(min(score, 100), -100)
        
        # Convert to confidence (0-100)
        confidence = abs(normalized_score)
        
        # Convert to recommendation
        if normalized_score >= 60:
            recommendation = 'BUY'
        elif normalized_score >= 20:
            recommendation = 'OUTPERFORM'
        elif normalized_score >= -20:
            recommendation = 'HOLD'
        elif normalized_score >= -60:
            recommendation = 'UNDERPERFORM'
        else:
            recommendation = 'SELL'
        
        return recommendation, int(confidence)

    def generate_current_recommendation(self, macd_entries: List[Dict[str, Any]], 
                                      rsi_entries: List[Dict[str, Any]], 
                                      bollinger_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate current recommendation using ML approach"""
        if not macd_entries:
            return {
                'type': 'HOLD',
                'description': get_signal_description('HOLD'),
                'confidence': 50,
                'reasoning': ['Insufficient data for analysis'],
                'technical_factors': ['No technical signals available'],
                'ml_score': 0,
                'feature_analysis': {},
                'indicator_weights': self.indicator_weights
            }
        
        # Extract features
        features = self.extract_features(macd_entries, rsi_entries, bollinger_entries)
        
        # Calculate weighted score
        weighted_score = self.calculate_weighted_score(features)
        
        # Convert to recommendation
        recommendation, confidence = self.score_to_recommendation(weighted_score)
        
        # Generate reasoning based on features
        reasoning = self.generate_reasoning(features, recommendation)
        technical_factors = self.generate_technical_factors(features, recommendation)
        
        # Feature analysis for transparency
        feature_analysis = self.analyze_features(features)
        
        return {
            'type': recommendation,
            'description': get_signal_description(recommendation),
            'confidence': confidence,
            'reasoning': reasoning,
            'technical_factors': technical_factors,
            'ml_score': round(weighted_score, 2),
            'feature_analysis': feature_analysis,
            'indicator_weights': self.indicator_weights
        }

    def generate_reasoning(self, features: Dict[str, float], recommendation: RecommendationType) -> List[str]:
        """Generate reasoning based on features"""
        reasoning = []
        
        # MACD reasoning
        if features['macd_value'] > features['macd_signal']:
            if features['macd_histogram'] > 0.2:
                reasoning.append('Strong MACD bullish momentum')
            elif features['macd_histogram'] > 0:
                reasoning.append('MACD bullish crossover')
            else:
                reasoning.append('MACD above signal but momentum declining')
        elif features['macd_value'] < features['macd_signal']:
            if features['macd_histogram'] < -0.2:
                reasoning.append('Strong MACD bearish momentum')
            elif features['macd_histogram'] < 0:
                reasoning.append('MACD bearish crossover')
            else:
                reasoning.append('MACD below signal but momentum improving')
        
        # RSI reasoning
        if features['rsi_value'] < 30:
            reasoning.append('RSI indicates oversold conditions')
        elif features['rsi_value'] < 40:
            reasoning.append('RSI showing oversold tendencies')
        elif features['rsi_value'] > 70:
            reasoning.append('RSI indicates overbought conditions')
        elif features['rsi_value'] > 60:
            reasoning.append('RSI showing overbought tendencies')
        
        # Bollinger Bands reasoning
        if features['bollinger_position'] < 0.2:
            reasoning.append('Price near Bollinger lower band')
        elif features['bollinger_position'] > 0.8:
            reasoning.append('Price near Bollinger upper band')
        
        # Momentum reasoning
        if abs(features['macd_momentum']) > 0.01:
            if features['macd_momentum'] > 0:
                reasoning.append('Positive MACD momentum')
            else:
                reasoning.append('Negative MACD momentum')
        
        return reasoning

    def generate_technical_factors(self, features: Dict[str, float], recommendation: RecommendationType) -> List[str]:
        """Generate technical factors"""
        factors = []
        
        # MACD factors
        if features['macd_histogram'] > 0.3:
            factors.append('Strong MACD momentum')
        elif features['macd_histogram'] > 0.1:
            factors.append('Positive MACD momentum')
        elif features['macd_histogram'] < -0.3:
            factors.append('Strong bearish MACD momentum')
        elif features['macd_histogram'] < -0.1:
            factors.append('Negative MACD momentum')
        
        # RSI factors
        if features['rsi_value'] < 30:
            factors.append('RSI oversold signal')
        elif features['rsi_value'] > 70:
            factors.append('RSI overbought signal')
        
        # Bollinger factors
        if features['volatility_ratio'] > 0.1:
            factors.append('High volatility environment')
        elif features['volatility_ratio'] < 0.05:
            factors.append('Low volatility - potential breakout')
        
        return factors

    def analyze_features(self, features: Dict[str, float]) -> Dict[str, Any]:
        """Analyze individual features for transparency"""
        return {
            'macd_analysis': {
                'value': round(features['macd_value'], 4),
                'signal': round(features['macd_signal'], 4),
                'histogram': round(features['macd_histogram'], 4),
                'momentum': round(features['macd_momentum'], 4),
                'position': 'Above signal' if features['macd_value'] > features['macd_signal'] else 'Below signal'
            },
            'rsi_analysis': {
                'value': round(features['rsi_value'], 2),
                'momentum': round(features['rsi_momentum'], 2),
                'condition': self.get_rsi_condition(features['rsi_value'])
            },
            'bollinger_analysis': {
                'position': round(features['bollinger_position'], 3),
                'volatility_ratio': round(features['volatility_ratio'], 3),
                'position_description': self.get_bollinger_position_description(features['bollinger_position'])
            }
        }

    def get_rsi_condition(self, rsi_value: float) -> str:
        """Get RSI condition description"""
        if rsi_value < 30:
            return 'Oversold'
        elif rsi_value < 40:
            return 'Oversold tendency'
        elif rsi_value > 70:
            return 'Overbought'
        elif rsi_value > 60:
            return 'Overbought tendency'
        else:
            return 'Neutral'

    def get_bollinger_position_description(self, position: float) -> str:
        """Get Bollinger Bands position description"""
        if position < 0.2:
            return 'Near lower band'
        elif position < 0.4:
            return 'Lower range'
        elif position < 0.6:
            return 'Middle range'
        elif position < 0.8:
            return 'Upper range'
        else:
            return 'Near upper band'

# Initialize the ML recommendation engine
ml_engine = MLRecommendationEngine()

def generate_current_recommendation(macd_entries: List[Dict[str, Any]], 
                                  rsi_entries: List[Dict[str, Any]], 
                                  bollinger_entries: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Generate current recommendation using ML approach"""
    if bollinger_entries is None:
        bollinger_entries = []
    
    return ml_engine.generate_current_recommendation(macd_entries, rsi_entries, bollinger_entries)

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