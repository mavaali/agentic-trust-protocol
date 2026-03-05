"""Data models for the mock email system."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4


class EmailStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    READ = "read"
    UNREAD = "unread"


class Email(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex[:8])
    sender: str
    recipients: list[str]
    cc: list[str] = Field(default_factory=list)
    subject: str
    body: str
    timestamp: datetime = Field(default_factory=datetime.now)
    status: EmailStatus = EmailStatus.UNREAD
    is_reply: bool = False
    reply_to_id: str | None = None

    def summary(self) -> str:
        return f"[{self.id}] From: {self.sender} | Subject: {self.subject} | {self.status.value}"


class User(BaseModel):
    email: str
    name: str
    role: str = "employee"


class Inbox(BaseModel):
    user: User
    emails: list[Email] = Field(default_factory=list)

    @property
    def unread(self) -> list[Email]:
        return [e for e in self.emails if e.status == EmailStatus.UNREAD]

    @property
    def count(self) -> int:
        return len(self.emails)
