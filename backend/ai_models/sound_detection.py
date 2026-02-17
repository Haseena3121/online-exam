"""
Sound Detection Model for Exam Monitoring
"""
import numpy as np
import logging

logger = logging.getLogger(__name__)

class SoundDetector:
    """Detect unusual sounds during exam"""
    
    def __init__(self):
        """Initialize sound detector"""
        self.sample_rate = 16000
        self.noise_threshold = 0.3
        self.sound_threshold = 0.5
        self.min_duration = 0.5  # seconds
        
    def detect_sound(self, audio_data):
        """
        Detect unusual sounds
        
        Args:
            audio_data: Audio data as numpy array
            
        Returns:
            dict: Sound detection results
        """
        try:
            if audio_data is None or len(audio_data) == 0:
                return {
                    'sound_detected': False,
                    'volume': 0,
                    'confidence': 0
                }
            
            # Normalize audio
            audio_normalized = self._normalize_audio(audio_data)
            
            # Calculate RMS (Root Mean Square) for volume
            rms = np.sqrt(np.mean(audio_normalized ** 2))
            
            # Detect speech or unusual sounds
            is_speech = self._detect_speech_patterns(audio_normalized)
            
            # Determine if sound is suspicious
            suspicious_sound = rms > self.sound_threshold or is_speech
            
            return {
                'sound_detected': suspicious_sound,
                'volume': float(rms),
                'is_speech': is_speech,
                'confidence': float(min(rms, 1.0)),
                'volume_level': self._get_volume_level(rms)
            }
            
        except Exception as e:
            logger.error(f"Sound detection error: {str(e)}")
            return {
                'sound_detected': False,
                'volume': 0,
                'confidence': 0,
                'error': str(e)
            }
    
    def _normalize_audio(self, audio_data):
        """Normalize audio data"""
        max_val = np.max(np.abs(audio_data))
        if max_val == 0:
            return audio_data
        return audio_data / max_val
    
    def _detect_speech_patterns(self, audio_data):
        """Detect if audio contains speech"""
        try:
            # Simple frequency analysis
            # Speech typically has energy in 300-3000 Hz range
            fft = np.fft.fft(audio_data)
            frequencies = np.abs(fft)
            
            # Check energy in speech frequency band
            speech_energy = np.mean(frequencies)
            
            return speech_energy > self.noise_threshold
            
        except:
            return False
    
    def _get_volume_level(self, rms):
        """Classify volume level"""
        if rms < 0.1:
            return 'silent'
        elif rms < 0.3:
            return 'quiet'
        elif rms < 0.6:
            return 'normal'
        elif rms < 0.8:
            return 'loud'
        else:
            return 'very_loud'