from flask import Flask, request, jsonify
import json
import os
import logging
from datetime import datetime
from collections import deque

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProfessionalTradingAI:
    def __init__(self):
        self.model_data = {
            'signals': deque(maxlen=1000),  # Store last 1000 signals for learning
            'accuracy_tracker': {'correct': 0, 'total': 0},
            'pattern_weights': {
                'rsi_neutral': 0.6,
                'ema_bearish': 0.7,
                'sma_bearish': 0.7,
                'macd_neutral': 0.5,
                'vix_calm': 0.8,
                'bollinger_within': 0.4,
                'cci_sell': 0.8,
                'supertrend_bullish': 0.9,
                'volume_weak': -0.3,
                'aroon_uptrend': 0.7,
                'parabolic_bearish': 0.6,
                'mfi_oversold': 0.8,
                'price_ranging': -0.2,
                'volume_strength_weak': -0.4
            }
        }
        logger.info("Professional Trading AI initialized")
    
    def analyze_comprehensive_signals(self, data):
        """Analyze comprehensive technical indicators"""
        signals = []
        strength = 0
        
        # RSI Analysis
        rsi_value = float(data.get('RSI', {}).get('rsi', 50))
        rsi_status = data.get('RSI', {}).get('status', 'Neutral')
        
        if rsi_value < 35:  # NIFTY oversold threshold
            signals.append("RSI_OVERSOLD")
            strength += 0.8
        elif rsi_value > 65:  # NIFTY overbought threshold
            signals.append("RSI_OVERBOUGHT")
            strength -= 0.8
        elif rsi_status == 'Neutral':
            signals.append("RSI_NEUTRAL")
            strength += self.model_data['pattern_weights']['rsi_neutral']
        
        # EMA Analysis
        ema_status = data.get('EMA20', {}).get('status', 'Neutral')
        if ema_status == 'Bearish':
            signals.append("EMA_BEARISH")
            strength -= self.model_data['pattern_weights']['ema_bearish']
        elif ema_status == 'Bullish':
            signals.append("EMA_BULLISH")
            strength += self.model_data['pattern_weights']['ema_bearish']
        
        # SMA Analysis
        sma_status = data.get('SMA50', {}).get('status', 'Neutral')
        if sma_status == 'Bearish':
            signals.append("SMA_BEARISH")
            strength -= self.model_data['pattern_weights']['sma_bearish']
        elif sma_status == 'Bullish':
            signals.append("SMA_BULLISH")
            strength += self.model_data['pattern_weights']['sma_bearish']
        
        # MACD Analysis
        macd_status = data.get('MACD', {}).get('status', 'Neutral')
        macd_histogram = float(data.get('MACD', {}).get('histogram', 0))
        
        if macd_status == 'Bullish' or macd_histogram > 0:
            signals.append("MACD_BULLISH")
            strength += 0.7
        elif macd_status == 'Bearish' or macd_histogram < 0:
            signals.append("MACD_BEARISH")
            strength -= 0.7
        else:
            signals.append("MACD_NEUTRAL")
            strength += self.model_data['pattern_weights']['macd_neutral']
        
        # VIX Analysis
        vix_value = float(data.get('VIX', {}).get('vix', 15))
        vix_status = data.get('VIX', {}).get('status', 'Normal')
        
        if vix_status == 'Calm Market' or vix_value < 15:
            signals.append("VIX_CALM")
            strength += self.model_data['pattern_weights']['vix_calm']
        elif vix_value > 20:
            signals.append("VIX_HIGH")
            strength -= 0.5
        
        # Bollinger Bands Analysis
        bb_status = data.get('BollingerBands', {}).get('status', 'Within Bands')
        if bb_status == 'Within Bands':
            signals.append("BOLLINGER_WITHIN")
            strength += self.model_data['pattern_weights']['bollinger_within']
        elif bb_status == 'Above Upper':
            signals.append("BOLLINGER_OVERBOUGHT")
            strength -= 0.6
        elif bb_status == 'Below Lower':
            signals.append("BOLLINGER_OVERSOLD")
            strength += 0.6
        
        # CCI Analysis
        cci_value = float(data.get('CCI', {}).get('value', 0))
        cci_status = data.get('CCI', {}).get('status', 'Neutral')
        
        if cci_status == 'Sell' or cci_value < -100:
            signals.append("CCI_SELL")
            strength -= self.model_data['pattern_weights']['cci_sell']
        elif cci_status == 'Buy' or cci_value > 100:
            signals.append("CCI_BUY")
            strength += self.model_data['pattern_weights']['cci_sell']
        
        # SuperTrend Analysis
        supertrend_status = data.get('SuperTrend', {}).get('status', 'Neutral')
        if supertrend_status == 'Bullish':
            signals.append("SUPERTREND_BULLISH")
            strength += self.model_data['pattern_weights']['supertrend_bullish']
        elif supertrend_status == 'Bearish':
            signals.append("SUPERTREND_BEARISH")
            strength -= self.model_data['pattern_weights']['supertrend_bullish']
        
        # Volume Analysis
        volume_status = data.get('VolumeIndicators', {}).get('status', 'Normal')
        volume_strength = data.get('VolumeStrength', {}).get('type', 'Normal')
        
        if volume_status == 'Weak' or volume_strength == 'Weak Volume':
            signals.append("VOLUME_WEAK")
            strength += self.model_data['pattern_weights']['volume_weak']
        elif volume_status == 'Strong':
            signals.append("VOLUME_STRONG")
            strength += 0.5
        
        # Aroon Analysis
        aroon_status = data.get('Aroon', {}).get('status', 'Neutral')
        if aroon_status == 'Uptrend':
            signals.append("AROON_UPTREND")
            strength += self.model_data['pattern_weights']['aroon_uptrend']
        elif aroon_status == 'Downtrend':
            signals.append("AROON_DOWNTREND")
            strength -= self.model_data['pattern_weights']['aroon_uptrend']
        
        # Parabolic SAR Analysis
        psar_status = data.get('ParabolicSAR', {}).get('status', 'Neutral')
        if psar_status == 'Bearish':
            signals.append("PARABOLIC_BEARISH")
            strength -= self.model_data['pattern_weights']['parabolic_bearish']
        elif psar_status == 'Bullish':
            signals.append("PARABOLIC_BULLISH")
            strength += self.model_data['pattern_weights']['parabolic_bearish']
        
        # MFI Analysis
        mfi_value = float(data.get('MFI', {}).get('value', 50))
        mfi_status = data.get('MFI', {}).get('status', 'Neutral')
        
        if mfi_status == 'Oversold' or mfi_value < 20:
            signals.append("MFI_OVERSOLD")
            strength += self.model_data['pattern_weights']['mfi_oversold']
        elif mfi_status == 'Overbought' or mfi_value > 80:
            signals.append("MFI_OVERBOUGHT")
            strength -= self.model_data['pattern_weights']['mfi_oversold']
        
        # Price Action Analysis
        price_action = data.get('PriceAction', {}).get('type', 'Normal')
        if price_action == 'Ranging':
            signals.append("PRICE_RANGING")
            strength += self.model_data['pattern_weights']['price_ranging']
        elif price_action == 'Trending':
            signals.append("PRICE_TRENDING")
            strength += 0.3
        
        return signals, strength
    
    def analyze_volume_patterns(self, data):
        """Analyze volume patterns and strength"""
        signals = []
        strength = 0
        
        # Volume Spike Analysis
        volume_spike = data.get('VolumeSpike', {}).get('spike', False)
        if volume_spike:
            signals.append("VOLUME_SPIKE")
            strength += 0.6
        
        # Volume Strength Analysis
        volume_strength_score = data.get('VolumeStrength', {}).get('score', 0)
        if volume_strength_score < -0.5:
            signals.append("VOLUME_STRENGTH_WEAK")
            strength += self.model_data['pattern_weights']['volume_strength_weak']
        elif volume_strength_score > 0.5:
            signals.append("VOLUME_STRENGTH_STRONG")
            strength += 0.5
        
        return signals, strength
    
    def analyze_trend_indicators(self, data):
        """Analyze trend-based indicators"""
        signals = []
        strength = 0
        
        # ADX Trend Strength
        adx_value = float(data.get('ADX', {}).get('value', 20))
        if adx_value > 25:
            signals.append("STRONG_TREND")
            strength += 0.4
        elif adx_value < 20:
            signals.append("WEAK_TREND")
            strength -= 0.2
        
        # Stochastic Analysis
        stoch_value = float(data.get('Stochastic', {}).get('value', 50))
        stoch_status = data.get('Stochastic', {}).get('status', 'Neutral')
        
        if stoch_value < 20:
            signals.append("STOCHASTIC_OVERSOLD")
            strength += 0.6
        elif stoch_value > 80:
            signals.append("STOCHASTIC_OVERBOUGHT")
            strength -= 0.6
        
        # ATR Volatility Analysis
        atr_value = float(data.get('ATR', {}).get('value', 20))
        if atr_value > 25:
            signals.append("HIGH_VOLATILITY")
            strength -= 0.3
        elif atr_value < 15:
            signals.append("LOW_VOLATILITY")
            strength += 0.2
        
        return signals, strength
    
    def analyze_price_position(self, data):
        """Analyze price position relative to key levels"""
        signals = []
        strength = 0
        
        ltp = float(data.get('LTP', 0))
        
        # Bollinger Bands Position
        bb_upper = float(data.get('BollingerBands', {}).get('upper', ltp + 50))
        bb_lower = float(data.get('BollingerBands', {}).get('lower', ltp - 50))
        
        bb_position = (ltp - bb_lower) / (bb_upper - bb_lower) if bb_upper != bb_lower else 0.5
        
        if bb_position > 0.8:
            signals.append("NEAR_BB_UPPER")
            strength -= 0.5
        elif bb_position < 0.2:
            signals.append("NEAR_BB_LOWER")
            strength += 0.5
        
        # EMA Position
        ema_value = float(data.get('EMA20', {}).get('ema', ltp))
        if ltp > ema_value:
            signals.append("ABOVE_EMA")
            strength += 0.3
        else:
            signals.append("BELOW_EMA")
            strength -= 0.3
        
        # SMA Position
        sma_value = float(data.get('SMA50', {}).get('sma', ltp))
        if ltp > sma_value:
            signals.append("ABOVE_SMA")
            strength += 0.3
        else:
            signals.append("BELOW_SMA")
            strength -= 0.3
        
        return signals, strength
    
    def analyze_oscillators(self, data):
        """Analyze oscillator indicators"""
        signals = []
        strength = 0
        
        # CCI Analysis
        cci_value = float(data.get('CCI', {}).get('value', 0))
        cci_status = data.get('CCI', {}).get('status', 'Neutral')
        
        if cci_status == 'Sell' or cci_value < -100:
            signals.append("CCI_OVERSOLD")
            strength += 0.7
        elif cci_status == 'Buy' or cci_value > 100:
            signals.append("CCI_OVERBOUGHT")
            strength -= 0.7
        
        # MFI Analysis
        mfi_value = float(data.get('MFI', {}).get('value', 50))
        mfi_status = data.get('MFI', {}).get('status', 'Neutral')
        
        if mfi_status == 'Oversold' or mfi_value < 20:
            signals.append("MFI_OVERSOLD")
            strength += 0.8
        elif mfi_status == 'Overbought' or mfi_value > 80:
            signals.append("MFI_OVERBOUGHT")
            strength -= 0.8
        
        return signals, strength
    
    def professional_signal_generation(self, data):
        """Generate professional trading signals"""
        try:
            # Handle both old and new data formats
            if isinstance(data, list) and len(data) > 0:
                # New format - extract from array
                market_data = data[0]
            else:
                # Old format - use directly
                market_data = data
            
            # Extract key values
            ltp = float(market_data.get('LTP', 0))
            vix_value = float(market_data.get('VIX', {}).get('vix', 15))
            rsi_value = float(market_data.get('RSI', {}).get('rsi', 50))
            
            # Analyze all components
            all_signals = []
            total_strength = 0
            
            # Comprehensive Technical Analysis
            comp_signals, comp_strength = self.analyze_comprehensive_signals(market_data)
            all_signals.extend(comp_signals)
            total_strength += comp_strength
            
            # Volume Pattern Analysis
            vol_signals, vol_strength = self.analyze_volume_patterns(market_data)
            all_signals.extend(vol_signals)
            total_strength += vol_strength
            
            # Trend Indicator Analysis
            trend_signals, trend_strength = self.analyze_trend_indicators(market_data)
            all_signals.extend(trend_signals)
            total_strength += trend_strength
            
            # Price Position Analysis
            price_signals, price_strength = self.analyze_price_position(market_data)
            all_signals.extend(price_signals)
            total_strength += price_strength
            
            # Oscillator Analysis
            osc_signals, osc_strength = self.analyze_oscillators(market_data)
            all_signals.extend(osc_signals)
            total_strength += osc_strength
            
            # VIX Filter and Market Regime
            vix_condition = self.determine_vix_condition(vix_value)
            
            # Professional Decision Making
            signal, confidence = self.make_professional_decision(
                all_signals, total_strength, market_data
            )
            
            # Store for learning
            signal_data = {
                'timestamp': datetime.now().isoformat(),
                'signal': signal,
                'confidence': confidence,
                'all_signals': all_signals,
                'strength': total_strength,
                'market_data': market_data
            }
            self.model_data['signals'].append(signal_data)
            
            return {
                'signal': signal,
                'confidence': round(confidence, 3),
                'analysis': {
                    'detected_signals': all_signals,
                    'total_strength': round(total_strength, 2),
                    'vix_condition': vix_condition,
                    'market_regime': self.determine_market_regime(market_data),
                    'ltp': ltp,
                    'signal_count': len(all_signals)
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in signal generation: {e}")
            return {
                'signal': 'HOLD',
                'confidence': 0.0,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def determine_vix_condition(self, vix):
        """Determine VIX condition"""
        if vix > 25:
            return "EXTREME_VOLATILITY"
        elif vix > 18:
            return "HIGH_VOLATILITY"
        elif vix < 12:
            return "LOW_VOLATILITY"
        else:
            return "NORMAL_VOLATILITY"
    
    def make_professional_decision(self, signals, strength, market_data):
        """Make professional trading decision based on all factors"""
        
        # Extract key values
        vix_value = float(market_data.get('VIX', {}).get('vix', 15))
        rsi_value = float(market_data.get('RSI', {}).get('rsi', 50))
        supertrend_status = market_data.get('SuperTrend', {}).get('status', 'Neutral')
        aroon_status = market_data.get('Aroon', {}).get('status', 'Neutral')
        
        # VIX Filter - No trading in high volatility
        if vix_value > 18:
            return 'HOLD', 0.0
        
        # Count bullish and bearish signals
        bullish_signals = [s for s in signals if any(word in s for word in 
                          ['BULLISH', 'OVERSOLD', 'BUY', 'UPTREND', 'STRONG', 'ABOVE'])]
        bearish_signals = [s for s in signals if any(word in s for word in 
                          ['BEARISH', 'OVERBOUGHT', 'SELL', 'DOWNTREND', 'WEAK', 'BELOW'])]
        
        bullish_count = len(bullish_signals)
        bearish_count = len(bearish_signals)
        
        # Base confidence from signal strength
        base_confidence = min(abs(strength) / 3.0, 1.0)  # Normalize to 0-1
        
        # Professional decision logic
        if strength > 1.5 and bullish_count >= 3:
            # Strong bullish setup
            if supertrend_status == 'Bullish' and rsi_value < 60:
                return 'BUY_CE', min(base_confidence + 0.2, 0.95)
            elif aroon_status == 'Uptrend' and rsi_value < 65:
                return 'BUY_CE', min(base_confidence + 0.1, 0.85)
            else:
                return 'BUY_CE', base_confidence
                
        elif strength < -1.5 and bearish_count >= 3:
            # Strong bearish setup
            if supertrend_status == 'Bearish' and rsi_value > 40:
                return 'BUY_PE', min(base_confidence + 0.2, 0.95)
            elif aroon_status == 'Downtrend' and rsi_value > 35:
                return 'BUY_PE', min(base_confidence + 0.1, 0.85)
            else:
                return 'BUY_PE', base_confidence
                
        elif abs(strength) > 1.0:
            # Moderate signals
            if strength > 0 and bullish_count > bearish_count:
                return 'BUY_CE', max(base_confidence, 0.65)
            elif strength < 0 and bearish_count > bullish_count:
                return 'BUY_PE', max(base_confidence, 0.65)
        
        # Default to HOLD
        return 'HOLD', 0.0
    
    def determine_market_regime(self, data):
        """Determine current market regime"""
        vix_value = float(data.get('VIX', {}).get('vix', 15))
        rsi_value = float(data.get('RSI', {}).get('rsi', 50))
        supertrend_status = data.get('SuperTrend', {}).get('status', 'Neutral')
        price_action = data.get('PriceAction', {}).get('type', 'Normal')
        
        if vix_value > 20:
            return "HIGH_VOLATILITY"
        elif vix_value < 12:
            return "LOW_VOLATILITY"
        elif supertrend_status == 'Bullish' and rsi_value < 70:
            return "BULLISH_TREND"
        elif supertrend_status == 'Bearish' and rsi_value > 30:
            return "BEARISH_TREND"
        elif price_action == 'Ranging':
            return "SIDEWAYS_RANGING"
        else:
            return "SIDEWAYS_MARKET"

# Initialize the AI model
trading_ai = ProfessionalTradingAI()

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Generate professional trading signal
        result = trading_ai.professional_signal_generation(data)
        
        logger.info(f"Prediction: {result['signal']} with confidence {result['confidence']}")
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in predict endpoint: {e}")
        return jsonify({
            'signal': 'HOLD',
            'confidence': 0.0,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    accuracy = 0.0
    if trading_ai.model_data['accuracy_tracker']['total'] > 0:
        accuracy = trading_ai.model_data['accuracy_tracker']['correct'] / trading_ai.model_data['accuracy_tracker']['total']
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_loaded': True,
        'total_signals': len(trading_ai.model_data['signals']),
        'accuracy': round(accuracy, 3),
        'pattern_weights': trading_ai.model_data['pattern_weights']
    })

@app.route('/update_accuracy', methods=['POST'])
def update_accuracy():
    """Update model accuracy based on trade outcomes"""
    try:
        data = request.get_json()
        predicted_signal = data.get('predicted_signal')
        actual_outcome = data.get('actual_outcome')  # 'correct' or 'incorrect'
        
        trading_ai.model_data['accuracy_tracker']['total'] += 1
        if actual_outcome == 'correct':
            trading_ai.model_data['accuracy_tracker']['correct'] += 1
        
        return jsonify({'message': 'Accuracy updated successfully'})
    
    except Exception as e:
        logger.error(f"Error updating accuracy: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_stats', methods=['GET'])
def get_stats():
    """Get model statistics"""
    try:
        accuracy = 0.0
        if trading_ai.model_data['accuracy_tracker']['total'] > 0:
            accuracy = trading_ai.model_data['accuracy_tracker']['correct'] / trading_ai.model_data['accuracy_tracker']['total']
        
        recent_signals = list(trading_ai.model_data['signals'])[-10:]  # Last 10 signals
        
        return jsonify({
            'total_predictions': trading_ai.model_data['accuracy_tracker']['total'],
            'correct_predictions': trading_ai.model_data['accuracy_tracker']['correct'],
            'accuracy': round(accuracy, 3),
            'recent_signals': recent_signals,
            'pattern_weights': trading_ai.model_data['pattern_weights']
        })
    
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
