from email_validator import validate_email, EmailNotValidError
from flask_mailman  import EmailMessage

def send_email(to : str, subject : str, body_html):
    code = 0
    for i in range(0,3):
        try:
            msg = EmailMessage(
                subject=subject,
                body=body_html, 
                to=[to],        
            )
            msg.content_subtype = 'html'
            
            code = msg.send()
            if not code:
                break 
        except Exception as e:
            code = 0
            print(f"Erro ao tentar enviar email: {e}")
        
    return code


def email_validate (email):
    try:
        email_check = validate_email(email, check_deliverability=True)
        return email_check.normalized
    except EmailNotValidError as e:
        return False