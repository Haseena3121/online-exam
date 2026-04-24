from app import create_app
app = create_app()
with app.app_context():
    from database import db
    from sqlalchemy import text
    with db.engine.connect() as conn:
        cols = [
            'ALTER TABLE session_analytics ADD COLUMN student_id INT NULL',
            'ALTER TABLE session_analytics ADD COLUMN exam_id INT NULL',
            'ALTER TABLE session_analytics ADD COLUMN eye_gaze_warnings INT DEFAULT 0',
            'ALTER TABLE session_analytics ADD COLUMN phone_detection_count INT DEFAULT 0',
            'ALTER TABLE session_analytics ADD COLUMN tab_switch_count INT DEFAULT 0',
            'ALTER TABLE session_analytics ADD COLUMN sound_detection_count INT DEFAULT 0',
            'ALTER TABLE session_analytics ADD COLUMN multiple_persons_detected INT DEFAULT 0',
            'ALTER TABLE session_analytics ADD COLUMN blur_exit_attempts INT DEFAULT 0',
            'ALTER TABLE session_analytics ADD COLUMN face_not_visible_count INT DEFAULT 0',
            'ALTER TABLE session_analytics ADD COLUMN head_movement_warnings INT DEFAULT 0',
            'ALTER TABLE session_analytics ADD COLUMN total_violations INT DEFAULT 0',
        ]
        for col in cols:
            try:
                conn.execute(text(col))
                name = col.split('ADD COLUMN ')[1].split(' ')[0]
                print('OK: ' + name)
            except Exception as e:
                print('Skip: ' + str(e)[:80])
        conn.commit()
    print('Done')
