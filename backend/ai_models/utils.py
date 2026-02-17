"""
Utility functions for AI models
"""
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

class AIModelUtils:
    """Utility functions for AI models"""
    
    @staticmethod
    def preprocess_frame(frame, target_size=(640, 480)):
        """
        Preprocess video frame
        
        Args:
            frame: Input frame
            target_size: Target size (width, height)
            
        Returns:
            Preprocessed frame
        """
        try:
            if frame is None:
                return None
            
            # Resize
            frame_resized = cv2.resize(frame, target_size)
            
            # Normalize
            frame_normalized = frame_resized.astype('float32') / 255.0
            
            return frame_normalized
            
        except Exception as e:
            logger.error(f"Frame preprocessing error: {str(e)}")
            return None
    
    @staticmethod
    def draw_detections(frame, detections):
        """
        Draw detection results on frame
        
        Args:
            frame: Input frame
            detections: Dictionary of detections
            
        Returns:
            Frame with drawn detections
        """
        try:
            output_frame = frame.copy()
            
            # Draw face detection
            if detections.get('face_detected'):
                cv2.putText(output_frame, 'Face Detected', (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Draw phone detection
            if detections.get('phone_detected'):
                cv2.putText(output_frame, 'Phone Detected!', (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Draw multiple persons
            if detections.get('multiple_persons'):
                cv2.putText(output_frame, 'Multiple Persons!', (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            return output_frame
            
        except Exception as e:
            logger.error(f"Drawing detections error: {str(e)}")
            return frame
    
    @staticmethod
    def calculate_frame_quality(frame):
        """
        Calculate frame quality metrics
        
        Args:
            frame: Input frame
            
        Returns:
            dict: Quality metrics
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate sharpness (Laplacian variance)
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Calculate brightness
            brightness = np.mean(gray)
            
            # Calculate contrast
            contrast = np.std(gray)
            
            # Determine quality level
            if sharpness > 500 and 50 < brightness < 200 and contrast > 30:
                quality_level = 'good'
            elif sharpness > 300 or (40 < brightness < 220 and contrast > 20):
                quality_level = 'fair'
            else:
                quality_level = 'poor'
            
            return {
                'sharpness': float(sharpness),
                'brightness': float(brightness),
                'contrast': float(contrast),
                'quality_level': quality_level
            }
            
        except Exception as e:
            logger.error(f"Frame quality calculation error: {str(e)}")
            return {
                'sharpness': 0,
                'brightness': 0,
                'contrast': 0,
                'quality_level': 'unknown'
            }