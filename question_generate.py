from transformers import pipeline

# Hugging Face free model for question generation
generator = pipeline("text-generation", model="bigscience/bloom-560m")  # Free & lightweight

def generate_questions(prompt, num_questions=5):
    output = generator(prompt, max_length=200, do_sample=True, top_p=0.95, num_return_sequences=1)
    text = output[0]['generated_text']

    # Split by newlines or simple splitting logic
    questions = []
    for line in text.split('\n'):
        line = line.strip()
        if line and len(questions) < num_questions:
            questions.append(line)
    # Ensure exactly num_questions
    while len(questions) < num_questions:
        questions.append("Sample question?")
    return questions[:num_questions]
