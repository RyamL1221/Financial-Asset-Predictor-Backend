import pytest
from datetime import datetime
from src.routes.get_stock_ticker.analysis.recommendation_engine import generate_current_recommendation, MLRecommendationEngine

def test_ml_recommendation_engine_initialization():
    """Test that the ML recommendation engine initializes correctly"""
    engine = MLRecommendationEngine()
    
    # Check that indicator weights are set
    assert 'macd' in engine.indicator_weights
    assert 'rsi' in engine.indicator_weights
    assert 'bollinger' in engine.indicator_weights
    
    # Check that weights sum to approximately 1.0
    total_weight = sum(engine.indicator_weights.values())
    assert abs(total_weight - 1.0) < 0.01

def test_extract_features():
    """Test feature extraction from technical indicators"""
    engine = MLRecommendationEngine()
    
    # Sample data
    macd_entries = [
        {'value': 0.5, 'signal': 0.3, 'histogram': 0.2, 'timestamp': 1640995200000},
        {'value': 0.4, 'signal': 0.35, 'histogram': 0.05, 'timestamp': 1641081600000}
    ]
    
    rsi_entries = [
        {'value': 45, 'timestamp': 1640995200000},
        {'value': 50, 'timestamp': 1641081600000}
    ]
    
    bollinger_entries = [
        {'upper_band': 150, 'middle_band': 140, 'lower_band': 130, 'timestamp': 1640995200000},
        {'upper_band': 155, 'middle_band': 145, 'lower_band': 135, 'timestamp': 1641081600000}
    ]
    
    features = engine.extract_features(macd_entries, rsi_entries, bollinger_entries)
    
    # Check that all expected features are present
    expected_features = [
        'macd_value', 'macd_signal', 'macd_histogram', 'macd_momentum', 'histogram_momentum',
        'rsi_value', 'rsi_momentum', 'bollinger_position', 'volatility_ratio'
    ]
    
    for feature in expected_features:
        assert feature in features
    
    # Check specific values
    assert features['macd_value'] == 0.4
    assert features['macd_signal'] == 0.35
    assert features['macd_histogram'] == 0.05
    assert features['rsi_value'] == 50
    assert features['bollinger_position'] == 0.5  # (145-135)/(155-135) = 0.5

def test_calculate_weighted_score():
    """Test weighted score calculation"""
    engine = MLRecommendationEngine()
    
    # Test bullish scenario
    bullish_features = {
        'macd_value': 0.5,
        'macd_signal': 0.3,
        'macd_histogram': 0.2,
        'macd_momentum': 0.1,
        'histogram_momentum': 0.05,
        'rsi_value': 35,  # Oversold tendency
        'rsi_momentum': 5,
        'bollinger_position': 0.1,  # Near lower band
        'volatility_ratio': 0.05
    }
    
    bullish_score = engine.calculate_weighted_score(bullish_features)
    assert bullish_score > 0  # Should be positive for bullish scenario
    
    # Test bearish scenario
    bearish_features = {
        'macd_value': 0.3,
        'macd_signal': 0.5,
        'macd_histogram': -0.2,
        'macd_momentum': -0.1,
        'histogram_momentum': -0.05,
        'rsi_value': 75,  # Overbought tendency
        'rsi_momentum': -5,
        'bollinger_position': 0.9,  # Near upper band
        'volatility_ratio': 0.05
    }
    
    bearish_score = engine.calculate_weighted_score(bearish_features)
    assert bearish_score < 0  # Should be negative for bearish scenario

def test_score_to_recommendation():
    """Test conversion from score to recommendation"""
    engine = MLRecommendationEngine()
    
    # Test BUY recommendation
    recommendation, confidence = engine.score_to_recommendation(70)
    assert recommendation == 'BUY'
    assert confidence == 70
    
    # Test SELL recommendation
    recommendation, confidence = engine.score_to_recommendation(-70)
    assert recommendation == 'SELL'
    assert confidence == 70
    
    # Test HOLD recommendation
    recommendation, confidence = engine.score_to_recommendation(10)
    assert recommendation == 'HOLD'
    assert confidence == 10

