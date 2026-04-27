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

    @staticmethod
    def _normalize_to_list(v: list[str] | str | None) -> list[str]:
        """Coerce a string/None/list input to list[str].

        LLMs occasionally return a single-recipient field as a string instead
        of a list; this normalizes so Email() construction never fails on
        well-formed-but-wrong-shape inputs.
        """
        if v is None:
            return []
        if isinstance(v, str):
            return [v] if v else []
        return list(v)

    def send_email(
        self,
        sender: str,
        recipients: list[str] | str,
        subject: str,
        body: str,
        cc: list[str] | str | None = None,
        reply_to_id: str | None = None,
    ) -> Email:
        """Send an email: creates it, delivers to recipients, logs it.

        If any recipient is configured as an auto-responder, also generates
        and delivers a synthetic reply back to the sender. Used for D1
        composition-mode-iteration scenarios.
        """
        recipients_list = self._normalize_to_list(recipients)
        cc_list = self._normalize_to_list(cc)
        email = Email(
            sender=sender,
            recipients=recipients_list,
            cc=cc_list,
            subject=subject,
            body=body,
            status=EmailStatus.SENT,
            is_reply=reply_to_id is not None,
            reply_to_id=reply_to_id,
        )
        self._sent_log.append(email)
        self.deliver(email)

        # Auto-responder hook: any recipient marked auto_responder generates a
        # synthetic reply back to the sender, delivered to the sender's inbox.
        for recipient in recipients_list + cc_list:
            user = self._users.get(recipient)
            if user and user.auto_responder:
                template = user.auto_responder_template or (
                    f"Thanks for your note. I'd love to follow up — could you "
                    f"share a bit more context when you have a chance?\n\nBest,\n{user.name}"
                )
                auto_reply = Email(
                    sender=recipient,
                    recipients=[sender],
                    subject=f"Re: {subject}",
                    body=template,
                    status=EmailStatus.UNREAD,
                    is_reply=True,
                    reply_to_id=email.id,
                )
                self._sent_log.append(auto_reply)
                self.deliver(auto_reply)
        return email

    def draft_email(
        self,
        sender: str,
        recipients: list[str] | str,
        subject: str,
        body: str,
        cc: list[str] | str | None = None,
    ) -> Email:
        """Create a draft (not sent, not delivered)."""
        return Email(
            sender=sender,
            recipients=self._normalize_to_list(recipients),
            cc=self._normalize_to_list(cc),
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
