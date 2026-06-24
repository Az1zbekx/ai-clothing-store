from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.embedding_service import create_embedding


def search_products(query: str, db: Session):

    query_embedding = create_embedding(query)

    sql = text("""
        SELECT
            id,
            name,
            description,
            category,
            color,
            season,
            size,
            price,
            stock
        FROM products
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT 6
    """)

    result = db.execute(
        sql,
        {
            "embedding": str(query_embedding)
        }
    )

    return result.fetchall()