"""
Person Detection Model using MediaPipe
"""
import cv2
import mediapipe as mp
import numpy as np
import logging

logger = logging.getLogger(__name__)

class PersonDetector:
    """Detect number of persons in frame"""
    
    def __init__(self):
        """Initialize person detector"""
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=0)
        
    def detect_persons(self, frame):
        """
        Detect number of persons in frame
        
        Args:
            frame: Input video frame
            
        Returns:
            dict: Detection results
        """
        try:
            if frame is None or frame.size == 0:
                return {
                    'person_detected': False,
                    'person_count': 0,
                    'confidence': 0,
                    'multiple_persons': False
                }
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.segmentation.process(frame_rgb)
            
            # Get foreground mask
            mask = results.segmentation_mask
            
            # Find contours (represents persons/objects)
            mask_binary = (mask > 0.5).astype(np.uint8)
            mask_8bit = (mask_binary * 255).astype(np.uint8)
            
            contours, _ = cv2.findContours(mask_8bit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours by size (remove noise)
            h, w = mask.shape
            min_area = (h * w) * 0.05  # Minimum 5% of frame
            max_area = (h * w) * 0.95  # Maximum 95% of frame
            
            persons = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if min_area < area < max_area:
                    x, y, cw, ch = cv2.boundingRect(contour)
                    persons.append({
                        'bbox': (x, y, cw, ch),
                        'area': area
                    })
            
            person_count = len(persons)
            
            return {
                'person_detected': person_count > 0,
                'person_count': person_count,
                'confidence': 0.8,
                'multiple_persons': person_count > 1,
                'persons': persons
            }
            
        except Exception as e:
            logger.error(f"Person detection error: {str(e)}")
            return {
                'person_detected': False,
                'person_count': 0,
                'confidence': 0,
                'error': str(e)
            }