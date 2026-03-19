import os
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
class LLMDecisionAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def decide(self, features):
        prompt = f"""
You are an expert in image compression.

Based on the following image characteristics, recommend the best compression strategy.

Image characteristics:
{features}

Choose the best format among:
JPEG, PNG, WEBP, AVIF, JPEG2000

Return ONLY JSON in this format:

{{
 "format": "...",
 "quality": number between 60 and 95,
 "resize": true or false,
 "reason": "short explanation"
}}
"""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        answer = response.choices[0].message.content
        decision = json.loads(answer)
        return decision