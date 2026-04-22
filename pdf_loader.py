import pdfplumber

def text_extracter_into_chunks(path):
    with pdfplumber.open(path) as pdf:
        all_pages = pdf.pages
        text_in_pdf = ""
        for page in all_pages:
            page_text = page.extract_text()
            if page_text:
                text_in_pdf += page_text + "\n"
        return split_text_into_chunks(text_in_pdf)
    
def split_text_into_chunks(text_in_pdf, chunk_size = 1000, overlap = 200):
    start = 0
    end = chunk_size
    text_list = []
    while start < len(text_in_pdf):
        chunk = text_in_pdf[start:end]
        text_list.append(chunk)
        start += chunk_size - overlap
        end += chunk_size - overlap
    return text_list
    

