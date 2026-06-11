import os
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"

client = Groq(api_key=GROQ_API_KEY)

def step1_search(topic: str) -> str:
    print(f"\n[Step 1] Searching for: {topic}")
    response = client.chat.completions.create(
        model="groq/compound-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a research assistant. Search the web and return raw findings only. No formatting, just facts and sources."
            },
            {
                "role": "user",
                "content": f"Search for current information on: {topic}"
            }
        ]
    )
    result = response.choices[0].message.content
    print(f"[Step 1 Complete] {len(result)} characters of research gathered")
    return result

def step2_summarize(raw_research: str) -> str:
    print(f"\n[Step 2] Summarizing research...")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an analyst. Summarize the key facts from the research provided. Be concise and accurate."
            },
            {
                "role": "user",
                "content": f"Summarize these research findings:\n\n{raw_research}"
            }
        ]
    )
    result = response.choices[0].message.content
    print(f"[Step 2 Complete] Summary created")
    return result

def step3_format_report(topic: str, summary: str) -> str:
    print(f"\n[Step 3] Formatting final report...")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional report writer for a cybersecurity consulting firm. "
                    "Format the input into a clean report with these sections: "
                    "Executive Summary, Key Findings, Recommendations, and Sources."
                )
            },
            {
                "role": "user",
                "content": f"Topic: {topic}\n\nResearch Summary:\n{summary}"
            }
        ]
    )
    result = response.choices[0].message.content
    print(f"[Step 3 Complete] Report ready\n")
    return result

def run_research_agent(topic: str) -> str:
    print(f"\n{'='*50}")
    print(f"RESEARCH AGENT STARTING")
    print(f"Topic: {topic}")
    print(f"{'='*50}")

    raw_research = step1_search(topic)
    summary = step2_summarize(raw_research)
    report = step3_format_report(topic, summary)

    print(f"\n{'='*50}")
    print("FINAL REPORT")
    print(f"{'='*50}\n")
    print(report)
    return report

if __name__ == "__main__":
    run_research_agent("HIPAA cybersecurity requirements for small therapy practices in 2026")