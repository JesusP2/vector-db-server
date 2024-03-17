from chromadb.api.types import EmbeddingFunction, Documents, Embeddings


class VoyageAIEmbeddingFunction(EmbeddingFunction):
    """Embedding function for Voyageai.com"""

    def __init__(
        self, api_key: str, model_name: str = "voyage-01", batch_size: int = 8
    ):
        """
        Initialize the VoyageAIEmbeddingFunction.

        Args:
        api_key (str): Your API key for the HuggingFace API.
        model_name (str, optional): The name of the model to use for text embeddings. Defaults to "voyage-01".
        batch_size (int, optional): The number of documents to send at a time. Defaults to 8 (The max supported 3rd Nov 2023).
        """
        if batch_size > 8:
            print("Voyage AI as of (3rd Nov 2023) has a batch size of max 8")

        if not api_key:
            raise ValueError("Please provide a VoyageAI API key.")

        try:
            import voyageai
        except ImportError:
            raise ValueError(
                "The VoyageAI python package is not installed. Please install it with `pip install voyageai`"
            )

        voyageai.api_key = api_key
        self.client = voyageai.Client()
        self.batch_size = batch_size
        self.model = model_name
        self.get_embeddings = self.client.embed

    def __call__(self, input: Documents) -> Embeddings:
        """
        Get the embeddings for a list of texts.

        Args:
        input (Documents): A list of texts to get embeddings for.

        Returns:
        Embeddings: The embeddings for the texts.

        Example:
        >>> voyage_ef = VoyageAIEmbeddingFunction(api_key="your_api_key")
        >>> input = ["Hello, world!", "How are you?"]
        >>> embeddings = voyage_ef(input)
        """
        iters = range(0, len(input), self.batch_size)
        embeddings = []
        for i in iters:
            results = self.get_embeddings(
                input[i : i + self.batch_size],
                model=self.model,
            )
            embeddings += results.embeddings
        return embeddings
