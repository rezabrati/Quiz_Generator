# model.py
import openai

class QuizGenerator_model:
    def __init__(self, api_key, base_url):
        # Initialize the OpenAI client
        openai.api_type = "openai"
        openai.api_key = api_key
        openai.api_base = base_url

    def answer(self, num_quiz, quiz_format, diff_level, context):

        client = openai.OpenAI(
           base_url= openai.api_base,
           api_key=openai.api_key,)

        response = client.chat.completions.create(
            model="accounts/fireworks/models/llama-v3p1-405b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are syntax validator and an expert quiz maker. Generate quizzes based on the provided {context}. "
                        f"Be precise in following the required output format, ensuring there are no syntax errors, "
                        f"such as mismatched parentheses, brackets, or quotes. If an answer requires a closing parenthesis, "
                        f"bracket, or quote, ensure it is included. "
                        f"Respond only with the questions and answers in the following exact Python dictionary format:\n\n"
                        f"{{\n"
                        f'"Question 1": ("question context", ["1) Option A", "2) Option B", "3) Option C", "4) Option D"], "Correct answer is option 4"),\n'
                        f'"Question 2": ("question context", ["1) Option A", "2) Option B", "3) Option C", "4) Option D"], "Correct answer is option 2")\n'
                        f"}}\n\n"
                        f"Do not include any additional text or explanations."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Please create a {num_quiz}-question quiz in {quiz_format} format. "
                        f"The difficulty level should be {diff_level}. "
                        f"Provide each question with exactly one correct answer, and ensure the response is error-free "
                        f"and correctly formatted as per the specified Python dictionary format."
                    )
                }
            ]
        )
        return response.choices[0].message.content


    def validate_and_format_quiz(self, context):

        client = openai.OpenAI(
           base_url= openai.api_base,
           api_key=openai.api_key,)

        try:
            response = client.chat.completions.create(
                model="accounts/fireworks/models/llama-v3-8b-instruct",
                messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a syntax validator. Check the provided context for syntax correctness and modify it if necessary."
                        "Be precise in following the required output format, ensuring there are no syntax errors, such as mismatched parentheses, brackets, or quotes. "
                        "If an answer requires a closing parenthesis, bracket, or quote, ensure it is included."
                        "Expected output format:\n\n"
                        "{\n"
                        '"Question 1": ("question context", ["1) Option A", "2) Option B", "3) Option C", "4) Option D"], "Correct answer is option 4"),\n'
                        '"Question 2": ("question context", ["1) Option A", "2) Option B", "3) Option C", "4) Option D"], "Correct answer is option 2")\n'
                        "}\n\n"
                        "If the output does not strictly match this format, it should not be returned. Please output only the modified content."
                    )
                },
                {
                    "role": "user",
                    "content": f"Check and modify the following {context}."
                    "Output only the modified content, nothing else."
                }
            ]
        )
            # Return the formatted content if the response is available
            return response.choices[0].message.content if response.choices else "No response received."
        
        except Exception as e:
            # Catch and log exceptions for debugging purposes
            return f"An error occurred: {str(e)}"

