from fpdf import FPDF

def generate_report(questions, answers, feedbacks, file_name="interview_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Smart Interview Simulator Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)
    for i, (q, a, f) in enumerate(zip(questions, answers, feedbacks)):
        pdf.multi_cell(0, 8, f"Q{i+1}: {q}")
        pdf.multi_cell(0, 8, f"Your Answer: {a}")
        pdf.multi_cell(0, 8, f"Feedback: {f}")
        pdf.ln(5)

    pdf.output(file_name)
    return file_name
