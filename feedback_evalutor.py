from transformers import pipeline

# Free HF model for feedback (text-generation)
feedback_generator = pipeline("text-generation", model="bigscience/bloom-560m")

def evaluate_answer(question, answer):
    prompt = f"Evaluate this answer for the question: {question}\nAnswer: {answer}\nProvide concise feedback:"
    output = feedback_generator(prompt, max_length=100, do_sample=True, top_p=0.95, num_return_sequences=1)
    feedback = output[0]['generated_text'].strip()
    return feedback
