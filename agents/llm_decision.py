import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMDecisionAgent:

    def __init__(self):
        self.client = OpenAI(api_key="sk-5678ijklmnopabcd5678ijklmnopabcd5678ijkl")
    def decide(self, features):

        prompt = f"""
You are an expert in image compression.

Image features:
{features}

Choose best format among: JPEG, PNG, WEBP

Rules:
- Photos → JPEG (quality 80-90)
- Documents/text → PNG
- Screenshots → PNG or WEBP

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

        except:
            pass

        # 🔥 fallback (très important)
        return {
            "format": "JPEG",
            "quality": 75,
            "resize": True,
            "reason": "fast mode"
        }