from sqlmodel import select, func, exists
from sqlalchemy.orm import selectinload, aliased, joinedload
from sqlalchemy import and_, desc
from auth.models import User
from .models import Chat, ChatUser, Message


def get_chat(chat_id, current_user, session, other_user=None):

    if not other_user:
        other_chatUser = aliased(ChatUser)

        other_user = (
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
        .join(User, User.id == other_user)
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


def verify_if_chat_exists(current_user, other_user_id, session):
    stmt = (
        select(Chat.id)
        .join(ChatUser)
        .where(ChatUser.user_id.in_([current_user, other_user_id]))
        .group_by(Chat.id)
        .having(func.count(ChatUser.user_id) == 2)
    )

    return session.exec(stmt).one_or_none()


def create_chat(current_user, other_user_id, session):
    chat = Chat()

    session.add(chat)
    session.flush()

    session.add_all(
        [
            ChatUser(user_id=current_user, chat_id=chat.id),
            ChatUser(user_id=other_user_id, chat_id=chat.id),
        ]
    )

    session.commit()
    session.refresh(chat)

    return chat.id
