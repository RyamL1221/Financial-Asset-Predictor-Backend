from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, mean_squared_error
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

from src.util.types import RecommendationType

class BollingerMLAnalyzer:
    """Machine Learning enhanced Bollinger Bands analyzer"""
    
    def __init__(self):
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.regressor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.cluster_model = KMeans(n_clusters=5, random_state=42)
        self.is_trained = False
        
    def _extract_features(self, bollinger_entries: List[Dict[str, Any]]) -> pd.DataFrame:
        """Extract comprehensive features from Bollinger Bands data"""
        if len(bollinger_entries) < 20:
            return pd.DataFrame()
            
        df = pd.DataFrame(bollinger_entries)
        df['upper_band'] = pd.to_numeric(df['upper_band'], errors='coerce')
        df['middle_band'] = pd.to_numeric(df['middle_band'], errors='coerce')
        df['lower_band'] = pd.to_numeric(df['lower_band'], errors='coerce')
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        
        # Basic Bollinger Band features
        df['band_width'] = df['upper_band'] - df['lower_band']
        df['band_position'] = (df['close'] - df['lower_band']) / (df['upper_band'] - df['lower_band'])
        df['bb_percent'] = (df['close'] - df['lower_band']) / (df['upper_band'] - df['lower_band']) * 100
        
        # Volatility features
        df['volatility'] = df['band_width'] / df['middle_band']
        df['volatility_ma'] = df['volatility'].rolling(window=10).mean()
        df['volatility_std'] = df['volatility'].rolling(window=10).std()
        
        # Price momentum features
        df['price_change'] = df['close'].pct_change()
        df['price_momentum'] = df['price_change'].rolling(window=5).mean()
        df['price_acceleration'] = df['price_momentum'].diff()
        
        # Bollinger Band squeeze and expansion
        df['squeeze'] = df['band_width'].rolling(window=20).mean() / df['band_width']
        df['expansion'] = df['band_width'] / df['band_width'].rolling(window=20).mean()
        
        # Cross-over signals
        df['upper_cross'] = (df['close'] > df['upper_band']).astype(int)
        df['lower_cross'] = (df['close'] < df['lower_band']).astype(int)
        df['middle_cross'] = (df['close'] > df['middle_band']).astype(int)
        
        # Trend features
        df['upper_trend'] = df['upper_band'].rolling(window=10).apply(lambda x: 1 if x.iloc[-1] > x.iloc[0] else -1)
        df['lower_trend'] = df['lower_band'].rolling(window=10).apply(lambda x: 1 if x.iloc[-1] > x.iloc[0] else -1)
        df['middle_trend'] = df['middle_band'].rolling(window=10).apply(lambda x: 1 if x.iloc[-1] > x.iloc[0] else -1)
        
        # Remove NaN values
        df = df.dropna()
        
        return df
    
    def _create_labels(self, df: pd.DataFrame, lookforward: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """Create classification and regression labels"""
        # Classification labels based on future price movement
        future_returns = df['close'].shift(-lookforward) / df['close'] - 1
        
        # Classification: 0=Strong Sell, 1=Sell, 2=Hold, 3=Buy, 4=Strong Buy
        classification_labels = np.zeros(len(df))
        classification_labels[future_returns > 0.05] = 4  # Strong Buy (>5% gain)
        classification_labels[(future_returns > 0.02) & (future_returns <= 0.05)] = 3  # Buy (2-5% gain)
        classification_labels[(future_returns >= -0.02) & (future_returns <= 0.02)] = 2  # Hold (-2% to 2%)
        classification_labels[(future_returns >= -0.05) & (future_returns < -0.02)] = 1  # Sell (-5% to -2%)
        classification_labels[future_returns < -0.05] = 0  # Strong Sell (<-5% loss)
        
        # Remove rows where we don't have future data
        valid_indices = ~np.isnan(future_returns)
        
        return classification_labels[valid_indices], future_returns[valid_indices]
    
    def train_models(self, bollinger_entries: List[Dict[str, Any]]) -> bool:
        """Train ML models on historical Bollinger Bands data"""
        try:
            df = self._extract_features(bollinger_entries)
            if len(df) < 50:
                return False
                
            # Create labels
            classification_labels, regression_labels = self._create_labels(df)
            
            # Prepare features (exclude target variables and non-feature columns)
            feature_columns = ['band_width', 'band_position', 'bb_percent', 'volatility', 
                             'volatility_ma', 'volatility_std', 'price_change', 'price_momentum',
                             'price_acceleration', 'squeeze', 'expansion', 'upper_cross', 
                             'lower_cross', 'middle_cross', 'upper_trend', 'lower_trend', 'middle_trend']
            
            X = df[feature_columns].values
            y_class = classification_labels
            y_reg = regression_labels
            
            # Remove rows with NaN in labels
            valid_mask = ~(np.isnan(y_class) | np.isnan(y_reg))
            X = X[valid_mask]
            y_class = y_class[valid_mask]
            y_reg = y_reg[valid_mask]
            
            if len(X) < 30:
                return False
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train models
            self.classifier.fit(X_scaled, y_class.astype(int))
            self.regressor.fit(X_scaled, y_reg)
            self.anomaly_detector.fit(X_scaled)
            self.cluster_model.fit(X_scaled)
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Error training models: {e}")
            return False
    
    def predict_signal(self, bollinger_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict trading signal using trained ML models"""
        if not self.is_trained or len(bollinger_entries) < 20:
            return self._fallback_analysis(bollinger_entries)
        
        try:
            df = self._extract_features(bollinger_entries)
            if len(df) == 0:
                return self._fallback_analysis(bollinger_entries)
            
            # Get latest features
            feature_columns = ['band_width', 'band_position', 'bb_percent', 'volatility', 
                             'volatility_ma', 'volatility_std', 'price_change', 'price_momentum',
                             'price_acceleration', 'squeeze', 'expansion', 'upper_cross', 
                             'lower_cross', 'middle_cross', 'upper_trend', 'lower_trend', 'middle_trend']
            
            latest_features = df[feature_columns].iloc[-1:].values
            latest_features_scaled = self.scaler.transform(latest_features)
            
            # Get predictions
            classification_pred = self.classifier.predict(latest_features_scaled)[0]
            regression_pred = self.regressor.predict(latest_features_scaled)[0]
            anomaly_score = self.anomaly_detector.decision_function(latest_features_scaled)[0]
            cluster_pred = self.cluster_model.predict(latest_features_scaled)[0]
            
            # Convert classification to recommendation
            recommendation_map = {
                0: 'SELL',      # Strong Sell
                1: 'UNDERPERFORM',  # Sell
                2: 'HOLD',      # Hold
                3: 'OUTPERFORM',    # Buy
                4: 'BUY'        # Strong Buy
            }
            
            recommendation = recommendation_map.get(int(classification_pred), 'HOLD')
            
            # Calculate confidence based on model agreement and anomaly detection
            confidence = self._calculate_confidence(classification_pred, regression_pred, 
                                                  anomaly_score, cluster_pred, df)
            
            # Generate analysis text
            analysis = self._generate_analysis_text(recommendation, classification_pred, 
                                                  regression_pred, anomaly_score, df)
            
            return {
                'recommendation': recommendation,
                'analysis': analysis,
                'confidence': confidence,
                'ml_features': {
                    'classification_prediction': int(classification_pred),
                    'regression_prediction': float(regression_pred),
                    'anomaly_score': float(anomaly_score),
                    'cluster': int(cluster_pred),
                    'expected_return': f"{regression_pred*100:.2f}%"
                },
                'bollinger_data': {
                    'upper_band': float(df['upper_band'].iloc[-1]),
                    'middle_band': float(df['middle_band'].iloc[-1]),
                    'lower_band': float(df['lower_band'].iloc[-1]),
                    'band_position': float(df['band_position'].iloc[-1]),
                    'volatility': float(df['volatility'].iloc[-1])
                }
            }
            
        except Exception as e:
            print(f"Error in ML prediction: {e}")
            return self._fallback_analysis(bollinger_entries)
    
    def _calculate_confidence(self, class_pred: float, reg_pred: float, 
                            anomaly_score: float, cluster_pred: int, df: pd.DataFrame) -> int:
        """Calculate confidence score based on multiple factors"""
        confidence = 50  # Base confidence
        
        # Classification confidence (higher for extreme predictions)
        if class_pred in [0, 4]:  # Strong signals
            confidence += 20
        elif class_pred in [1, 3]:  # Moderate signals
            confidence += 10
        
        # Regression confidence (higher for larger predicted moves)
        if abs(reg_pred) > 0.05:
            confidence += 15
        elif abs(reg_pred) > 0.02:
            confidence += 10
        
        # Anomaly confidence (lower confidence for anomalies)
        if anomaly_score < -0.5:  # Anomaly detected
            confidence -= 20
        
        # Volatility confidence (lower confidence in high volatility)
        current_volatility = df['volatility'].iloc[-1]
        if current_volatility > 0.1:
            confidence -= 15
        elif current_volatility < 0.05:
            confidence += 10
        
        # Band position confidence
        band_position = df['band_position'].iloc[-1]
        if band_position < 0.1 or band_position > 0.9:  # Near bands
            confidence += 10
        
        return max(10, min(95, confidence))
    
    def _generate_analysis_text(self, recommendation: str, class_pred: float, 
                              reg_pred: float, anomaly_score: float, df: pd.DataFrame) -> str:
        """Generate detailed analysis text"""
        analysis_parts = []
        
        # Recommendation basis
        if class_pred == 4:
            analysis_parts.append("ML model predicts strong bullish momentum")
        elif class_pred == 3:
            analysis_parts.append("ML model indicates moderate buying opportunity")
        elif class_pred == 2:
            analysis_parts.append("ML model suggests neutral position")
        elif class_pred == 1:
            analysis_parts.append("ML model indicates moderate selling pressure")
        else:
            analysis_parts.append("ML model predicts strong bearish momentum")
        
        # Expected return
        if abs(reg_pred) > 0.02:
            direction = "gain" if reg_pred > 0 else "loss"
            analysis_parts.append(f"Expected {abs(reg_pred)*100:.1f}% {direction} over next 5 days")
        
        # Anomaly detection
        if anomaly_score < -0.5:
            analysis_parts.append("Anomaly detection suggests unusual market conditions")
        
        # Bollinger Band context
        band_position = df['band_position'].iloc[-1]
        if band_position < 0.1:
            analysis_parts.append("Price near lower Bollinger Band - potential oversold condition")
        elif band_position > 0.9:
            analysis_parts.append("Price near upper Bollinger Band - potential overbought condition")
        
        # Volatility context
        volatility = df['volatility'].iloc[-1]
        if volatility > 0.1:
            analysis_parts.append("High volatility detected - increased risk")
        elif volatility < 0.05:
            analysis_parts.append("Low volatility - potential breakout opportunity")
        
        return ". ".join(analysis_parts) + "."
    
    def _fallback_analysis(self, bollinger_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback to simple analysis when ML models aren't available"""
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
        close = float(latest_bollinger.get('close', 0))
        
        # Simple analysis
        band_width = upper_band - lower_band
        band_position = (close - lower_band) / band_width if band_width > 0 else 0.5
        
        if band_position < 0.1:
            recommendation = 'BUY'
            analysis = "Price near lower Bollinger Band - potential oversold condition"
            confidence = 70
        elif band_position > 0.9:
            recommendation = 'SELL'
            analysis = "Price near upper Bollinger Band - potential overbought condition"
            confidence = 70
        else:
            recommendation = 'HOLD'
            analysis = "Price within normal Bollinger Band range"
            confidence = 50
        
        return {
            'recommendation': recommendation,
            'analysis': analysis,
            'confidence': confidence,
            'bollinger_data': {
                'upper_band': upper_band,
                'middle_band': middle_band,
                'lower_band': lower_band,
                'band_position': band_position,
                'volatility': band_width / middle_band if middle_band > 0 else 0
            }
        }

# Global analyzer instance
ml_analyzer = BollingerMLAnalyzer()

def analyze_bollinger_current(bollinger_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze current Bollinger Bands position and provide ML-enhanced recommendation"""
    # Try to train models if we have enough data
    if len(bollinger_entries) >= 50 and not ml_analyzer.is_trained:
        ml_analyzer.train_models(bollinger_entries)
    
    # Get ML-enhanced prediction
    return ml_analyzer.predict_signal(bollinger_entries)

def train_bollinger_models(bollinger_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Train the ML models with historical data"""
    success = ml_analyzer.train_models(bollinger_entries)
    return {
        'success': success,
        'message': 'Models trained successfully' if success else 'Insufficient data for training',
        'data_points_used': len(bollinger_entries) if success else 0
    } 