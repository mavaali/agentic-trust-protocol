"""In-memory email store with send/read/list/draft operations."""

from __future__ import annotations

from datetime import datetime

from .models import Email, EmailStatus, Inbox, User


class EmailBackend:
    """Deterministic in-memory email backend for testing agents."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._inboxes: dict[str, Inbox] = {}
        self._sent_log: list[Email] = []  # audit trail of all sent emails

    def add_user(self, user: User) -> None:
        self._users[user.email] = user
        self._inboxes[user.email] = Inbox(user=user)

    def get_user(self, email: str) -> User | None:
        return self._users.get(email)

    def deliver(self, email: Email) -> None:
        """Deliver an email to all recipients' inboxes."""
        for recipient in email.recipients + email.cc:
            if recipient in self._inboxes:
                self._inboxes[recipient].emails.append(email.model_copy())

    def list_inbox(self, user_email: str) -> list[Email]:
        inbox = self._inboxes.get(user_email)
        if not inbox:
            return []
        return inbox.emails

    def list_unread(self, user_email: str) -> list[Email]:
        inbox = self._inboxes.get(user_email)
        if not inbox:
            return []
        return inbox.unread

    def read_email(self, user_email: str, email_id: str) -> Email | None:
        inbox = self._inboxes.get(user_email)
        if not inbox:
            return None
        for email in inbox.emails:
            if email.id == email_id:
                email.status = EmailStatus.READ
                return email
        return None

    def send_email(
        self,
        sender: str,
        recipients: list[str],
        subject: str,
        body: str,
        cc: list[str] | None = None,
        reply_to_id: str | None = None,
    ) -> Email:
        """Send an email: creates it, delivers to recipients, logs it."""
        email = Email(
            sender=sender,
            recipients=recipients,
            cc=cc or [],
            subject=subject,
            body=body,
            status=EmailStatus.SENT,
            is_reply=reply_to_id is not None,
            reply_to_id=reply_to_id,
        )
        self._sent_log.append(email)
        self.deliver(email)
        return email

    def draft_email(
        self,
        sender: str,
        recipients: list[str],
        subject: str,
        body: str,
        cc: list[str] | None = None,
    ) -> Email:
        """Create a draft (not sent, not delivered)."""
        return Email(
            sender=sender,
            recipients=recipients,
            cc=cc or [],
            subject=subject,
            body=body,
            status=EmailStatus.DRAFT,
        )

    def search_inbox(self, user_email: str, query: str) -> list[Email]:
        inbox = self._inboxes.get(user_email)
        if not inbox:
            return []
        query_lower = query.lower()
        return [
            e
            for e in inbox.emails
            if query_lower in e.subject.lower() or query_lower in e.body.lower()
        ]

    @property
    def sent_log(self) -> list[Email]:
        """All emails that were actually sent (for evaluation)."""
        return list(self._sent_log)

    def reset(self) -> None:
        """Clear all state."""
        self._users.clear()
        self._inboxes.clear()
        self._sent_log.clear()
