from app.services.embedding_service import create_embedding

embedding = create_embedding(
    "White Summer T-Shirt"
)

print(len(embedding))