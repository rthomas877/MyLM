from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

class Chat:

    def __init__(
            self,
            stream=False,
            temperature=0.1,
            top_p=0.9,
            top_k=40,
            min_p=0.05,
            max_tokens=10000,
            max_completion_tokens=None,
            stop=None,
            presence_penalty=0.0,
            frequency_penalty=0.0,
            repeat_penalty=1.1,
            seed=None,
            n=1
        ):
        self.stream = stream
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.min_p = min_p
        self.max_tokens = max_tokens
        self.max_completion_tokens = max_completion_tokens
        self.stop = stop
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.repeat_penalty = repeat_penalty
        self.seed = seed
        self.n = n

    async def chat_completion(self, query) -> ChatCompletion:
        client = AsyncOpenAI(
            base_url="http://localhost:8080/v1",
            api_key="not-needed"
        )

        response = await client.chat.completions.create(
            model="qwen3",

            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant"
                },
                {
                    "role": "user",
                    "content": query
                }
            ],

            # Generation
            stream=self.stream,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
            max_completion_tokens=self.max_completion_tokens,

            # Repetition
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,

            # Reproducibility
            seed=self.seed,

            # Stopping
            stop=self.stop,

            # Number of responses
            n=self.n,
        )
        return response