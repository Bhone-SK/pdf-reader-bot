# PDF Q&A

A RAG-based tool that lets you ask questions about any PDF using Claude AI. Upload a PDF, ask questions, and get answers with citations from the text.

## Requirements

- Python 3.8+
- An Anthropic API key (get one at console.anthropic.com)

## Installation

1. Clone the repository
   ```
   git clone https://github.com/Bhone-SK/pdf-reader-bot.git
   cd pdf-reader-bot
   ```

2. Install dependencies
   ```
   pip install anthropic pdfplumber sentence-transformers faiss-cpu python-dotenv
   ```

3. Set up your API key
   - Rename `.env.example` to `.env`
   - Open `.env` and replace `your-api-key-here` with your actual key from console.anthropic.com
   - Add credits to your account at console.anthropic.com → Plans & Billing

## Usage

### GUI
Run the graphical interface:
```
python gui.py
```

1. Click **[ load pdf ]** to select a PDF file
2. Wait for it to finish loading and embedding
3. Type your question and press **Enter** or click **[ ask ]**
4. The answer will appear in the output box with citations from the text

### CLI
Run from the terminal:
```
python main.py
```

1. Enter the full path to your PDF when prompted:
   ```
   Enter the file path: /Users/yourname/documents/paper.pdf
   ```
2. Enter your question when prompted:
   ```
   Enter your question: What is the main finding of this study?
   ```
3. The answer will print directly in the terminal


## Project Structure

```
your-project/
├── gui.py          # graphical user interface
├── callAPI.py      # handles Claude API calls
├── embedder.py     # embeds text using sentence transformers
├── search.py       # FAISS index for similarity search
├── pdf_loader.py   # extracts and chunks text from PDFs
├── .env.example    # API key template
├── .gitignore
└── README.md
```

## How It Works

1. The PDF is extracted and split into overlapping text chunks
2. Each chunk is embedded using a sentence transformer model
3. When you ask a question, it is also embedded and compared against the chunks
4. The 5 most relevant chunks are retrieved and sent to Claude along with your question
5. Claude answers based on the context from the PDF

## GUI Demo 

**Loading a PDF:**
![Loading PDF](https://github.com/user-attachments/assets/0fed3cfa-2851-49a7-ab45-3dd670dd4d7e)
![Loading PDF](https://github.com/user-attachments/assets/152db774-a904-4f9c-90b0-4abf497eb024)

**Wait until it is successfully loaded**
![Wait until loaded](https://github.com/user-attachments/assets/54e3d659-b6e2-462a-bdd0-617bf6fb06a4)

**Ask question and get answer**
![Ask question](https://github.com/user-attachments/assets/665b2d40-25d0-4637-a8f9-54b39705f847)
![Get answer](https://github.com/user-attachments/assets/7f50439b-1ab8-47a6-9607-c09300d00586)

## CLI Demo
**Loading a PDF:**
![Loading PDF](https://github.com/user-attachments/assets/bc76784b-bc97-4452-a409-015c7739e496)

**Ask question and get answer**
![Ask question](https://github.com/user-attachments/assets/cb469422-be3c-4ad8-9e52-8021b2207795)
![Get answer](https://github.com/user-attachments/assets/d592d547-e452-4daf-854b-8118a5a00863)

**Quit**
![Quit](https://github.com/user-attachments/assets/cf4c71e9-24ae-4e67-aaee-7fb9b45fba09)

## Notes

- Your `.env` file contains your API key — never share it or upload it to GitHub
- Each user needs their own Anthropic API key
- API usage is billed per request at console.anthropic.com
