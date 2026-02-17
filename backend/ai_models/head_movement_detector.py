"""
Head Movement and Extreme Pose Detection
"""
import cv2
import mediapipe as mp
import numpy as np
import logging

logger = logging.getLogger(__name__)

class HeadMovementDetector:
    """Detect suspicious head movements"""
    
    def __init__(self):
        """Initialize head movement detector"""
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5
        )
        
        self.prev_head_position = None
        self.movement_threshold = 0.15  # Relative movement threshold
        self.extreme_angle_threshold = 45  # Degrees
        
    def detect_head_movement(self, frame):
        """
        Detect suspicious head movements
        
        Args:
            frame: Input video frame
            
        Returns:
            dict: Movement detection results
        """
        try:
            if frame is None or frame.size == 0:
                return {
                    'extreme_movement': False,
                    'movement_speed': 0,
                    'head_angle': 0,
                    'confidence': 0
                }
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = frame.shape
            
            results = self.pose.process(frame_rgb)
            
            if not results.pose_landmarks:
                return {
                    'extreme_movement': False,
                    'movement_speed': 0,
                    'head_angle': 0,
                    'confidence': 0
                }
            
            landmarks = results.pose_landmarks.landmark
            
            # Get head position (nose landmark)
            nose = landmarks[0]  # Nose
            left_shoulder = landmarks[11]  # Left shoulder
            right_shoulder = landmarks[12]  # Right shoulder
            
            current_head_pos = np.array([nose.x, nose.y])
            
            # Calculate movement speed
            movement_speed = 0
            if self.prev_head_position is not None:
                movement_speed = np.linalg.norm(current_head_pos - self.prev_head_position)
            
            self.prev_head_position = current_head_pos
            
            # Calculate head angle
            head_angle = self._calculate_head_angle(nose, left_shoulder, right_shoulder)
            
            # Determine if movement is extreme
            extreme_movement = movement_speed > self.movement_threshold or \
                             abs(head_angle) > self.extreme_angle_threshold
            
            return {
                'extreme_movement': extreme_movement,
                'movement_speed': float(movement_speed),
                'head_angle': float(head_angle),
                'confidence': 0.8,
                'suspicious': extreme_movement
            }
            
        except Exception as e:
            logger.error(f"Head movement detection error: {str(e)}")
            return {
                'extreme_movement': False,
                'movement_speed': 0,
                'head_angle': 0,
                'error': str(e)
            }
    
    def _calculate_head_angle(self, nose, left_shoulder, right_shoulder):
        """Calculate head angle relative to shoulders"""
        try:
            # Create vector from left to right shoulder
            shoulder_vector = np.array([right_shoulder.x - left_shoulder.x, 
                                       right_shoulder.y - left_shoulder.y])
            
            # Create vector from center of shoulders to nose
            center_shoulder = np.array([(left_shoulder.x + right_shoulder.x) / 2,
                                       (left_shoulder.y + right_shoulder.y) / 2])
            head_vector = np.array([nose.x - center_shoulder[0],
                                   nose.y - center_shoulder[1]])
            
            # Calculate angle
            if np.linalg.norm(shoulder_vector) == 0 or np.linalg.norm(head_vector) == 0:
                return 0
            
            cos_angle = np.dot(shoulder_vector, head_vector) / \
                       (np.linalg.norm(shoulder_vector) * np.linalg.norm(head_vector))
            
            angle = np.arccos(np.clip(cos_angle, -1, 1)) * 180 / np.pi
            
            return angle
            
        except:
            return 0