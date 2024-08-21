import logging
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict
from models import analyse as analyse_model, document as document_model
from config.database import get_db
from datetime import date
from PyPDF2 import PdfReader
import io
import spacy
from collections import Counter
import nltk
from nltk.corpus import stopwords
from transformers import pipeline

# Load necessary models and resources
nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

router = APIRouter()

class KeywordPosition(BaseModel):
    sentence: str
    position: int
    relevance_score: float

class KeywordResult(BaseModel):
    keyword: str
    occurrences: int
    positions: List[KeywordPosition]

class AnalysisResponse(BaseModel):
    text: str
    stats: dict
    keyword_results: List[KeywordResult]
    total_words: int
    keyword_density: Dict[str, float]

@router.post("/analyse", response_model=AnalysisResponse)
async def analyse_document(file: UploadFile = File(...), keywords: str = Form(""), db: Session = Depends(get_db)):
    content = await file.read()

    if file.content_type == "application/pdf":
        text_content, stats = extract_text_and_stats_from_pdf(content)
    else:
        try:
            text_content = content.decode("utf-8")
            stats = analyze_text(text_content)
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Invalid document format. Please upload a text file or a PDF.")

    # Save document metadata and analysis result
    new_document = document_model.Document(
        nom_document=file.filename,
        type_document=file.content_type,
        date_upload=date.today(),
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    new_analysis = analyse_model.Analyse(
        date_analyse=date.today(),
        result=text_content,
        id_document=new_document.id_document,
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    
    # Process keywords
    keyword_list = [k.strip().lower() for k in keywords.split(',') if k.strip()]
    doc = nlp(text_content)
    keyword_positions = find_sentences_with_keywords(doc, keyword_list)
    total_words = len(doc)
    keyword_density = calculate_keyword_density(doc, keyword_list)

    keyword_results = [
        KeywordResult(
            keyword=keyword,
            occurrences=len(positions),
            positions=sorted(positions, key=lambda x: x.relevance_score, reverse=True)
        )
        for keyword, positions in keyword_positions.items()
    ]

    return AnalysisResponse(
        text=text_content,
        stats=stats,
        keyword_results=keyword_results,
        total_words=total_words,
        keyword_density=keyword_density
    )

# Helper functions

def extract_text_and_stats_from_pdf(pdf_content: bytes) -> tuple[str, dict]:
    text = ""
    pdf_reader = PdfReader(io.BytesIO(pdf_content))
    num_pages = len(pdf_reader.pages)
    
    for page in pdf_reader.pages:
        text += page.extract_text()

    stats = analyze_text(text)
    stats.update({
        "total_pages": num_pages,
        "average_words_per_page": stats["total_words"] / num_pages if num_pages else 0,
    })

    return text, stats

def analyze_text(text: str) -> dict:
    doc = nlp(text)
    
    words = [token.text.lower() for token in doc if token.is_alpha]
    sentences = list(doc.sents)
    paragraphs = text.split('\n\n')
    
    stop_words = set(stopwords.words('english'))
    word_freq = Counter(word for word in words if word not in stop_words)
    
    syllable_count = sum(count_syllables(word) for word in words)
    complex_words = sum(1 for word in words if count_syllables(word) >= 3)
    
    if len(sentences) > 0 and len(words) > 0:
        flesch_kincaid = 0.39 * (len(words) / len(sentences)) + 11.8 * (syllable_count / len(words)) - 15.59
    else:
        flesch_kincaid = 0

    synthesis = generate_summary(text)
    entities = extract_named_entities(doc)
    
    stats = {
        "total_words": len(words),
        "unique_words": len(set(words)),
        "total_sentences": len(sentences),
        "total_paragraphs": len(paragraphs),
        "average_sentence_length": len(words) / len(sentences) if sentences else 0,
        "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
        "most_common_words": dict(word_freq.most_common(10)),
        "flesch_kincaid_grade": flesch_kincaid,
        "complex_word_count": complex_words,
        "complex_word_percentage": (complex_words / len(words)) * 100 if words else 0,
        "synthesis": synthesis,
        "named_entities": entities,
    }
    
    return stats

def count_syllables(word: str) -> int:
    word = word.lower()
    count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count += 1
    if count == 0:
        count += 1
    return count

def generate_summary(text: str) -> str:
    max_chunk_size = 1024
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []

    current_length = 0
    for sentence in sentences:
        sentence_length = len(nltk.word_tokenize(sentence))
        if current_length + sentence_length <= max_chunk_size:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    summaries = []
    for chunk in chunks:
        try:
            summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            logging.error(f"Error summarizing text: {e}")

    return " ".join(summaries)

def extract_named_entities(doc):
    entities = {}
    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = []
        entities[ent.label_].append(ent.text)
    return entities

def calculate_relevance_score(sentence: str, keyword: str) -> float:
    keyword_position = sentence.lower().index(keyword.lower())
    sentence_length = len(sentence)
    return 1 - (keyword_position / sentence_length)

def find_sentences_with_keywords(doc, keywords: List[str]) -> Dict[str, List[KeywordPosition]]:
    keyword_positions = {keyword: [] for keyword in keywords}
    
    for i, sent in enumerate(doc.sents):
        sentence_text = sent.text.strip()
        sentence_lower = sentence_text.lower()
        for keyword in keywords:
            if keyword.lower() in sentence_lower:
                keyword_positions[keyword].append(KeywordPosition(
                    sentence=sentence_text,
                    position=i,
                    relevance_score=calculate_relevance_score(sentence_text, keyword)
                ))
    
    return keyword_positions

def calculate_keyword_density(doc, keywords: List[str]) -> Dict[str, float]:
    word_count = len(doc)
    keyword_counts = Counter(token.text.lower() for token in doc if token.text.lower() in keywords)
    return {keyword: count / word_count * 100 for keyword, count in keyword_counts.items()}