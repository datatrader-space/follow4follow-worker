import imaplib
import logging
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
import json
import mailparser
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
# Assuming these are your custom exceptions
class EmailClientException(Exception):
    """Base exception for email client operations."""
    pass
class ClientDisconnectedException(EmailClientException):
    """Raised when the client is unexpectedly disconnected."""
    pass
class BaseEmailClient:
    """
    A base class for interacting with IMAP email accounts.
    Handles connection, disconnection, and basic email fetching.
    Subclasses should implement service-specific logic for search and extraction.
    """
    def __init__(self,
                #  email_address: str,
                 imap_email_host: str,
                 imap_email_username: str,
                 imap_email_password: str,
                 imap_email_port: int = 993,  # Default IMAPS port
                 logger: Optional[logging.Logger] = None):
        # self.email_address = email_address
        self.imap_email_username = imap_email_username
        self.imap_email_host = imap_email_host
        self.imap_email_password = imap_email_password
        self.imap_email_port = imap_email_port
        self.log = logger if logger else logging.getLogger(__name__)
        self._connection: Optional[imaplib.IMAP4_SSL] = None
        self._seen_uids: set = set()  # To keep track of processed email UIDs
    @property
    def connection(self) -> imaplib.IMAP4_SSL:
        """Provides the IMAP connection object."""
        if not self._connection or self._connection.state != 'SELECTED':
            self.connect() # Attempt to reconnect if not connected or selected
        return self._connection
    def connect(self) -> imaplib.IMAP4_SSL:
        """
        Establishes an SSL IMAP connection to the email server.
        Raises EmailClientException if connection fails.
        """
        try:
            if getattr(self, '_connected', False):
              return  # already connected, skip reconnecting
            self._connection = imaplib.IMAP4_SSL(self.imap_email_host, self.imap_email_port)
            self._connection.login(self.imap_email_username, self.imap_email_password)
            self.log.info(f"Successfully connected to IMAP server: {self.imap_email_host}")
            print("connected!!")
            return self._connection
        except Exception as error:
            self.log.exception(f"Failed to connect to IMAP server: {error}")
            raise EmailClientException(f"IMAP connection failed: {error}") from error
    def disconnect(self):
        """Closes the IMAP connection."""
        if self._connection:
            try:
                if self._connection.state in ["SELECTED"]:
                    self._connection.close()
                self._connection.logout()
                self.log.info("Disconnected from IMAP server.")
            except Exception as error:
                self.log.error(f"Error during IMAP disconnect: {error}")
            finally:
                self._connection = None
    def select_inbox(self):
        """Selects the INBOX folder."""
        try:
            status, _ = self.connection.select('INBOX')
            if status != 'OK':
                raise EmailClientException(f"Failed to select INBOX: {status}")
            self.log.debug("INBOX selected.")
        except (imaplib.IMAP4.error, imaplib.IMAP4.abort) as e:
            self.log.exception("IMAP error selecting INBOX, attempting reconnect.")
            self.disconnect()
            raise ClientDisconnectedException("IMAP client disconnected during INBOX selection.") from e
    def _fetch_email_data(self, uid: str) -> Optional[bytes]:
        """
        Fetches the raw email data for a given UID.
        """
        try:
            # Ensure connection is fresh and mailbox is selected before fetching a specific UID
            # This can help if the connection implicitly dropped or mailbox got deselected
            self.connection.noop() # Send a NOOP command to keep connection alive and check status
            self.connection.select('INBOX') # Re-select inbox just in case
            status, msg_data = self.connection.uid('fetch', uid, '(RFC822)') # Use UID fetch directly
            if status == 'OK' and msg_data and msg_data[0]:
                # Ensure it's not a 'NIL' response, which means UID not found
                if isinstance(msg_data[0], tuple) and len(msg_data[0]) > 1:
                    return msg_data[0][1]
                else:
                    self.log.warning(f"Fetch for UID {uid} returned no data or an unexpected format: {msg_data}")
                    return None
            else:
                self.log.warning(f"Failed to fetch email UID {uid}: Status={status}, Data={msg_data}")
                return None
        except (imaplib.IMAP4.error, imaplib.IMAP4.abort) as e:
            # Log the specific UID that caused the issue
            self.log.exception(f"IMAP error fetching email UID {uid}. Attempting reconnect if client disconnected.")
            self.disconnect() # Disconnect to force a full reconnect
            # Re-raise to signal a more critical connection issue
            raise ClientDisconnectedException(f"IMAP client disconnected while fetching email UID {uid}.") from e
        except Exception as e:
            self.log.error(f"Unexpected error fetching email UID {uid}: {e}")
            return None
    def search_emails(self, criteria: str) -> List[str]:
        """
        Searches the currently selected mailbox for emails matching the criteria.
        Returns a list of email UIDs.
        """
        try:
            status, data = self.connection.uid('search', None, criteria)
            if status == 'OK':
                uids = data[0].split()
                self.log.debug(f"Found {len(uids)} emails matching criteria: {criteria}")
                return [uid.decode('utf-8') for uid in uids]
            else:
                self.log.warning(f"IMAP search failed with status: {status}")
                return []
        except (imaplib.IMAP4.error, imaplib.IMAP4.abort) as e:
            self.log.exception("IMAP error during search, attempting reconnect.")
            self.disconnect()
            raise ClientDisconnectedException("IMAP client disconnected during search.") from e
        except Exception as e:
            self.log.error(f"Unexpected error during IMAP search: {e}")
            return []
    def get_new_emails(self, search_criteria: str) -> List[mailparser.MailParser]:
        """
        Fetches and parses new emails based on search criteria.
        Keeps track of already processed UIDs to avoid reprocessing.
        """
        self.select_inbox()
        all_uids = self.search_emails(search_criteria)
        new_uids = [uid for uid in all_uids if uid not in self._seen_uids]
        parsed_emails = []
        for uid in new_uids:
            raw_email = self._fetch_email_data(uid)
            if raw_email:
                try:
                    parsed_email = mailparser.parse_from_bytes(raw_email)
                    parsed_emails.append(parsed_email)
                    self._seen_uids.add(uid)  # Mark as seen after successful parsing
                except Exception as e:
                    self.log.error(f"Error parsing email UID {uid}: {e}")
        if new_uids:
            try:
                self.connection.expunge() # Remove deleted messages permanently
            except (imaplib.IMAP4.error, imaplib.IMAP4.abort) as e:
                self.log.warning(f"Error during expunge: {e}")
                self.disconnect() # Disconnect on expunge error as state might be bad
        return parsed_emails
    def extract_from_email(self, parsed_email: mailparser.MailParser, case: str, service: Optional[str] = None) -> Optional[str]:
        """
        Placeholder for extracting specific information from a parsed email.
        This method should be overridden by subclasses or handled by a separate parser.
        """
        raise NotImplementedError("Subclasses must implement extract_from_email method.")
    def extract_code_from_subject(subject: str) -> str:
        if not subject:
            return None
        pattern = r'confirmation code is (\w+)'  # Adjust if needed
        match = re.search(pattern, subject)
        if match:
            return match.group(1)
        return None
    def get_data_from_emails(self, search_criteria: str, case: str, service: Optional[str] = None) -> List[Tuple[str, datetime]]:
        """
        Combines fetching new emails with extraction.
        Returns a list of (extracted_data, email_datetime) tuples.
        """
        print("request comming")
        new_emails = self.get_new_emails(search_criteria)
        print(new_emails)
        extracted_data_list = []
        EMAILS_DATA = []
        for email in new_emails:
            email_dict = {
                # 'body': email.text_plain[0] if email.text_plain else None,
                'datetime': email.date,  # datetime object
                'headers': json.loads(email.headers_json)
            }
            EMAILS_DATA.append(email_dict)
        # Find the latest email by datetime
        latest_email = max(EMAILS_DATA, key=lambda x: x['datetime'])
        # Print subject and datetime of the latest email
        subject = latest_email['headers'].get('Subject')
        code = None
        if subject:
            match = re.search(r'confirmation code is (\w+)', subject)
            if match:
                code = match.group(1)
        dt_str = latest_email['datetime'].strftime('%Y-%m-%d %H:%M:%S %Z')
        return [(latest_email['headers'].get('Subject'), dt_str,latest_email['headers']['To'][0][1],code)]
        # Apply sorting if requested
        # for email in new_emails:
        #     EMAILS_DATA.append({'body':email.body,'datetime':email.date_json,'headers':json.loads(email.headers_json)})
        #     print(EMAILS_DATA)
        # return EMAILS_DATA
