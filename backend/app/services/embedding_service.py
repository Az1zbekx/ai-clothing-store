import ollama

def create_embedding(text: str):

    response = ollama.embed(
        model="nomic-embed-text",
        input=text
    )

    return response["embeddings"][0]