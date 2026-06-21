from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

sentences = [
    "I love dogs.",
    "I like puppies.",
    "I enjoy programming."
]

embeddings = model.encode(sentences)

print(embeddings.shape)