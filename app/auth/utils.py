from flask_mail import Message
from app import mail
from flask import url_for, current_app

def send_verification_email(user):
    token = user.get_reset_token()
    msg = Message('Email Verification', sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f'''Dear {user.username},

Thank you for registering at Enhancing Lettuce Crop Management. To complete your registration and verify your email address, please click the link below:

{url_for('auth.verify_email', token=token, _external=True)}

If you did not register on our website, please ignore this email and no changes will be made.

This link will expire in 30 minutes for your security.

Best regards,
The Enhancing Lettuce Crop Management Team
'''
    mail.send(msg)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    msg.body = f'''Dear {user.username},

To reset your password for your Enhancing Lettuce Crop Management account, please click the link below:

{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email and no changes will be made.

This link will expire in 30 minutes for your security.

Best regards,
The Enhancing Lettuce Crop Management Team
'''
    mail.send(msg)
