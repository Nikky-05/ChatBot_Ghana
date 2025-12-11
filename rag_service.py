import json
import os
import google.generativeai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class RAGChatbot:
    def __init__(self, faq_file="extracted_faqs.json"):
        self.faq_file = faq_file
        self.faqs = self._load_faqs()
        self.vectorizer = TfidfVectorizer()
        self.faq_vectors = None
        self.questions = []
        self._prepare_vectors()
        
        # Initialize Gemini Model
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def _load_faqs(self):
        try:
            with open(self.faq_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.faq_file} not found. Please run parse_faqs.py first.")
            return []

    def _clean_question(self, question):
        """Clean question text by removing formatting artifacts"""
        # Remove leading dash and whitespace
        cleaned = question.strip()
        if cleaned.startswith('-'):
            cleaned = cleaned[1:].strip()
        
        # Skip lines that are "Short Answer:" metadata
        if cleaned.lower().startswith('short answer:'):
            return None
            
        return cleaned
    
    def _prepare_vectors(self):
        if not self.faqs:
            return
        
        # Collect all questions for vectorization
        # We will map the index back to the FAQ entry
        self.questions = []
        self.question_to_faq_map = []
        
        for i, faq in enumerate(self.faqs):
            for q in faq.get("questions", []):
                cleaned_q = self._clean_question(q)
                if cleaned_q:  # Only add if not None (skip Short Answer lines)
                    self.questions.append(cleaned_q)
                    self.question_to_faq_map.append(i)
        
        if self.questions:
            self.faq_vectors = self.vectorizer.fit_transform(self.questions)

    def get_relevant_context(self, query, threshold=0.2):
        if not self.faq_vectors is not None:
            return None

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.faq_vectors).flatten()
        
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score < threshold:
            return None
            
        faq_idx = self.question_to_faq_map[best_idx]
        return self.faqs[faq_idx]

    def generate_response(self, query):
        context = self.get_relevant_context(query)
        
        if not context:
            # Fallback if no context found in FAQs
            prompt = f"""
            You are a professional support assistant for GRA (Ghana Revenue Authority) E-commerce compliance.
            The user asked: "{query}"
            
            I couldn't find a specific answer in the FAQ database for this question.
            Please politely inform the user that you don't have that specific information available,
            but you're here to help with other GRA E-commerce compliance questions.
            Keep the tone professional, helpful, and courteous.
            """
        else:
            # Get the answer, clean up if needed
            answer = context.get('answer', '').strip()
            
            # If answer is empty, try to extract from questions (some FAQs have it there)
            if not answer:
                for q in context.get('questions', []):
                    if 'short answer:' in q.lower():
                        answer = q.split(':', 1)[1].strip()
                        break
            
            # RAG Prompt
            prompt = f"""
            You are a professional support assistant for GRA (Ghana Revenue Authority) E-commerce compliance.
            
            User Question: "{query}"
            
            Answer from FAQ Database: {answer}
            
            Instructions:
            1. Provide a clear, professional answer based on the FAQ database information.
            2. Rephrase the answer in a conversational yet professional manner.
            3. Be helpful, accurate, and courteous.
            4. Do NOT add information that isn't in the provided answer.
            5. Keep responses concise and to the point.
            """
            
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties at the moment. Please try again shortly. (Error: {str(e)})"

if __name__ == "__main__":
    bot = RAGChatbot()
    print(bot.generate_response("What is the VAT rate?"))
