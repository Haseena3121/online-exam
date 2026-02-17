"""
Face Detection Model using MediaPipe
"""
import cv2
import mediapipe as mp
import numpy as np
import logging

logger = logging.getLogger(__name__)

class FaceDetector:
    """Detect face presence and visibility"""
    
    def __init__(self):
        """Initialize face detection model"""
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,  # 1 for full range, 0 for close-range
            min_detection_confidence=0.5
        )
        self.min_face_size = 0.05  # Minimum face size relative to frame
        
    def detect_face(self, frame):
        """
        Detect face in frame
        
        Args:
            frame: Input video frame
            
        Returns:
            dict: Detection results with face presence and confidence
        """
        try:
            if frame is None or frame.size == 0:
                return {
                    'face_detected': False,
                    'confidence': 0,
                    'face_count': 0,
                    'face_size': 0
                }
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = frame.shape
            
            # Detect faces
            results = self.face_detection.process(frame_rgb)
            
            if not results.detections:
                return {
                    'face_detected': False,
                    'confidence': 0,
                    'face_count': 0,
                    'face_size': 0
                }
            
            # Analyze detections
            face_sizes = []
            confidences = []
            
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                face_width = bbox.width
                face_height = bbox.height
                face_size = face_width * face_height
                face_sizes.append(face_size)
                
                if hasattr(detection, 'score'):
                    confidences.append(detection.score[0])
            
            avg_confidence = np.mean(confidences) if confidences else 0
            avg_face_size = np.mean(face_sizes) if face_sizes else 0
            
            return {
                'face_detected': len(face_sizes) > 0,
                'confidence': float(avg_confidence),
                'face_count': len(face_sizes),
                'face_size': float(avg_face_size),
                'face_visible': avg_face_size > self.min_face_size
            }
            
        except Exception as e:
            logger.error(f"Face detection error: {str(e)}")
            return {
                'face_detected': False,
                'confidence': 0,
                'face_count': 0,
                'face_size': 0,
                'error': str(e)
            }
    
    def get_face_landmarks(self, frame):
        """
        Get face landmarks for additional analysis
        
        Args:
            frame: Input video frame
            
        Returns:
            dict: Face landmarks and mesh points
        """
        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(frame_rgb)
            
            if not results.detections:
                return None
            
            landmarks = []
            for detection in results.detections:
                face_landmarks = {
                    'bbox': detection.location_data.relative_bounding_box,
                    'keypoints': detection.location_data.relative_keypoints if hasattr(detection.location_data, 'relative_keypoints') else []
                }
                landmarks.append(face_landmarks)
            
            return landmarks
            
        except Exception as e:
            logger.error(f"Error getting landmarks: {str(e)}")
            return None