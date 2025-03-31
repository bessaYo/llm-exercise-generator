from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_huggingface import HuggingFaceEmbeddings
from uuid import uuid4
import faiss


class VectorStore:
    def __init__(self, embedding_function=None):
        """
        Initializes an empty FAISS vector store with the specified embedding function.

        Args:
            embedding_function: A function that converts text into vector embeddings.
        """
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
        """
        Adds extracted documents/pages to the vector store as text embeddings.

        Args:
            documents (list): A list of Document objects.

        Returns:
            None
        """
        uuids = [str(uuid4()) for _ in range(len(documents))]
        self.vector_store.add_documents(documents=documents, ids=uuids)
        print(f"Successfully added {len(documents)} documents to the vector store")

    def find_related_documents(self, learning_goal, k=2):
        """
        Finds the most relevant slides in the vector store for a given learning goal.

        Args:
            learning_goal (str): A string describing the learning objective or query.
            k (int): The number of similar slides to retrieve (default is 2).

        Returns:
            list: A list of the most relevant slides to the learning goal, ranked by similarity.
        """
        learning_goal_embedding = self.embedding_function.embed_query(learning_goal)
        results = self.vector_store.similarity_search_by_vector(
            learning_goal_embedding, k=k
        )
        return results
