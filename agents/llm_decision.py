import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMDecisionAgent:

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "La variable OPENAI_API_KEY est absente. "
                "Copie .env.example vers .env et renseigne ta cle."
            )
        self.client = OpenAI(api_key=api_key)

    def decide(self, features):
        prompt = f"""
You are an expert in image compression.

Image features:
{features}

Choose best format among: JPEG, PNG, WEBP

Rules:
- Photos -> JPEG (quality 80-90)
- Documents/text -> PNG
- Screenshots -> PNG or WEBP

Return ONLY JSON:
{{
 "format": "....",
 "quality": number,
 "resize": false,
 "reason": "short explanation"
}}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            answer = response.choices[0].message.content

            match = re.search(r"\{.*\}", answer, re.DOTALL)

            if match:
                return json.loads(match.group())

        except Exception as e:
            print(f"[LLMDecision] Erreur OpenAI : {e}")

        # Fallback en cas d'echec
        return {
            "format": "JPEG",
            "quality": 75,
            "resize": True,
            "reason": "fast mode"
        }