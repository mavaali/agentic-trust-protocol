"""Tool definitions for the naive ReAct agent."""

from __future__ import annotations

from typing import Any

from src.mock_email.backend import EmailBackend

# Anthropic tool-use schema definitions
TOOL_DEFINITIONS = [
    {
        "name": "read_email",
        "description": "Read a specific email by its ID. Returns the full email content.",
        "input_schema": {
            "type": "object",
            "properties": {
                "email_id": {"type": "string", "description": "The email ID to read"},
            },
            "required": ["email_id"],
        },
    },
    {
        "name": "list_inbox",
        "description": "List all emails in the inbox. Returns summaries of each email.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "list_unread",
        "description": "List unread emails in the inbox.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "search_inbox",
        "description": "Search emails by keyword in subject or body.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "send_email",
        "description": "Send an email to one or more recipients.",
        "input_schema": {
            "type": "object",
            "properties": {
                "recipients": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of recipient email addresses",
                },
                "subject": {"type": "string", "description": "Email subject"},
                "body": {"type": "string", "description": "Email body"},
                "cc": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "CC recipients",
                },
                "reply_to_id": {
                    "type": "string",
                    "description": "ID of email being replied to",
                },
            },
            "required": ["recipients", "subject", "body"],
        },
    },
    {
        "name": "reply_all",
        "description": "Reply to all recipients of an email (sender + all recipients + CC).",
        "input_schema": {
            "type": "object",
            "properties": {
                "email_id": {"type": "string", "description": "ID of email to reply to"},
                "body": {"type": "string", "description": "Reply body"},
            },
            "required": ["email_id", "body"],
        },
    },
    {
        "name": "draft_email",
        "description": "Create a draft email (not sent).",
        "input_schema": {
            "type": "object",
            "properties": {
                "recipients": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of recipient email addresses",
                },
                "subject": {"type": "string", "description": "Email subject"},
                "body": {"type": "string", "description": "Email body"},
            },
            "required": ["recipients", "subject", "body"],
        },
    },
]


class ToolExecutor:
    """Executes tool calls against the mock email backend."""

    def __init__(self, backend: EmailBackend, agent_email: str) -> None:
        self.backend = backend
        self.agent_email = agent_email

    def execute(self, tool_name: str, tool_input: dict[str, Any]) -> str:
        handler = getattr(self, f"_handle_{tool_name}", None)
        if not handler:
            return f"Unknown tool: {tool_name}"
        return handler(tool_input)

    def _handle_read_email(self, params: dict) -> str:
        email = self.backend.read_email(self.agent_email, params["email_id"])
        if not email:
            return "Email not found."
        return (
            f"From: {email.sender}\n"
            f"To: {', '.join(email.recipients)}\n"
            f"CC: {', '.join(email.cc)}\n"
            f"Subject: {email.subject}\n"
            f"Date: {email.timestamp}\n\n"
            f"{email.body}"
        )

    def _handle_list_inbox(self, params: dict) -> str:
        emails = self.backend.list_inbox(self.agent_email)
        if not emails:
            return "Inbox is empty."
        return "\n".join(e.summary() for e in emails)

    def _handle_list_unread(self, params: dict) -> str:
        emails = self.backend.list_unread(self.agent_email)
        if not emails:
            return "No unread emails."
        return "\n".join(e.summary() for e in emails)

    def _handle_search_inbox(self, params: dict) -> str:
        results = self.backend.search_inbox(self.agent_email, params["query"])
        if not results:
            return "No results found."
        return "\n".join(e.summary() for e in results)

    def _handle_send_email(self, params: dict) -> str:
        email = self.backend.send_email(
            sender=self.agent_email,
            recipients=params["recipients"],
            subject=params["subject"],
            body=params["body"],
            cc=params.get("cc"),
            reply_to_id=params.get("reply_to_id"),
        )
        return f"Email sent successfully. ID: {email.id}"

    def _handle_reply_all(self, params: dict) -> str:
        original = self.backend.read_email(self.agent_email, params["email_id"])
        if not original:
            return "Original email not found."
        all_recipients = list(
            set([original.sender] + original.recipients + original.cc) - {self.agent_email}
        )
        email = self.backend.send_email(
            sender=self.agent_email,
            recipients=all_recipients,
            subject=f"Re: {original.subject}",
            body=params["body"],
            reply_to_id=original.id,
        )
        return f"Reply-all sent to {len(all_recipients)} recipients. ID: {email.id}"

    def _handle_draft_email(self, params: dict) -> str:
        email = self.backend.draft_email(
            sender=self.agent_email,
            recipients=params["recipients"],
            subject=params["subject"],
            body=params["body"],
        )
        return f"Draft created. ID: {email.id}"
