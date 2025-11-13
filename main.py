# main.py

from document_handler import read_uploaded_file
from qdrant_handler import upsert_document
from structure_handler import (
    parse_structure,
    auto_detect_sections_and_fields,
    ask_missing_fields_interactively
)
from proposal_generator import generate_proposal


def main():
    print("\n📄 Reading uploaded document...")
    doc_text = read_uploaded_file()
    print("✅ Document loaded!")

    print("\n🔎 Indexing document in Qdrant...")
    upsert_document(doc_text)

    print("\n📋 Paste your structure (any format — JSON, bullet points, template, or text).")
    print("💡 When done, type a single line with 'END' and hit Enter.")

    # ✅ MULTI-LINE input:
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    structure_input = "\n".join(lines)

    # Now parse and process:
    sections, fields_map = auto_detect_sections_and_fields(structure_input, doc_text)

    print(f"\n✅ Sections found: {sections}")
    print(f"✅ Fields to fill: {fields_map}")

    filled_fields = ask_missing_fields_interactively(fields_map)

    generate_proposal(sections, filled_fields)

    print("\n🎉 Proposal ready! See: proposal.md")


if __name__ == "__main__":
    main()
