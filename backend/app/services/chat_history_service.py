from sqlalchemy.orm import Session

from app.models.chat_history import ChatHistory


def save_chat(
    user_id: int,
    user_message: str,
    ai_response: str,
    db: Session,
    product_id: int | None = None
):
    chat = ChatHistory(
        user_id=user_id,
        user_message=user_message,
        ai_response=ai_response,
        product_id=product_id
    )

    db.add(chat)
    db.commit()

    return chat

def get_last_chat(
    user_id: int,
    db: Session
):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.id.desc())
        .first()
    )