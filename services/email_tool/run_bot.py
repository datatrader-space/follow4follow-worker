from services.email_tool.endpoints import BaseEmailClient
import re

class InstagramEmailFetcher:
    def __init__(self, profile):
        self.profile = profile
        self.client = BaseEmailClient(
            imap_email_host=profile.imap_email_host,
            imap_email_username=profile.imap_email_username,
            imap_email_password=profile.imap_email_password,
            imap_email_port=profile.imap_email_port,
        )

    def fetch_instagram_code(self):
        """
        Connect to the IMAP inbox and extract the latest Instagram confirmation code.
        Returns the 6-digit code as a string, or None if not found.
        """
        try:
            self.client.connect()

            # Instagram usually sends from this address
            extracted_data = self.client.get_data_from_emails(
                search_criteria='FROM "security@mail.instagram.com"',
                extraction_case="is your Instagram code"
            )

            if not extracted_data:
                print("[!] No confirmation email found.")
                return None

            # Combine email parts into one string
            email_body = " ".join(str(part) for part in extracted_data[0])

            # Look for a 6-digit code in the text
            match = re.search(r"\b(\d{6})\b", email_body)
            if match:
                return match.group(1)

            print("[!] No code found in email body.")
            return None

        except Exception as e:
            print(f"[!] Error while fetching Instagram code: {e}")
            return None

        finally:
            try:
                self.client.disconnect()
            except Exception:
                pass
