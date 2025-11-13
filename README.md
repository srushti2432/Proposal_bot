# RAG-Based Proposal Generation Pipeline

## Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline that automates the creation of client proposals using RFP (Request for Proposal) documents.

The system extracts and chunks context from RFPs, embeds them into a Qdrant vector database, and uses these chunks—along with a predefined structure (structure.txt)—to interactively ask the user questions. It then combines all relevant context and user inputs to generate a comprehensive proposal in Markdown format.

## Key Features

* **RFP Parsing & Chunking** – Extracts and preprocesses text from RFPs for contextual understanding.

* **Embedding Storage in Qdrant** – Uses Qdrant as the vector store for efficient semantic retrieval.

* **RAG Integration with Gemini** – Leverages a Large Language Model (LLM) to generate grounded responses from retrieved RFP content.

* **Interactive Q&A Interface** – Dynamically asks the user guided questions based on the structure defined in structure.txt.

* **Proposal Generation** – Combines contextual data and user responses to produce a structured Markdown proposal document.

## How It Works

* **Extract Context** – Reads and extracts text from the RFP document (PDF or text).

* **Chunking & Embedding** – Splits text into semantically meaningful chunks and embeds them into Qdrant.

* **Context Retrieval** – Retrieves the most relevant chunks when generating proposal content.

* **Interactive Q&A** – Prompts the user with targeted questions to refine the proposal.

* **Generate Proposal** – Synthesizes retrieved context and user input into a complete Markdown proposal.

## Dependencies

* Create a virtual environment and install dependencies:

```
pip install -r requirements.txt
```

### Core Libraries:

1. `qdrant-client – Vector database for embeddings`

2. `pymupdf or PyPDF2 – PDF text extraction`

3. `google-generativeai – Gemini API integration`

4. `python-dotenv – Environment variable management`

### Environment Variables (.env)

Create a .env file in your project root with:

```

GEMINI_API_KEY=your_gemini_api_key_here

QDRANT_URL=your_qdrant_url

QDRANT_API_KEY=your_qdrant_api_key

```

### Running the Project

Run the main pipeline with:

```
python main.py
```

or

```
python main.py run
```

#### The system will:

* Process your RFP,

* Ask contextual questions,

* Retrieve relevant chunks from Qdrant,

* And generate a Markdown proposal file under output/proposal.md.
