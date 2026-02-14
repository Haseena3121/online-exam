class NotificationService {
  constructor() {
    this.notifications = [];
  }

  // Show notification
  show(message, type = 'info', duration = 3000) {
    const id = Date.now();
    const notification = {
      id,
      message,
      type, // 'info', 'success', 'warning', 'error'
      duration
    };

    this.notifications.push(notification);

    if (duration > 0) {
      setTimeout(() => {
        this.remove(id);
      }, duration);
    }

    return id;
  }

  // Remove notification
  remove(id) {
    this.notifications = this.notifications.filter(n => n.id !== id);
  }

  // Get all notifications
  getAll() {
    return this.notifications;
  }

  // Convenience methods
  success(message, duration) {
    return this.show(message, 'success', duration);
  }

  error(message, duration) {
    return this.show(message, 'error', duration);
  }

  warning(message, duration) {
    return this.show(message, 'warning', duration);
  }

  info(message, duration) {
    return this.show(message, 'info', duration);
  }
}

export default new NotificationService();