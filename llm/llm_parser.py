# llm/llm_parser.py
import os
import PyPDF2
import docx
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai.api_key = OPENAI_API_KEY

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(file)
    all_text = []
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            all_text.append(text)
    return "\n".join(all_text)

def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    doc = docx.Document(file)
    all_text = []
    for paragraph in doc.paragraphs:
        all_text.append(paragraph.text)
    return "\n".join(all_text)

def parse_financial_report(uploaded_file, file_type="pdf"):
    """
    Convert the uploaded_file into text.
    file_type can be 'pdf' or 'docx'.
    """
    if file_type == "pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        return extract_text_from_docx(uploaded_file)
    else:
        return "Unsupported file type"

def generate_llm_summary(parsed_text, model_outputs, risk_analysis):
    """
    Utilize an LLM (e.g. OpenAI) to create a cohesive summary
    that merges the input text (parsed from PDF/DOC), model outputs, and risk data.
    
    This function returns a text summary from the LLM. Expand the prompt as needed.
    """
    if not OPENAI_API_KEY:
        # Return a mock response if no key is set
        return (
            "LLM Summary (Mock): The financial report indicates strong fundamentals. "
            "Model outputs suggest positive cash flows, and risk analysis remains stable."
        )
    
    prompt = f"""
The user has provided a financial research report with the following text:
---
{parsed_text}
---
We also have these model outputs:
{model_outputs}

And a risk analysis:
{risk_analysis}

Combine all this information into a cohesive summary of the company's financial situation, 
covering key takeaways, data insights, potential risks, and an overall conclusion.
Respond in a professional tone, with bullet points where helpful.
    """

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("OpenAI error:", e)
        return "LLM error. Could not generate summary."
