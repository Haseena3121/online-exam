"""
Violation detection and analysis service
"""
import logging
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)

class ViolationDetector:
    """Detect and analyze violations"""
    
    # Violation thresholds
    VIOLATION_THRESHOLDS = {
        'phone_detected': 20,
        'tab_switch': 10,
        'eye_gaze_suspicious': 10,
        'multiple_persons': 20,
        'sound_detected': 5,
        'blur_exit_attempt': 20,
        'face_not_visible': 15,
        'extreme_head_movement': 10
    }
    
    # Severity mapping
    SEVERITY_MAP = {
        'phone_detected': 'high',
        'tab_switch': 'high',
        'eye_gaze_suspicious': 'medium',
        'multiple_persons': 'high',
        'sound_detected': 'low',
        'blur_exit_attempt': 'high',
        'face_not_visible': 'high',
        'extreme_head_movement': 'medium'
    }
    
    @staticmethod
    def get_violation_severity(violation_type):
        """Get severity level for violation"""
        return ViolationDetector.SEVERITY_MAP.get(violation_type, 'medium')
    
    @staticmethod
    def get_trust_score_reduction(violation_type):
        """Get trust score reduction for violation"""
        severity = ViolationDetector.get_violation_severity(violation_type)
        
        reduction_map = {
            'low': 5,
            'medium': 10,
            'high': 20
        }
        
        return reduction_map.get(severity, 10)
    
    @staticmethod
    def analyze_violation_pattern(violations):
        """Analyze violation pattern"""
        if not violations:
            return {
                'total_violations': 0,
                'violation_types': {},
                'severity_distribution': {},
                'average_trust_score_loss': 0,
                'is_suspicious': False,
                'risk_level': 'low'
            }
        
        analysis = {
            'total_violations': len(violations),
            'violation_types': defaultdict(int),
            'severity_distribution': defaultdict(int),
            'average_trust_score_loss': 0,
            'is_suspicious': False,
            'risk_level': 'low'
        }
        
        total_reduction = 0
        
        for violation in violations:
            analysis['violation_types'][violation.violation_type] += 1
            analysis['severity_distribution'][violation.severity] += 1
            total_reduction += violation.trust_score_reduction
        
        analysis['average_trust_score_loss'] = (
            total_reduction / len(violations) if violations else 0
        )
        
        # Determine if suspicious
        high_severity_count = analysis['severity_distribution'].get('high', 0)
        if high_severity_count >= 3 or len(violations) >= 5:
            analysis['is_suspicious'] = True
        
        # Determine risk level
        if len(violations) >= 5 or analysis['average_trust_score_loss'] >= 15:
            analysis['risk_level'] = 'high'
        elif len(violations) >= 3 or analysis['average_trust_score_loss'] >= 10:
            analysis['risk_level'] = 'medium'
        else:
            analysis['risk_level'] = 'low'
        
        return analysis
    
    @staticmethod
    def get_violation_recommendations(analysis):
        """Get recommendations based on violation analysis"""
        recommendations = []
        
        if analysis['is_suspicious']:
            recommendations.append("🚨 Suspicious behavior detected. Monitor closely.")
        
        if analysis['risk_level'] == 'high':
            recommendations.append("⚠️ High risk level. Consider additional proctoring measures.")
        
        if analysis['violation_types'].get('phone_detected', 0) >= 2:
            recommendations.append("📱 Multiple phone detections. Verify student identity.")
        
        if analysis['violation_types'].get('multiple_persons', 0) >= 1:
            recommendations.append("👥 Multiple persons detected. Verify exam environment.")
        
        if analysis['violation_types'].get('tab_switch', 0) >= 3:
            recommendations.append("📑 Frequent tab switching. Possible resource checking.")
        
        return recommendations

violation_detector = ViolationDetector()