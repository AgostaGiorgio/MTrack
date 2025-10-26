from src.config.logger import *
import httpx, json

from src.models.ai_messages import ChatMessage


logger = logging.getLogger(__name__)


class LLMWrapper:
    def __init__(self, llm_url: str, model: str):
        self.__llm_url = llm_url
        self.__model = model
        self.__headers = {
            "Content-Type": "application/json",
        }
        
    async def ainvoke(self, messages: list[ChatMessage] | str, prompt: str | None = None) -> str:
        _messages: list[ChatMessage] = []
        if prompt:
            _messages.append(ChatMessage(role="system", content=prompt))
            
        if type(messages) is str:
            _messages.append(ChatMessage(role="user", content=messages))
        else:
            _messages += messages
            
        data = {
            "model": self.__model,
            "messages": [msg.to_dict() for msg in _messages],
            "stream": False,
            "Temperature": 0,
        }
        
        async with httpx.AsyncClient(timeout=None) as client:
            logger.debug(f"Sending request to LLM at {self.__llm_url} with data: {data}")
            response = await client.post(self.__llm_url, json=data, headers=self.__headers)
            response.raise_for_status()
            raw_text = response.text
            logger.debug(f"Raw LLM response: {raw_text}")

            contents = []
            for line in raw_text.strip().split("\n"):
                try:
                    obj = json.loads(line)
                    if "message" in obj and "content" in obj["message"]:
                        contents.append(obj["message"]["content"])
                except json.JSONDecodeError:
                    continue

            return "".join(contents).strip()