from pdf_loader import text_extracter_into_chunks
from embedder import embed_sentences
from search import create_faiss_index
from callAPI import format_LLM
from pathlib import Path

path = Path(input("Enter the file path: "))
if not path.exists():
    print("File not found. Please check the path")
    exit()
chunks_of_text = text_extracter_into_chunks(path)
pdf_embeddings = embed_sentences(chunks_of_text)

ask_more = True
while ask_more:
    question = input("Enter your question (or q to exit): ").strip()
    if question.upper() == "Q":
        ask_more = False
    else:
        I = create_faiss_index(pdf_embeddings, question, pdf_embeddings.shape[1])
        top_matches = [chunks_of_text[i] for i in I[0]]

        answer = format_LLM(question, top_matches)
        print(answer)
