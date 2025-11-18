"""
Twilio integration for SMS and voice communications.
"""

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from typing import Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class TwilioClient:
    """
    Twilio client for SMS and voice communications.
    """

    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.from_phone = settings.TWILIO_PHONE_NUMBER

        if not all([self.account_sid, self.auth_token, self.from_phone]):
            logger.warning("Twilio credentials not fully configured - SMS/voice will not work")
            self.client = None
        else:
            self.client = Client(self.account_sid, self.auth_token)
            logger.info("Twilio client initialized successfully")

    def send_sms(
        self,
        to_phone: str,
        message: str,
        from_phone: Optional[str] = None
    ) -> Optional[str]:
        """
        Send an SMS message.

        Args:
            to_phone: Recipient phone number (E.164 format: +1234567890)
            message: Message text (max 1600 characters)
            from_phone: Sender phone number (defaults to configured number)

        Returns:
            Message SID if successful, None otherwise
        """
        if not self.client:
            logger.error("Twilio client not initialized - cannot send SMS")
            return None

        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=from_phone or self.from_phone,
                to=to_phone
            )

            logger.info(f"SMS sent successfully to {to_phone}: {message_obj.sid}")
            return message_obj.sid

        except TwilioRestException as e:
            logger.error(f"Failed to send SMS to {to_phone}: {e}")
            return None

    def send_bulk_sms(
        self,
        phone_numbers: list[str],
        message: str
    ) -> dict[str, Optional[str]]:
        """
        Send SMS to multiple recipients.

        Args:
            phone_numbers: List of phone numbers
            message: Message text

        Returns:
            Dictionary mapping phone numbers to message SIDs
        """
        results = {}

        for phone in phone_numbers:
            sid = self.send_sms(phone, message)
            results[phone] = sid

        successful = sum(1 for sid in results.values() if sid is not None)
        logger.info(f"Bulk SMS sent: {successful}/{len(phone_numbers)} successful")

        return results

    def send_whatsapp(
        self,
        to_phone: str,
        message: str
    ) -> Optional[str]:
        """
        Send a WhatsApp message via Twilio.

        Args:
            to_phone: Recipient phone number (E.164 format)
            message: Message text

        Returns:
            Message SID if successful, None otherwise
        """
        if not self.client:
            logger.error("Twilio client not initialized - cannot send WhatsApp")
            return None

        try:
            # WhatsApp messages use "whatsapp:" prefix
            message_obj = self.client.messages.create(
                body=message,
                from_=f"whatsapp:{self.from_phone}",
                to=f"whatsapp:{to_phone}"
            )

            logger.info(f"WhatsApp message sent successfully to {to_phone}: {message_obj.sid}")
            return message_obj.sid

        except TwilioRestException as e:
            logger.error(f"Failed to send WhatsApp to {to_phone}: {e}")
            return None

    def make_call(
        self,
        to_phone: str,
        twiml_url: str,
        from_phone: Optional[str] = None
    ) -> Optional[str]:
        """
        Make a voice call.

        Args:
            to_phone: Recipient phone number
            twiml_url: URL that returns TwiML instructions
            from_phone: Caller phone number (defaults to configured number)

        Returns:
            Call SID if successful, None otherwise
        """
        if not self.client:
            logger.error("Twilio client not initialized - cannot make call")
            return None

        try:
            call = self.client.calls.create(
                twiml=twiml_url,
                to=to_phone,
                from_=from_phone or self.from_phone
            )

            logger.info(f"Call initiated to {to_phone}: {call.sid}")
            return call.sid

        except TwilioRestException as e:
            logger.error(f"Failed to make call to {to_phone}: {e}")
            return None

    def get_message_status(self, message_sid: str) -> Optional[str]:
        """
        Get the status of a sent message.

        Args:
            message_sid: Message SID

        Returns:
            Message status or None if failed
        """
        if not self.client:
            return None

        try:
            message = self.client.messages(message_sid).fetch()
            return message.status
        except TwilioRestException as e:
            logger.error(f"Failed to get message status for {message_sid}: {e}")
            return None


# Global Twilio client instance
twilio_client = TwilioClient()
