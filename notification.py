from plyer import notification

def notify_user(title: str, message: str, duration: int = 5):
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=duration,
            app_icon="logo.ico"
        )
    except Exception as e:
        print(f"Notification error: {e}")