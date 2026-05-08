"""
Application entry point
"""
import os
from app import create_app, db

def main():
    """Main entry point"""
    app = create_app()
    
    with app.app_context():
        db.create_all()
    
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"\n{'='*50}")
    print(f"* Online Exam Proctoring System")
    print(f"{'='*50}")
    print(f"Server running at http://localhost:{port}")
    print(f"Debug mode: {debug}")
    print(f"{'='*50}\n")
    
    import threading
    import time
    from cleanup_evidence import cleanup_old_evidence

    def background_cleanup():
        while True:
            try:
                print("* Running automatic evidence cleanup job...")
                cleanup_old_evidence()
            except Exception as e:
                print(f"Cleanup error: {e}")
            time.sleep(6 * 3600)  # Sleep 6 hours

    cleanup_thread = threading.Thread(target=background_cleanup, daemon=True)
    cleanup_thread.start()

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )

if __name__ == '__main__':
    main()