from win10toast import ToastNotifier

def notify_user(
    title: str = "Notification",
    message: str = "Notification body",
    duration: int = 20
):
    toast = ToastNotifier()

    toast.show_toast(
        title,
        message,
        duration = 20,
        icon_path = "logo.ico",
        threaded = True,
    )
    
if __name__ == "__main__":
    notify_user(
        title="Posture Checker",
        message="This is a test notification from Posture Checker.",
        duration=10
    )