import fitz


class Preprocess:
    def __init__(self, file_path):
        self.file_path = file_path
        author_and_title = file_path.split('/')[-1]
        author_name = author_and_title.split('-')[1]
        author_name = author_name.split('.')[0]
        self.pdf_info = {'name': author_name.lower(),
                         'author': author_and_title.split('-')[0].lower(),
                         'text': ''}

    def clean_document(self, doc_text):
        cleaned_lines = [line.strip() for
                         line in doc_text.split('\n') if line.strip() != '']
        cleaned_text = '\n'.join(cleaned_lines)
        cleaned_text = ' '.join(cleaned_text.split())
        return cleaned_text

    def read_pdf(self):
        pages_text = []
        with fitz.open(self.file_path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                clean_page = self.clean_document(page.get_text())
                self.pdf_info['text'] += clean_page
                pages_text.append((clean_page, page_number))
        return pages_text, self.pdf_info

    def chunk_text(self, pages_text, chunk_size, overlap_size):
        chunks = []
        chunk = ""
        current_chunk_pages = []
        start = 0
        for text, page_number in pages_text:
            while start < len(text):
                end = start + chunk_size \
                        if start + chunk_size <= len(text) else len(text)
                chunk += text[start:end]
                if page_number not in current_chunk_pages:
                    current_chunk_pages.append(page_number)

                if len(chunk) >= chunk_size or end == len(text):
                    chunks.append((chunk, current_chunk_pages))
                    chunk = text[max(0, end-overlap_size):end]
                    current_chunk_pages = [page_number] if chunk else []
                    start = end + overlap_size - len(chunk)
                else:
                    start = end

            start = 0

        if chunk:
            chunks.append((chunk, current_chunk_pages))
        return chunks
