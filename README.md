# 🔎 Website RAG - Answer questions about a website content using RAG

This streamlit application lets you interactively ask questions about any website using a Retrieval-Augmented Generation (RAG) pipeline.

Simply load a URL, ask your question, and watch the AI stream the answer in real time - based strictly on the website's content.


## Installation

This project uses **uv**, an ultra-fast Python package/dependency manager.

### 1. Clone the repo

```bash
git clone https://github.com/sudharshanreddyt/website-rag.git
cd website-rag
```

## 2. Install dependencies using uv

```bash
uv sync
```

This will create a virtual environment and install the libraries specified in `pyproject.toml`.


## 3. Environment Variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```


## 4. Running the App

Start the Streamlit UI:

```bash
uv run streamlit run main.py
```

The app will open automatically at:

```
http://localhost:8501
```

## For running the image using Docker

```bash
docker run -p 8501:8501 --env GROQ_API_KEY=your_key_here website-rag
```

## Project Structure

```
website-rag/
│
├── main.py                # Streamlit UI + model streaming
├── langchain_helper.py    # Loading, splitting, embedding, RAG prompt
├── pyproject.toml         # uv dependency config
├── README.md              # Project documentation
└── .env                   # for storing API keys and secrets
```


## How It Works - RAG Pipeline

1. **Load Website:**
   Extract text content using LangChain's `WebBaseLoader`.

2. **Split Content:**
   Breaks large text into small, meaningful chunks.

3. **Embed Text:**
   Generates vector embeddings using SentenceTransformer MiniLM.

4. **Store in Chroma:**
   Store embeddings in a vector database for fast similarity search.

5. **Retrieve Relevant Context:**
   Fetches the most relevant chunks based on your query.

6. **Generate Answer (OpenAI LLM from Groq):**
   Streams a final answer that uses only the retrieved website content.


## Example Usage

1. Enter a URL, such as:
   - `https://www.geeksforgeeks.org/artificial-intelligence/agents-artificial-intelligence/`

2. Click **Load Website** to process and index the content.

3. Ask any question related to the page:
   - *Explain the architecture of AI agents*
   - *What are the different types of of AI agents*
   - *How does AI agents work ?*

4. The app will stream the answer in real time based on the website's information.


## Sample Outputs
![Sample_Output1](/outputs/output1.png)