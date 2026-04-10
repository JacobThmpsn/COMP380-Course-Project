import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You rate reading difficulty.

Return only JSON.

{
 "score": number,
 "reasons": [string,...],
 "complex_words":[{"word":string,"definition":string}]
}

Score scale
0 easiest
100 hardest

Explain what makes the text easy or difficult.
Do not suggest rewriting the text.
Definitions must use simple English.
"""


def score_with_ai(text, metrics):

    payload = {
        "text": text,
        "metrics": metrics
    }

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        temperature=0.2,
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":str(payload)}
        ]
    )

    content = response.choices[0].message.content
    import json
    return json.loads(content)