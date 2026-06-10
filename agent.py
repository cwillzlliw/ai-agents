"""
Beginner Agent Project 1: Q&A Agent with Web Search
Using Groq Compound — built-in web search, no external tools needed
"""
import os

from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL = "groq/compound-mini"               # has built-in web search

client = Groq(api_key=GROQ_API_KEY)

def run_agent(user_question: str) -> str:
    print(f"\n[User] {user_question}\n")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a cybersecurity consultant advising K-12 schools. Be concise and practical."
                    "Search the web for current information when needed. "
                    "Always say where your information came from."
                )
            },
            {"role": "user", "content": user_question}
        ]
    )

    answer = response.choices[0].message.content
    print(f"[Answer]\n{answer}")
    return answer

if __name__ == "__main__":
    run_agent("What is the CIA triad in cybersecurity?")
