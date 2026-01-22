from sqlmodel import select
from sqlalchemy.orm import selectinload, aliased, joinedload
from sqlalchemy import exists, and_, desc
from auth.models import User
from .models import Chat, ChatUser, Message


def get_chat(chat_id, current_user, session):

    other_chatUser = aliased(ChatUser)

    other_participant = (
        select(other_chatUser.user_id)
        .where(
            and_(
                other_chatUser.chat_id == chat_id,
                other_chatUser.user_id != current_user,
            )
        )
        .limit(1)
        .scalar_subquery()
    )

    stmt = (
        select(ChatUser, User)
        .join(User, User.id == other_participant)
        .where(
            and_(
                ChatUser.chat_id == chat_id,
                ChatUser.user_id == current_user,
            )
        )
    )

    chat_db = session.exec(stmt).one_or_none()

    return chat_db


def get_user_all_chats(current_user, session):

    other_chatUser = aliased(ChatUser)

    other_participant = (
        select(other_chatUser.user_id)
        .where(
            and_(
                other_chatUser.chat_id == ChatUser.chat_id,
                other_chatUser.user_id != current_user,
            )
        )
        .limit(1)
        .scalar_subquery()
    )

    stmt = (
        select(ChatUser, User)
        .join(User, User.id == other_participant)
        .where(ChatUser.user_id == current_user)
    )

    chats_db = session.exec(stmt).all()

    if not chats_db:
        return

    return chats_db


def get_chat_messages(chat_id: int, cursor: int | None, session):
    limit = 30

    stmt = select(Message).where(Message.chat_id == chat_id)

    if cursor:
        stmt = stmt.where(Message.id < cursor)

    stmt = stmt.order_by(Message.created_at.desc()).limit(limit + 1)

    messages = session.exec(stmt).all()

    has_more = len(messages) > limit
    messages = messages[:limit]

    next_cursor = messages[-1].id if has_more else None

    messages.reverse()

    return {
        "items": messages,
        "next_cursor": next_cursor,
        "has_more": has_more,
    }
