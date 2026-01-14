import re
from typing import Tuple
from langchain_gigachat.chat_models import GigaChat  # пакет langchain-gigachat [web:3]
from bot.prompts import EVAL_PROMPT

class GigaChatService:
    def __init__(self, credentials: str, scope: str, verify_ssl: bool):
        self.llm = GigaChat(credentials=credentials, scope=scope, verify_ssl_certs=verify_ssl)

    async def evaluate(
        self,
        audit: str,
        product: str,
        activity: str,
        ogran: str,
        solution: str,
    ) -> Tuple[int, str]:
        prompt = EVAL_PROMPT.format(
            audit=audit,
            product=product,
            activity=activity,
            ogran=ogran,
            solution=solution,
        )
        # invoke синхронный; для простоты оставляем так (можно завернуть в to_thread при нагрузке)
        resp = self.llm.invoke(prompt)
        text = getattr(resp, "content", str(resp))

        score = self._extract_score(text)
        return score, text

    def _extract_score(self, text: str) -> int:
        m = re.search(r"(\bОценка\b\s*:\s*)(\d{1,2})\s*/\s*10", text, flags=re.IGNORECASE)
        if m:
            return max(0, min(10, int(m.group(2))))
        m2 = re.search(r"(\d{1,2})\s*/\s*10", text)
        if m2:
            return max(0, min(10, int(m2.group(1))))
        return 0