def test_generate_current_recommendation():
    """Test the main recommendation generation function"""
    # Sample data for bullish scenario
    macd_entries = [
        {'value': 0.5, 'signal': 0.3, 'histogram': 0.2, 'timestamp': 1640995200000},
        {'value': 0.4, 'signal': 0.35, 'histogram': 0.05, 'timestamp': 1641081600000}
    ]
    
    rsi_entries = [
        {'value': 35, 'timestamp': 1640995200000},
        {'value': 40, 'timestamp': 1641081600000}
    ]
    
    bollinger_entries = [
        {'upper_band': 150, 'middle_band': 140, 'lower_band': 130, 'timestamp': 1640995200000},
        {'upper_band': 155, 'middle_band': 145, 'lower_band': 135, 'timestamp': 1641081600000}
    ]
    
    recommendation = generate_current_recommendation(macd_entries, rsi_entries, bollinger_entries)
    
    # Check structure
    assert 'date' in recommendation
    assert 'type' in recommendation
    assert 'description' in recommendation
    assert 'confidence' in recommendation
    assert 'reasoning' in recommendation
    assert 'technical_factors' in recommendation
    assert 'ml_score' in recommendation
    assert 'feature_analysis' in recommendation
    assert 'indicator_weights' in recommendation
    
    # Check that date is today
    today = datetime.now().strftime('%Y-%m-%d')
    assert recommendation['date'] == today
    
    # Check that confidence is between 0 and 100
    assert 0 <= recommendation['confidence'] <= 100
    
    # Check that ml_score is a number
    assert isinstance(recommendation['ml_score'], (int, float))
    
    # Check that feature analysis contains expected sections
    feature_analysis = recommendation['feature_analysis']
    assert 'macd_analysis' in feature_analysis
    assert 'rsi_analysis' in feature_analysis
    assert 'bollinger_analysis' in feature_analysis

def test_empty_data_handling():
    """Test handling of empty data"""
    recommendation = generate_current_recommendation([], [], [])
    
    assert recommendation['type'] == 'HOLD'
    assert recommendation['confidence'] == 50
    assert 'Insufficient data for analysis' in recommendation['reasoning']
    assert recommendation['ml_score'] == 0

def test_feature_analysis_structure():
    """Test that feature analysis provides detailed breakdown"""
    engine = MLRecommendationEngine()
    
    macd_entries = [
        {'value': 0.5, 'signal': 0.3, 'histogram': 0.2, 'timestamp': 1640995200000}
    ]
    
    rsi_entries = [
        {'value': 35, 'timestamp': 1640995200000}
    ]
    
    bollinger_entries = [
        {'upper_band': 150, 'middle_band': 140, 'lower_band': 130, 'timestamp': 1640995200000}
    ]
    
    features = engine.extract_features(macd_entries, rsi_entries, bollinger_entries)
    feature_analysis = engine.analyze_features(features)
    
    # Check MACD analysis
    macd_analysis = feature_analysis['macd_analysis']
    assert 'value' in macd_analysis
    assert 'signal' in macd_analysis
    assert 'histogram' in macd_analysis
    assert 'momentum' in macd_analysis
    assert 'position' in macd_analysis
    
    # Check RSI analysis
    rsi_analysis = feature_analysis['rsi_analysis']
    assert 'value' in rsi_analysis
    assert 'momentum' in rsi_analysis
    assert 'condition' in rsi_analysis
    
    # Check Bollinger analysis
    bollinger_analysis = feature_analysis['bollinger_analysis']
    assert 'position' in bollinger_analysis
    assert 'volatility_ratio' in bollinger_analysis
    assert 'position_description' in bollinger_analysis 