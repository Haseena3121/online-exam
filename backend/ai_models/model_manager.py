"""
Unified Model Manager for all AI detection models
"""
import logging
from .face_detection import FaceDetector
from .eye_gaze_tracking import EyeGazeTracker
from .phone_detection import PhoneDetector
from .sound_detection import SoundDetector
from .background_blur import BackgroundBlurDetector
from .person_detection import PersonDetector
from .head_movement_detector import HeadMovementDetector

logger = logging.getLogger(__name__)

class ViolationDetectionManager:
    """Unified manager for all violation detection models"""
    
    def __init__(self):
        """Initialize all detection models"""
        logger.info("Initializing violation detection models...")
        
        try:
            self.face_detector = FaceDetector()
            logger.info("✓ Face detection model loaded")
        except Exception as e:
            logger.warning(f"Face detection initialization failed: {str(e)}")
            self.face_detector = None
        
        try:
            self.eye_tracker = EyeGazeTracker()
            logger.info("✓ Eye gaze tracking model loaded")
        except Exception as e:
            logger.warning(f"Eye gaze tracking initialization failed: {str(e)}")
            self.eye_tracker = None
        
        try:
            self.phone_detector = PhoneDetector()
            logger.info("✓ Phone detection model loaded")
        except Exception as e:
            logger.warning(f"Phone detection initialization failed: {str(e)}")
            self.phone_detector = None
        
        try:
            self.sound_detector = SoundDetector()
            logger.info("✓ Sound detection model loaded")
        except Exception as e:
            logger.warning(f"Sound detection initialization failed: {str(e)}")
            self.sound_detector = None
        
        try:
            self.blur_detector = BackgroundBlurDetector()
            logger.info("✓ Background blur detection model loaded")
        except Exception as e:
            logger.warning(f"Background blur detection initialization failed: {str(e)}")
            self.blur_detector = None
        
        try:
            self.person_detector = PersonDetector()
            logger.info("✓ Person detection model loaded")
        except Exception as e:
            logger.warning(f"Person detection initialization failed: {str(e)}")
            self.person_detector = None
        
        try:
            self.head_detector = HeadMovementDetector()
            logger.info("✓ Head movement detection model loaded")
        except Exception as e:
            logger.warning(f"Head movement detection initialization failed: {str(e)}")
            self.head_detector = None
        
        logger.info("Violation detection manager initialized")
    
    def analyze_frame(self, frame, prev_frame=None):
        """
        Analyze frame for all violations
        
        Args:
            frame: Current frame
            prev_frame: Previous frame (for movement analysis)
            
        Returns:
            dict: All detection results
        """
        results = {}
        
        # Face detection
        if self.face_detector:
            results['face'] = self.face_detector.detect_face(frame)
        
        # Eye gaze tracking
        if self.eye_tracker:
            results['eye_gaze'] = self.eye_tracker.detect_eye_gaze(frame)
        
        # Phone detection
        if self.phone_detector:
            results['phone'] = self.phone_detector.detect_phone(frame)
        
        # Background blur
        if self.blur_detector:
            results['blur'] = self.blur_detector.detect_blur_status(frame)
            if prev_frame is not None:
                results['blur']['removal_attempt'] = self.blur_detector.detect_blur_removal_attempt(prev_frame, frame)
        
        # Person detection
        if self.person_detector:
            results['persons'] = self.person_detector.detect_persons(frame)
        
        # Head movement
        if self.head_detector:
            results['head_movement'] = self.head_detector.detect_head_movement(frame)
        
        return results
    
    def analyze_audio(self, audio_data):
        """
        Analyze audio for violations
        
        Args:
            audio_data: Audio data
            
        Returns:
            dict: Audio analysis results
        """
        results = {}
        
        if self.sound_detector:
            results['sound'] = self.sound_detector.detect_sound(audio_data)
        
        return results

# Singleton instance
_manager = None

def get_detection_manager():
    """Get or create detection manager instance"""
    global _manager
    if _manager is None:
        _manager = ViolationDetectionManager()
    return _manager