"""
Phone/Device Detection using COCO-SSD Model
"""
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

class PhoneDetector:
    """Detect mobile phones and suspicious devices"""
    
    def __init__(self):
        """Initialize phone detector"""
        # Try to import TensorFlow models
        try:
            import tensorflow as tf
            self.tf = tf
            self.model_loaded = True
        except ImportError:
            logger.warning("TensorFlow not available for phone detection")
            self.model_loaded = False
        
        # Objects to detect as suspicious
        self.suspicious_objects = [
            'cell phone', 'mobile phone', 'phone', 'handbag', 'book',
            'monitor', 'laptop', 'keyboard', 'mouse', 'remote'
        ]
        
        # Confidence threshold
        self.confidence_threshold = 0.5
    
    def detect_phone(self, frame):
        """
        Detect phone/device in frame
        
        Args:
            frame: Input video frame
            
        Returns:
            dict: Detection results
        """
        try:
            if frame is None or frame.size == 0:
                return {
                    'phone_detected': False,
                    'confidence': 0,
                    'objects_detected': []
                }
            
            # Simple edge-based detection if TensorFlow not available
            if not self.model_loaded:
                return self._simple_phone_detection(frame)
            
            # Advanced detection would go here
            # Using COCO-SSD or similar model
            
            return {
                'phone_detected': False,
                'confidence': 0,
                'objects_detected': [],
                'method': 'simple'
            }
            
        except Exception as e:
            logger.error(f"Phone detection error: {str(e)}")
            return {
                'phone_detected': False,
                'confidence': 0,
                'error': str(e)
            }
    
    def _simple_phone_detection(self, frame):
        """
        Simple phone detection using edges and contours
        
        Args:
            frame: Input video frame
            
        Returns:
            dict: Detection results
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect edges
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            # Look for rectangular shapes (typical phone shape)
            suspicious_count = 0
            rectangles = []
            
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
                
                # Look for 4-sided shapes (rectangles)
                if len(approx) == 4:
                    area = cv2.contourArea(contour)
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Phone-like dimensions (height > width, reasonable size)
                    if h > w and area > 500:
                        aspect_ratio = h / w
                        if 1.5 < aspect_ratio < 4:  # Phone-like aspect ratio
                            suspicious_count += 1
                            rectangles.append({
                                'bbox': (x, y, w, h),
                                'area': area,
                                'aspect_ratio': aspect_ratio
                            })
            
            return {
                'phone_detected': suspicious_count > 0,
                'confidence': min(suspicious_count * 0.3, 1.0),
                'suspicious_objects_count': suspicious_count,
                'objects_detected': rectangles,
                'method': 'edge_detection'
            }
            
        except Exception as e:
            logger.error(f"Simple phone detection error: {str(e)}")
            return {
                'phone_detected': False,
                'confidence': 0,
                'error': str(e)
            }