import docx
import json

def parse_docx(file_path):
    doc = docx.Document(file_path)
    faqs = []
    current_faq = {}
    state = "START" # START, QUESTIONS, ANSWER
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
            
        if text.lower().startswith("intent:"):
            if current_faq:
                faqs.append(current_faq)
            current_faq = {"intent": text.split(":", 1)[1].strip(), "questions": [], "answer": ""}
            state = "START"
        elif "sample utterances" in text.lower():
            state = "QUESTIONS"
        elif text.lower().startswith("answer:") or text.lower().startswith("response:"):
            state = "ANSWER"
            # If the answer line itself has content, add it
            parts = text.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                current_faq["answer"] += parts[1].strip() + "\n"
        else:
            if state == "QUESTIONS":
                current_faq["questions"].append(text)
            elif state == "ANSWER":
                current_faq["answer"] += text + "\n"
    
    if current_faq:
        faqs.append(current_faq)
            
    return faqs

if __name__ == "__main__":
    faqs = parse_docx("GRA_Ecommerce_Chatbot_Intents_FAQs.docx")
    with open("extracted_faqs.json", "w") as f:
        json.dump(faqs, f, indent=2)
    print(f"Extracted {len(faqs)} FAQs")