# # 1. Instantiate the BaseEmailClient
# b = BaseEmailClient(
#     imap_email_host='mail.privateemail.com',
#     imap_email_username='noreply@datatrader.space',
#     imap_email_password='robocop@123',
#     imap_email_port=993
# )
# try:
#     # 2. Connect to the email server
#     b.connect()
#     # 3. Define your search criteria
#     # Examples:
#     # search_criteria = "UNSEEN"  # Get all unread emails
#     # search_criteria = 'FROM "support@example.com"' # Emails from a specific sender
#     # search_criteria = 'SUBJECT "Order Confirmation" SINCE 20-Jul-2025' # Subject and date
#     search_criteria = 'FROM "INFO@X.com"' # Get all emails (be careful with large mailboxes)
#     # 4. Define the 'case' for extraction
#     # This corresponds to what you want to extract using the extract_from_email method.
#     # Based on the placeholder implementation, valid cases could be: "subject", "body", "html", "from"
#     extraction_case = "Your X confirmation code"
#     # extraction_case = "body"
#     # extraction_case = "from"
#     # 5. Call get_data_from_emails
#     extracted_email_data = b.get_data_from_emails(search_criteria, extraction_case)
#     print(extracted_email_data)
#     # 6. Process the extracted data
# except EmailClientException as e:
#     print(f"An email client error occurred: {e}")
# except ClientDisconnectedException as e:
#     print(f"The client disconnected: {e}")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")
# finally:
#     # 7. Disconnect when done (important for clean exit)
#     b.disconnect()