"""
Eye Gaze Tracking Model using MediaPipe Facemesh
"""
import cv2
import mediapipe as mp
import numpy as np
import logging
from scipy.spatial import distance

logger = logging.getLogger(__name__)

class EyeGazeTracker:
    """Track eye gaze direction for suspicious behavior"""
    
    def __init__(self):
        """Initialize eye gaze tracker"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5
        )
        
        # Eye landmark indices
        self.LEFT_EYE_INDICES = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.RIGHT_EYE_INDICES = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        
    def detect_eye_gaze(self, frame):
        """
        Detect eye gaze direction
        
        Args:
            frame: Input video frame
            
        Returns:
            dict: Eye gaze information
        """
        try:
            if frame is None or frame.size == 0:
                return {
                    'looking_at_screen': True,
                    'gaze_direction': 'center',
                    'confidence': 0,
                    'is_suspicious': False
                }
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(frame_rgb)
            
            if not results.multi_face_landmarks:
                return {
                    'looking_at_screen': False,
                    'gaze_direction': 'unknown',
                    'confidence': 0,
                    'is_suspicious': True
                }
            
            landmarks = results.multi_face_landmarks[0].landmark
            h, w, c = frame.shape
            
            # Get eye positions
            left_eye = self._get_eye_center(landmarks, self.LEFT_EYE_INDICES)
            right_eye = self._get_eye_center(landmarks, self.RIGHT_EYE_INDICES)
            
            # Calculate gaze direction
            gaze_direction = self._calculate_gaze_direction(left_eye, right_eye, w, h)
            
            # Determine if looking at screen
            looking_at_screen = gaze_direction == 'center' or gaze_direction == 'center-left' or gaze_direction == 'center-right'
            
            return {
                'looking_at_screen': looking_at_screen,
                'gaze_direction': gaze_direction,
                'confidence': 0.8,
                'is_suspicious': not looking_at_screen,
                'left_eye': left_eye,
                'right_eye': right_eye
            }
            
        except Exception as e:
            logger.error(f"Eye gaze tracking error: {str(e)}")
            return {
                'looking_at_screen': True,
                'gaze_direction': 'unknown',
                'confidence': 0,
                'error': str(e)
            }
    
    def _get_eye_center(self, landmarks, eye_indices):
        """Get center of eye from landmarks"""
        eye_points = np.array([[landmarks[i].x, landmarks[i].y] for i in eye_indices])
        return np.mean(eye_points, axis=0)
    
    def _calculate_gaze_direction(self, left_eye, right_eye, w, h):
        """Calculate gaze direction"""
        avg_eye_x = (left_eye[0] + right_eye[0]) / 2
        avg_eye_y = (left_eye[1] + right_eye[1]) / 2
        
        # Divide screen into regions
        if avg_eye_x < 0.33:
            horizontal = 'left'
        elif avg_eye_x > 0.66:
            horizontal = 'right'
        else:
            horizontal = 'center'
        
        if avg_eye_y < 0.33:
            vertical = 'up'
        elif avg_eye_y > 0.66:
            vertical = 'down'
        else:
            vertical = 'center'
        
        if vertical == 'center' and horizontal == 'center':
            return 'center'
        elif vertical == 'center':
            return f'center-{horizontal}'
        else:
            return f'{vertical}-{horizontal}'