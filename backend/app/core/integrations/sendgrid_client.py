"""
SendGrid integration for email communications.
"""

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Personalization
from python_http_client.exceptions import HTTPError
from typing import Optional, List, Dict, Any
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class SendGridClient:
    """
    SendGrid client for transactional and marketing emails.
    """

    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.SENDGRID_FROM_EMAIL

        if not self.api_key:
            logger.warning("SendGrid API key not configured - email sending will not work")
            self.client = None
        else:
            self.client = SendGridAPIClient(self.api_key)
            logger.info("SendGrid client initialized successfully")

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_content: Optional[str] = None,
        from_email: Optional[str] = None,
        reply_to: Optional[str] = None
    ) -> bool:
        """
        Send a single email.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email content
            plain_content: Plain text email content
            from_email: Sender email (defaults to configured email)
            reply_to: Reply-to email address

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.error("SendGrid client not initialized - cannot send email")
            return False

        try:
            message = Mail(
                from_email=from_email or self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content,
                plain_text_content=plain_content
            )

            if reply_to:
                message.reply_to = reply_to

            response = self.client.send(message)

            logger.info(f"Email sent successfully to {to_email}: status {response.status_code}")
            return response.status_code in [200, 201, 202]

        except HTTPError as e:
            logger.error(f"Failed to send email to {to_email}: {e.body}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending email to {to_email}: {e}")
            return False

    def send_template_email(
        self,
        to_email: str,
        template_id: str,
        dynamic_data: Dict[str, Any],
        subject: Optional[str] = None,
        from_email: Optional[str] = None
    ) -> bool:
        """
        Send an email using a SendGrid template.

        Args:
            to_email: Recipient email address
            template_id: SendGrid template ID
            dynamic_data: Dictionary of template variables
            subject: Email subject (if not in template)
            from_email: Sender email (defaults to configured email)

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.error("SendGrid client not initialized - cannot send email")
            return False

        try:
            message = Mail(
                from_email=from_email or self.from_email,
                to_emails=to_email
            )
            message.template_id = template_id

            if subject:
                message.subject = subject

            # Add dynamic template data
            message.dynamic_template_data = dynamic_data

            response = self.client.send(message)

            logger.info(f"Template email sent successfully to {to_email}: status {response.status_code}")
            return response.status_code in [200, 201, 202]

        except HTTPError as e:
            logger.error(f"Failed to send template email to {to_email}: {e.body}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending template email to {to_email}: {e}")
            return False

    def send_bulk_email(
        self,
        recipients: List[Dict[str, str]],
        subject: str,
        html_content: str,
        plain_content: Optional[str] = None,
        from_email: Optional[str] = None
    ) -> bool:
        """
        Send email to multiple recipients.

        Args:
            recipients: List of dictionaries with 'email' and optional 'name'
            subject: Email subject
            html_content: HTML email content
            plain_content: Plain text email content
            from_email: Sender email (defaults to configured email)

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.error("SendGrid client not initialized - cannot send email")
            return False

        try:
            message = Mail(
                from_email=from_email or self.from_email,
                subject=subject,
                html_content=html_content,
                plain_text_content=plain_content
            )

            # Add all recipients
            for recipient in recipients:
                email = recipient.get('email')
                name = recipient.get('name', '')
                message.add_to(To(email, name))

            response = self.client.send(message)

            logger.info(f"Bulk email sent successfully to {len(recipients)} recipients: status {response.status_code}")
            return response.status_code in [200, 201, 202]

        except HTTPError as e:
            logger.error(f"Failed to send bulk email: {e.body}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending bulk email: {e}")
            return False

    def send_transactional_email(
        self,
        to_email: str,
        email_type: str,
        data: Dict[str, Any]
    ) -> bool:
        """
        Send a transactional email based on type.

        Args:
            to_email: Recipient email
            email_type: Type of email (welcome, receipt, password_reset, etc.)
            data: Data to populate the email template

        Returns:
            True if successful, False otherwise
        """
        # Email templates (in production, use SendGrid templates)
        templates = {
            "welcome": {
                "subject": "Welcome to {gym_name}!",
                "html": """
                <h1>Welcome to {gym_name}!</h1>
                <p>Hi {member_name},</p>
                <p>We're excited to have you join our fitness community!</p>
                <p>Your membership starts on {start_date}.</p>
                <p>Best regards,<br>{gym_name} Team</p>
                """
            },
            "payment_receipt": {
                "subject": "Payment Receipt - ${amount}",
                "html": """
                <h1>Payment Received</h1>
                <p>Hi {member_name},</p>
                <p>We've received your payment of ${amount}.</p>
                <p>Invoice: {invoice_number}</p>
                <p>Date: {payment_date}</p>
                <p>Thank you for your payment!</p>
                """
            },
            "payment_failed": {
                "subject": "Payment Failed - Action Required",
                "html": """
                <h1>Payment Failed</h1>
                <p>Hi {member_name},</p>
                <p>We were unable to process your payment of ${amount}.</p>
                <p>Reason: {failure_reason}</p>
                <p>Please update your payment method to continue your membership.</p>
                """
            },
            "membership_expiring": {
                "subject": "Your Membership is Expiring Soon",
                "html": """
                <h1>Membership Expiring</h1>
                <p>Hi {member_name},</p>
                <p>Your membership will expire on {expiry_date}.</p>
                <p>Renew now to keep your membership active!</p>
                <a href="{renewal_link}">Renew Membership</a>
                """
            }
        }

        template = templates.get(email_type)

        if not template:
            logger.error(f"Unknown email type: {email_type}")
            return False

        # Format template with data
        subject = template["subject"].format(**data)
        html_content = template["html"].format(**data)

        return self.send_email(to_email, subject, html_content)


# Global SendGrid client instance
sendgrid_client = SendGridClient()
