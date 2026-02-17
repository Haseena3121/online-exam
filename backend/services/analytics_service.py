"""
Analytics and reporting service
"""
import logging
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Generate analytics and reports"""
    
    @staticmethod
    def get_exam_analytics(exam_id):
        """Get analytics for exam"""
        from models import ExamResult, ViolationLog, ExamEnrollment
        
        try:
            enrollments = ExamEnrollment.query.filter_by(exam_id=exam_id).all()
            results = ExamResult.query.filter_by(exam_id=exam_id).all()
            violations = ViolationLog.query.filter_by(exam_id=exam_id).all()
            
            if not results:
                return {
                    'total_students': len(enrollments),
                    'submitted': 0,
                    'passed': 0,
                    'failed': 0,
                    'average_score': 0,
                    'highest_score': 0,
                    'lowest_score': 0,
                    'total_violations': 0,
                    'average_violations_per_student': 0
                }
            
            passed = len([r for r in results if r.status == 'pass'])
            failed = len([r for r in results if r.status == 'fail'])
            
            scores = [r.percentage for r in results if r.percentage is not None]
            
            analytics = {
                'total_students': len(enrollments),
                'submitted': len(results),
                'passed': passed,
                'failed': failed,
                'average_score': sum(scores) / len(scores) if scores else 0,
                'highest_score': max(scores) if scores else 0,
                'lowest_score': min(scores) if scores else 0,
                'total_violations': len(violations),
                'average_violations_per_student': len(violations) / len(results) if results else 0
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting exam analytics: {str(e)}")
            return {}
    
    @staticmethod
    def get_student_analytics(student_id):
        """Get analytics for student"""
        from models import ExamResult, ViolationLog
        
        try:
            results = ExamResult.query.filter_by(student_id=student_id).all()
            violations = ViolationLog.query.filter_by(student_id=student_id).all()
            
            if not results:
                return {
                    'total_exams': 0,
                    'passed': 0,
                    'failed': 0,
                    'average_score': 0,
                    'total_violations': 0,
                    'average_trust_score': 100
                }
            
            passed = len([r for r in results if r.status == 'pass'])
            failed = len([r for r in results if r.status == 'fail'])
            
            scores = [r.percentage for r in results if r.percentage is not None]
            trust_scores = [r.final_trust_score for r in results if r.final_trust_score is not None]
            
            analytics = {
                'total_exams': len(results),
                'passed': passed,
                'failed': failed,
                'average_score': sum(scores) / len(scores) if scores else 0,
                'total_violations': len(violations),
                'average_trust_score': sum(trust_scores) / len(trust_scores) if trust_scores else 100,
                'highest_score': max(scores) if scores else 0,
                'lowest_score': min(scores) if scores else 0
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting student analytics: {str(e)}")
            return {}
    
    @staticmethod
    def get_examiner_analytics(examiner_id):
        """Get analytics for examiner"""
        from models import Exam, ExamEnrollment, ExamResult, ViolationLog
        
        try:
            exams = Exam.query.filter_by(examiner_id=examiner_id).all()
            
            total_students = 0
            total_results = 0
            total_violations = 0
            
            for exam in exams:
                total_students += len(exam.enrollments)
                total_results += len(exam.results)
                total_violations += len(exam.violations)
            
            analytics = {
                'total_exams': len(exams),
                'published_exams': len([e for e in exams if e.is_published]),
                'total_students': total_students,
                'total_submissions': total_results,
                'total_violations': total_violations
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting examiner analytics: {str(e)}")
            return {}
    
    @staticmethod
    def generate_report(exam_id, format='json'):
        """Generate exam report"""
        from models import ExamResult, ViolationLog, Exam
        
        try:
            exam = Exam.query.get(exam_id)
            if not exam:
                return None
            
            results = ExamResult.query.filter_by(exam_id=exam_id).all()
            violations = ViolationLog.query.filter_by(exam_id=exam_id).all()
            
            report = {
                'exam': exam.to_dict(),
                'analytics': AnalyticsService.get_exam_analytics(exam_id),
                'results': [r.to_dict() for r in results],
                'violations_summary': {
                    'total': len(violations),
                    'by_type': {},
                    'by_severity': {}
                },
                'generated_at': datetime.utcnow().isoformat()
            }
            
            for violation in violations:
                if violation.violation_type not in report['violations_summary']['by_type']:
                    report['violations_summary']['by_type'][violation.violation_type] = 0
                report['violations_summary']['by_type'][violation.violation_type] += 1
                
                if violation.severity not in report['violations_summary']['by_severity']:
                    report['violations_summary']['by_severity'][violation.severity] = 0
                report['violations_summary']['by_severity'][violation.severity] += 1
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return None

analytics_service = AnalyticsService()