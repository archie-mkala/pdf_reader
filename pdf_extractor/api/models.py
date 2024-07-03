from django.db import models
import PyPDF2
import spacy

nlp = spacy.load('en_core_web_sm')

class Pdf(models.Model):
    email = models.EmailField(unique=True)
    pdf_file = models.FileField(upload_to='pdfs/')
    content = models.TextField(blank=True, null=True)
    nouns = models.JSONField(blank=True, null=True)
    verbs = models.JSONField(blank=True, null=True)

    def extract_text(self):
        with self.pdf_file.open('rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            text = ''
            for page in range(pdf_reader.getNumPages()):
                text += pdf_reader.getPage(page).extractText()

            doc = nlp(text)
            nouns = [token.text for token in doc if token.pos_ == 'NOUN']
            verbs = [token.text for token in doc if token.pos_ == 'VERB']

            self.content = text
            self.nouns = nouns
            self.verbs = verbs
            self.save()


