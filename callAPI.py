from dotenv import load_dotenv
import os
from pathlib import Path
import anthropic

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')

client = anthropic.Anthropic()

def format_LLM(question, top_matches_list):
    top_matches_string = "\n".join(top_matches_list)
    content = f"""Use the following context from a scientific paper to answer the question.
    Include citations from the text.
    Context: {top_matches_string}
    Question: {question}"""
    
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )
    return message.content[0].text
