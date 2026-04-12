# ─── ADD THIS IMPORT at the top of commands.py ───────────────────────────────
# import messaging


# ─── ADD THESE COMMAND BLOCKS inside the run_command() if/elif chain ──────────
# Place them before the "# ── AI FALLBACK" block


        # ── EMAIL ────────────────────────────────────────────
        # Usage: "email to john@gmail.com subject Hello body How are you?"
        elif command.startswith("email ") or command.startswith("send email "):
            command_type = "messaging"
            raw = command.replace("send email ", "").replace("email ", "")

            # Parse: "to <address> subject <subject> body <body>"
            to_match = re.search(r"to\s+([\w.\-+@]+)", raw)
            subject_match = re.search(r"subject\s+(.+?)(?:\s+body\s+|$)", raw)
            body_match = re.search(r"body\s+(.+)", raw, re.DOTALL)

            if not to_match:
                response = (
                    "Usage: email to <address> subject <subject> body <message>\n"
                    "Example: email to lucy@gmail.com subject Hello body Hope you're well!"
                )
            else:
                to = to_match.group(1)
                subject = subject_match.group(1).strip() if subject_match else "Message from JARVIS"
                body = body_match.group(1).strip() if body_match else raw
                response = messaging.send_email(to, subject, body)


        # ── WHATSAPP ─────────────────────────────────────────
        # Usage: "whatsapp +254712345678 Hey how are you"
        elif command.startswith("whatsapp ") or command.startswith("send whatsapp "):
            command_type = "messaging"
            raw = command.replace("send whatsapp ", "").replace("whatsapp ", "").strip()

            # First token = phone number, rest = message
            parts = raw.split(" ", 1)
            if len(parts) < 2:
                response = (
                    "Usage: whatsapp <number> <message>\n"
                    "Example: whatsapp +254712345678 Hey, are you free tonight?"
                )
            else:
                number = parts[0].strip()
                message = parts[1].strip()
                response = messaging.send_whatsapp(number, message)


        # ── INSTAGRAM DM ─────────────────────────────────────
        # Usage: "instagram @username Hey there!"
        elif command.startswith("instagram ") or command.startswith("dm "):
            command_type = "messaging"
            raw = command.replace("instagram ", "").replace("dm ", "").strip()

            # First token = username, rest = message
            parts = raw.split(" ", 1)
            if len(parts) < 2:
                response = (
                    "Usage: instagram @username <message>\n"
                    "Example: instagram johndoe Hey, check this out!"
                )
            else:
                username = parts[0].replace("@", "").strip()
                message = parts[1].strip()
                response = messaging.send_instagram_dm(username, message)


# ─── ADD THESE TO THE HELP COMMAND ───────────────────────────────────────────
# Inside the help elif block, add this section:

"""
MESSAGING:
  email to [address] subject [subject] body [message]
  whatsapp [+number] [message]   — Send WhatsApp (needs Twilio sandbox)
  instagram [@user] [message]    — Send Instagram DM (opens browser)
  dm [@user] [message]           — Same as instagram
"""