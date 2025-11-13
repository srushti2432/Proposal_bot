# proposal_generator.py

import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

from qdrant_handler import semantic_search

# Setup Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_proposal(sections, filled_fields):
    model = genai.GenerativeModel('gemini-1.5-pro')

    # Get doc context from Qdrant
    doc_context = []
    for sec in sections:
        doc_context.extend(semantic_search(sec, top_k=5))
    combined_context = "\n".join(doc_context)

    prompt = f"""
You are an expert proposal writer.

- Use these sections: {sections}
- Use the user-provided answers for each section.
- Enrich with relevant document context.
- Write clearly, persuasively, and in clean Markdown.

## User Answers:
{json.dumps(filled_fields, indent=2)}

## Document Context:
{combined_context}

✅ Generate ONLY the final Markdown proposal.
"""

    response = model.generate_content(prompt)
    proposal = response.text

    with open("proposal.md", "w", encoding="utf-8") as f:
        f.write(proposal)

    print("\n✅ Proposal saved as 'proposal.md'.")
