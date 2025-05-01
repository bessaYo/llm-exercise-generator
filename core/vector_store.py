#!/usr/bin/env python
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_huggingface import HuggingFaceEmbeddings
from uuid import uuid4
import faiss


class VectorStore:
    def __init__(self, embedding_function=None):
        """Initializes an empty FAISS vector store with the specified embedding function."""
        self.name = "vector_store"
        if embedding_function is None:
            # Default: all-MiniLM-L6-v2 - smaller model (22M) with high accuracy
            embedding_function = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        self.embedding_function = embedding_function
        self.embedding_dim = len(embedding_function.embed_query("test"))
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.vector_store = FAISS(
            embedding_function=embedding_function,
            index=self.index,
            docstore=InMemoryDocstore({}),
            index_to_docstore_id={},
        )

    def add_documents(self, documents):
        """Adds extracted documents/pages to the vector store as text embeddings."""
        uuids = [str(uuid4()) for _ in range(len(documents))]
        self.vector_store.add_documents(documents=documents, ids=uuids)
        print(f"Successfully added {len(documents)} documents to the vector store")

    def find_related_documents(self, learning_objective, k=3):
        """Finds the most relevant documents in the vector store based on a learning objective."""
        if not self.embedding_function:
            raise ValueError("Embedding function is not initialized.")

        if not self.vector_store:
            raise ValueError("Vector store is not initialized.")

        # Create embedding for the learning objective
        learning_objective_embedding = self.embedding_function.embed_query(
            learning_objective
        )
        if learning_objective_embedding is None:
            raise ValueError("Embedding for learning goal could not be created.")

        # Perform similarity search with k = 3
        results = self.vector_store.similarity_search_by_vector(
            learning_objective_embedding, k=k
        )

        return results if results else None
