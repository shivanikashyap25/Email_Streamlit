import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

# Function to extract name from email
def extract_name(email):
    username = email.split('@')[0]  # Extract part before '@'
    # Remove numbers and special characters
    name = re.sub(r'[^a-zA-Z]', '', username)
    return name.capitalize()  # Capitalize the name

# Function to send personalized emails
def send_email(to_emails, subject, message_body, from_email, app_password):
    try:
        # SMTP server setup (using Gmail's SMTP server as an example)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, app_password)

        # Send email to each recipient
        for email in to_emails:
            name = extract_name(email)
            personalized_message = f"Hey {name},\n\n{message_body}"

            # Create email content
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(personalized_message, 'plain'))

            server.send_message(msg)

        server.quit()
        return "Emails sent successfully!"
    except smtplib.SMTPAuthenticationError:
        return "Authentication failed. Please check your email address and App Password."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit application
def main():
    st.title("Personalized Bulk Email Sender App 📧")

    # Input fields for email details
    to_emails = st.text_area("Recipient Email Addresses (separate by commas)").strip()
    subject = st.text_input("Email Subject")
    message_body = st.text_area("Email Message Body")
    from_email = st.text_input("Your Email Address", type="password")
    app_password = st.text_input("Your App Password", type="password")

    # Send email button
    if st.button("Send Email"):
        if to_emails and subject and message_body and from_email and app_password:
            # Split and clean recipient emails
            email_list = [email.strip() for email in to_emails.split(",") if email.strip()]
            if len(email_list) > 0:
                status = send_email(email_list, subject, message_body, from_email, app_password)
                if "successfully" in str(status):
                    st.success(str(status))
                else:
                    st.error(str(status))
            else:
                st.error("No valid email addresses provided.")
        else:
            st.error("Please fill in all the fields before sending the emails.")

if __name__ == "__main__":
    main()
