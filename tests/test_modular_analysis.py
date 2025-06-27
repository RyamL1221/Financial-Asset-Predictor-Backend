import unittest
from unittest.mock import Mock, patch
from src.routes.get_stock_ticker.analysis import perform_stock_analysis

class TestModularAnalysis(unittest.TestCase):
    """Test the modular analysis structure"""
    
    def test_perform_stock_analysis_with_valid_data(self):
        """Test that perform_stock_analysis works with valid data"""
        # Mock data
        macd_values = [
            {
                'timestamp': 1640995200000,  # 2022-01-01
                'value': 0.5,
                'signal': 0.3,
                'histogram': 0.2
            },
            {
                'timestamp': 1641081600000,  # 2022-01-02
                'value': 0.6,
                'signal': 0.4,
                'histogram': 0.2
            }
        ]
        
        rsi_values = [
            {
                'timestamp': 1640995200000,
                'value': 45.0
            },
            {
                'timestamp': 1641081600000,
                'value': 50.0
            }
        ]
        
        bollinger_values = [
            {
                'timestamp': 1640995200000,
                'upper_band': 150.0,
                'middle_band': 140.0,
                'lower_band': 130.0
            }
        ]
        
        eps = {
            'current': {
                '0y': 2.5,
                '+1y': 3.0
            }
        }
        
        # Perform analysis
        result = perform_stock_analysis(
            macd_values=macd_values,
            rsi_values=rsi_values,
            bollinger_band_values=bollinger_values,
            eps=eps
        )
        
        # Verify structure
        self.assertIn('eps_analysis', result)
        self.assertIn('macd_signals', result)
        self.assertIn('current_recommendation', result)
        self.assertIn('technical_analysis', result)
        self.assertIn('recommendation_scale', result)
        
        # Verify EPS analysis
        self.assertEqual(result['eps_analysis']['current'], 2.5)
        self.assertEqual(result['eps_analysis']['growth_percentage'], 20.0)
        
        # Verify current recommendation exists
        self.assertIn('type', result['current_recommendation'])
        self.assertIn('confidence', result['current_recommendation'])
        self.assertIn('reasoning', result['current_recommendation'])
        
        # Verify technical analysis exists
        self.assertIn('macd_recommendation', result['technical_analysis'])
        self.assertIn('rsi_recommendation', result['technical_analysis'])
        self.assertIn('bollinger_recommendation', result['technical_analysis'])
    
    def test_perform_stock_analysis_with_empty_data(self):
        """Test that perform_stock_analysis handles empty data gracefully"""
        result = perform_stock_analysis(
            macd_values=[],
            rsi_values=[],
            bollinger_band_values=[],
            eps={}
        )
        
        # Should still return a valid structure
        self.assertIn('eps_analysis', result)
        self.assertIn('macd_signals', result)
        self.assertIn('current_recommendation', result)
        self.assertIn('technical_analysis', result)
        self.assertIn('recommendation_scale', result)
        
        # Should have default values
        self.assertIsNone(result['eps_analysis']['current'])
        self.assertIsNone(result['eps_analysis']['growth_percentage'])
        self.assertEqual(result['current_recommendation']['type'], 'HOLD')

if __name__ == '__main__':
    unittest.main() 