"""
Background Blur Detection Model
"""
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

class BackgroundBlurDetector:
    """Detect background blur enforcement"""
    
    def __init__(self):
        """Initialize background blur detector"""
        self.blur_threshold = 50  # Threshold for blur detection
        
    def detect_blur_status(self, frame):
        """
        Detect if background is blurred
        
        Args:
            frame: Input video frame
            
        Returns:
            dict: Blur detection results
        """
        try:
            if frame is None or frame.size == 0:
                return {
                    'background_blurred': False,
                    'blur_strength': 0,
                    'confidence': 0
                }
            
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate Laplacian variance (measure of blur)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Analyze background
            h, w = gray.shape
            background = gray[int(h*0.7):, :].copy()
            background_var = cv2.Laplacian(background, cv2.CV_64F).var()
            
            # Determine if background is blurred
            is_blurred = background_var < self.blur_threshold
            blur_strength = max(0, min(1, (self.blur_threshold - background_var) / self.blur_threshold))
            
            return {
                'background_blurred': is_blurred,
                'blur_strength': float(blur_strength),
                'foreground_variance': float(laplacian_var),
                'background_variance': float(background_var),
                'confidence': 0.7
            }
            
        except Exception as e:
            logger.error(f"Blur detection error: {str(e)}")
            return {
                'background_blurred': False,
                'blur_strength': 0,
                'confidence': 0,
                'error': str(e)
            }
    
    def detect_blur_removal_attempt(self, prev_frame, curr_frame):
        """
        Detect if student is trying to remove blur
        
        Args:
            prev_frame: Previous frame
            curr_frame: Current frame
            
        Returns:
            bool: True if blur removal attempt detected
        """
        try:
            if prev_frame is None or curr_frame is None:
                return False
            
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate difference
            diff = cv2.absdiff(prev_gray, curr_gray)
            
            # Get background changes
            h, w = diff.shape
            background_diff = diff[int(h*0.7):, :].copy()
            
            # High change in background might indicate blur filter being toggled
            if np.mean(background_diff) > 50:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Blur removal detection error: {str(e)}")
            return False