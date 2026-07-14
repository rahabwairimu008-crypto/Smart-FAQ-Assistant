"""
whatsapp_bot.py
WhatsApp integration for the Smart FAQ Assistant, per the project brief's
"WhatsApp Integration" requirement.

Uses Twilio's WhatsApp Sandbox (free for development/testing) via a
Flask webhook: Twilio forwards incoming WhatsApp messages to this
server as an HTTP POST, and this server replies with TwiML containing
the assistant's answer.

--------------------------------------------------------------------
SETUP (one-time):
--------------------------------------------------------------------
1. Create a free Twilio account: https://www.twilio.com/try-twilio
2. In the Twilio Console, activate the WhatsApp Sandbox
   (Messaging -> Try it out -> Send a WhatsApp message). Twilio gives
   you a sandbox number and a join code, e.g. "join happy-tiger" --
   send that from your own WhatsApp to the sandbox number once to
   link your phone for testing.
3. Run this server:
       python3 whatsapp_bot.py
   By default it listens on http://localhost:5000/whatsapp
4. Twilio needs a PUBLIC url to reach your local server. During
   development, use ngrok (https://ngrok.com/):
       ngrok http 5000
   Copy the https://xxxx.ngrok-free.app URL it gives you.
5. In the Twilio Console -> WhatsApp Sandbox Settings, paste:
       https://xxxx.ngrok-free.app/whatsapp
   into "WHEN A MESSAGE COMES IN", method POST, and save.
6. Message the sandbox number on WhatsApp with any of the 70+
   DeKUT SCIT questions -- you should get an automatic reply.

For a real production deployment (not just the free sandbox), you'd
apply for a proper Twilio WhatsApp Business number, or use Meta's
WhatsApp Cloud API directly -- the Flask route below stays the same
either way, only the provider setup differs.
--------------------------------------------------------------------
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from main import handle_query

app = Flask(__name__)


@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """
    Twilio POSTs incoming WhatsApp messages here as form-encoded data.
    The message text is in the 'Body' field; the sender's WhatsApp
    number is in 'From' (useful for logging who's asking what).
    """
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "unknown")

    print(f"[WhatsApp] {sender} asked: {incoming_msg}")

    if not incoming_msg:
        reply_text = (
            "Hi! Send me a question about DeKUT SCIT -- registration, "
            "fees, exams, attachment, graduation, and more."
        )
    else:
        result = handle_query(incoming_msg)
        reply_text = result["response"]

    twiml = MessagingResponse()
    twiml.message(reply_text)
    return str(twiml)


@app.route("/", methods=["GET"])
def health_check():
    """Simple check that the server is up (visit in a browser)."""
    return "DeKUT SCIT WhatsApp FAQ Assistant is running."


if __name__ == "__main__":
    print("Starting WhatsApp FAQ Assistant server on http://localhost:5000")
    print("Webhook endpoint: http://localhost:5000/whatsapp")
    print("(Expose this publicly with ngrok for Twilio to reach it -- see")
    print(" the setup instructions at the top of this file.)\n")
    app.run(host="0.0.0.0", port=5000, debug=True)