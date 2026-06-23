"""Service functions for sending application emails."""

from flask_mailman import EmailMessage


def send_email(to: str, subject: str, body_html: str) -> int:
    """
    Send an HTML email with a limited retry policy.

    The function attempts to send the message up to three times. Sending stops
    immediately after a successful attempt. If an exception occurs or all
    attempts fail, the function returns zero.

    Args:
        to (str): Recipient's email address.
        subject (str): Subject displayed in the email.
        body_html (str): Email body formatted as HTML.

    Returns:
        int: The number of successfully sent messages, or zero when the email
            could not be sent.
    """
    for _ in range(3):
        try:
            msg = EmailMessage(
                subject=subject,
                body=body_html,
                to=[to],
            )
            msg.content_subtype = 'html'
            
            code = msg.send()
            if code:
                break
        except Exception as e:
            code = 0
            print(f"Erro ao tentar enviar email: {e}")
        
    return code
