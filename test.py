import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def send_attendance_email(teacher_email, attendance_file):
    # Gmail sender details
    sender_email = "yogeshsoni230305@gmail.com"    # Replace with your Gmail address
    password = "lvlz wzwi mrbb vqoe"         # Replace with your 16-character App Password
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    subject = f"Attendance Report - {current_date}"
    body = f"""
    Dear Teacher,
    
    Please find attached the attendance report for {current_date}. 
    The file contains student names and their attendance timestamps as recorded 
    by the facial recognition system.
    
    Regards,
    Attendance System
    {sender_email}
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = teacher_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with open(attendance_file, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename=attendance_{current_date}.txt'
            )
            msg.attach(part)
    except FileNotFoundError:
        print(f"Attendance file not found: {attendance_file}")
        return
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable TLS
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print(f"Attendance email sent successfully to {teacher_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    teacher_email = "yogeshsoni233005@gmail.com"          # Replace with teacher's email
    attendance_file = "G:/attendance_sys-main/attendance_2025-04-08.txt"
    send_attendance_email(teacher_email, attendance_file)