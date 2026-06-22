# app/services/email_service.py
from flask import current_app, render_template, url_for
# import flask_mail ou smtplib aqui se for o caso

def _send_base_email(to : str, subject : str, body_html):
    print(f"Enviando email para: {to}", flush=True)
    print(f"Assunto: {subject}" , flush=True)
    print(f"Corpo do email: {body_html}", flush=True)
    
    
    return "hffff"


def send_password_recovery_email(user_email: str, token: str):
    
    subject = "Recuperação de Senha - Meninas Hub"
    link = f"localhost:5000/{url_for('main.reset_password', token=token)}"
    
    body = render_template("recuperacao_email.html", link=link)
    
    saiddddd = _send_base_email(to=user_email, subject=subject, body_html=body)
    return saiddddd


def send_welcome_email(user_email: str, username: str):
    
    subject = "Bem-vindo ao Meninas Hub!"
    body = render_template("bem_vindo_email.html", username=username)
    
    return _send_base_email(to=user_email, subject=subject, body_html=body)