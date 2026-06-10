import os

from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL = "groq/compound-mini"

client = Groq(api_key=GROQ_API_KEY)

def summarize_document(file_path: str) -> str:
    with open(file_path, "r") as f:
        content = f.read()
    
    print(f"\n[Agent] Reading: {file_path}")
    print(f"[Agent] Characters: {len(content)}\n")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a compliance analyst for small healthcare practices. "
                    "When given a document produce: "
                    "1) A 3-sentence summary, "
                    "2) Key points as a bullet list, "
                    "3) Any compliance gaps or risks you notice."
                )
            },
            {
                "role": "user",
                "content": f"Please analyze this document:\n\n{content}"
            }
        ]
    )

    answer = response.choices[0].message.content
    print(f"[Answer]\n{answer}")
    return answer

if __name__ == "__main__":
    summarize_document("sample.txt")