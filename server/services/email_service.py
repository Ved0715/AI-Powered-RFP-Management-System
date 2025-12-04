import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# Email configuration
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
IMAP_HOST = os.getenv("IMAP_HOST", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(to: str, subject: str, body: str) -> Dict:
    """
    Send email using SMTP
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body (HTML)
    
    Returns:
        dict with success status
    """
    try:
        # Create message
        message = MIMEMultipart('alternative')
        message['From'] = EMAIL_ADDRESS
        message['To'] = to
        message['Subject'] = subject
        
        # Add HTML body
        html_part = MIMEText(body, 'html')
        message.attach(html_part)
        
        # Send via SMTP
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)
        
        return {
            "success": True,
            "to": to
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "to": to
        }


def send_rfp_email(vendor_email: str, vendor_name: str, rfp_data: Dict) -> Dict:
    """
    Send RFP to a vendor with formatted content
    
    Args:
        vendor_email: Vendor's email address
        vendor_name: Vendor's name
        rfp_data: RFP information (title, description, requirements, etc.)
    
    Returns:
        dict with send status
    """
    
    # Format requirements as HTML list
    requirements_html = ""
    if rfp_data.get('requirements'):
        requirements_html = "<ul>"
        for req in rfp_data['requirements']:
            requirements_html += f"<li>{req}</li>"
        requirements_html += "</ul>"
    
    # Create email body
    subject = f"RFP: {rfp_data.get('title', 'Untitled')}"
    
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb;">Request for Proposal</h2>
            
            <p>Dear {vendor_name},</p>
            
            <p>We would like to invite you to submit a proposal for the following requirement:</p>
            
            <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #1f2937;">Project: {rfp_data.get('title')}</h3>
                <p><strong>Description:</strong> {rfp_data.get('description')}</p>
                
                {f'<p><strong>Budget:</strong> ${rfp_data.get("budget"):,.2f}</p>' if rfp_data.get('budget') else ''}
                {f'<p><strong>Deadline:</strong> {rfp_data.get("deadline")}</p>' if rfp_data.get('deadline') else ''}
                {f'<p><strong>Payment Terms:</strong> {rfp_data.get("payment_terms")}</p>' if rfp_data.get('payment_terms') else ''}
                {f'<p><strong>Warranty:</strong> {rfp_data.get("warranty_terms")}</p>' if rfp_data.get('warranty_terms') else ''}
                
                {f'<div><strong>Requirements:</strong>{requirements_html}</div>' if requirements_html else ''}
            </div>
            
            <p>Please submit your proposal including:</p>
            <ul>
                <li>Detailed pricing breakdown</li>
                <li>Delivery timeline</li>
                <li>Terms and conditions</li>
                <li>Any relevant certifications or warranties</li>
            </ul>
            
            <p>We look forward to receiving your proposal.</p>
            
            <p>Best regards,<br>
            Procurement Team</p>
        </div>
    </body>
    </html>
    """
    
    return send_email(vendor_email, subject, body)


def get_unread_emails(vendor_emails: List[str] = None, max_results: int = 10) -> List[Dict]:
    """
    Fetch unread emails from vendors using IMAP
    
    Args:
        vendor_emails: List of vendor email addresses to filter by
        max_results: Maximum number of emails to fetch
    
    Returns:
        List of email data
    """
    try:
        # Connect to IMAP
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select('inbox')
        
        # Search for unread emails
        search_criteria = 'UNSEEN'
        
        # If vendor emails provided, filter by sender
        if vendor_emails:
            vendor_search = ' OR '.join([f'FROM "{email}"' for email in vendor_emails])
            search_criteria = f'({search_criteria} ({vendor_search}))'
        
        _, message_numbers = mail.search(None, search_criteria)
        
        emails = []
        for num in message_numbers[0].split()[:max_results]:
            _, msg_data = mail.fetch(num, '(RFC822)')
            
            email_body = msg_data[0][1]
            email_message = email.message_from_bytes(email_body)
            
            # Extract email details
            subject = email_message['subject']
            sender = email_message['from']
            
            # Get email body
            body = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
                    elif part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True).decode()
            else:
                body = email_message.get_payload(decode=True).decode()
            
            emails.append({
                "id": num.decode(),
                "subject": subject,
                "from": sender,
                "body": body,
                "snippet": body[:200] if body else ""
            })
        
        mail.close()
        mail.logout()
        
        return emails
        
    except Exception as e:
        print(f"Error fetching emails: {str(e)}")
        return []


def mark_email_as_read(message_id: str) -> bool:
    """Mark an email as read using IMAP"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select('inbox')
        
        # Mark as seen
        mail.store(message_id.encode(), '+FLAGS', '\\Seen')
        
        mail.close()
        mail.logout()
        
        return True
    except Exception as e:
        print(f"Error marking email as read: {str(e)}")
        return False