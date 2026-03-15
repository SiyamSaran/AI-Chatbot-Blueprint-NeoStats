from fpdf import FPDF
import io

def export_chat_to_pdf(messages):
    """
    Exports the chat history to a PDF file and returns the bytes.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Use a Unicode-safe built-in font
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, "NeoStats ChatBot History", ln=True, align='C')
    pdf.ln(10)
    
    for msg in messages:
        role = msg["role"].capitalize()
        content = msg["content"]
        
        # Clean content of characters that might break standard fonts
        content = content.encode('latin-1', 'replace').decode('latin-1')
        
        # Role Header
        pdf.set_font("helvetica", 'B', 12)
        pdf.cell(0, 10, f"{role}:", ln=True)
        
        # Content
        pdf.set_font("helvetica", size=11)
        # Using multi_cell for wrapping text
        pdf.multi_cell(0, 10, content)
        pdf.ln(5)
        
    # Return PDF as bytes
    # dest='S' returns the PDF as a string (or bytearray in some versions)
    content = pdf.output(dest='S')
    if isinstance(content, str):
        return content.encode('latin-1')
    return bytes(content)
