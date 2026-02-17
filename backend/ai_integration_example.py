"""
Example of how to integrate AI models in your proctoring system
"""
from ai_models.model_manager import get_detection_manager
import logging

logger = logging.getLogger(__name__)

def process_exam_frame(frame, prev_frame=None):
    """
    Process frame during exam and detect violations
    
    Args:
        frame: Current video frame
        prev_frame: Previous frame for motion analysis
        
    Returns:
        dict: Detected violations
    """
    try:
        # Get detection manager
        detector = get_detection_manager()
        
        # Analyze frame
        detections = detector.analyze_frame(frame, prev_frame)
        
        # Check for violations
        violations = []
        
        # Check face detection
        if detections.get('face', {}).get('face_detected') is False:
            violations.append({
                'type': 'face_not_visible',
                'severity': 'high',
                'confidence': 0.9
            })
        
        # Check eye gaze
        if detections.get('eye_gaze', {}).get('is_suspicious'):
            violations.append({
                'type': 'eye_gaze_suspicious',
                'severity': 'medium',
                'confidence': detections['eye_gaze'].get('confidence', 0.5)
            })
        
        # Check phone
        if detections.get('phone', {}).get('phone_detected'):
            violations.append({
                'type': 'phone_detected',
                'severity': 'high',
                'confidence': detections['phone'].get('confidence', 0.8)
            })
        
        # Check blur
        if detections.get('blur', {}).get('background_blurred') is False:
            violations.append({
                'type': 'blur_exit_attempt',
                'severity': 'high',
                'confidence': 0.8
            })
        
        # Check for blur removal attempt
        if detections.get('blur', {}).get('removal_attempt'):
            violations.append({
                'type': 'blur_removal_attempt',
                'severity': 'high',
                'confidence': 0.9
            })
        
        # Check multiple persons
        if detections.get('persons', {}).get('multiple_persons'):
            violations.append({
                'type': 'multiple_persons',
                'severity': 'high',
                'confidence': 0.85,
                'person_count': detections['persons'].get('person_count', 0)
            })
        
        # Check head movement
        if detections.get('head_movement', {}).get('extreme_movement'):
            violations.append({
                'type': 'extreme_head_movement',
                'severity': 'medium',
                'confidence': detections['head_movement'].get('confidence', 0.7)
            })
        
        return {
            'violations': violations,
            'detections': detections,
            'violation_count': len(violations)
        }
        
    except Exception as e:
        logger.error(f"Error processing frame: {str(e)}")
        return {
            'violations': [],
            'detections': {},
            'violation_count': 0,
            'error': str(e)
        }

def process_exam_audio(audio_data):
    """
    Process audio during exam
    
    Args:
        audio_data: Audio data as numpy array
        
    Returns:
        dict: Audio analysis results
    """
    try:
        detector = get_detection_manager()
        
        audio_analysis = detector.analyze_audio(audio_data)
        
        violations = []
        
        if audio_analysis.get('sound', {}).get('sound_detected'):
            violations.append({
                'type': 'sound_detected',
                'severity': 'low',
                'confidence': audio_analysis['sound'].get('confidence', 0.6),
                'volume_level': audio_analysis['sound'].get('volume_level')
            })
        
        return {
            'violations': violations,
            'audio_analysis': audio_analysis,
            'violation_count': len(violations)
        }
        
    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        return {
            'violations': [],
            'audio_analysis': {},
            'violation_count': 0,
            'error': str(e)
        }