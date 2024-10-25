import PyPDF2
import ast
import re

class QuizGenerator:
    def __init__(self, uploaded_file=None):
        self.uploaded_file = uploaded_file
        self.context = ""
        self.questions_with_options = []
        self.correct_answers = []

    def extract_data(self):
        """Extract text from the uploaded PDF file."""
        if self.uploaded_file is None:
            raise ValueError("No file uploaded.")
        pdf_reader = PyPDF2.PdfReader(self.uploaded_file)
        extracted_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text()
        self.context = extracted_text
        return self.context

    @staticmethod
    def correct_and_balance_braces(input_string):
        """Correct unbalanced braces in the input string."""
        open_count = input_string.count('{')
        close_count = input_string.count('}')
        
        if open_count > close_count:
            corrected_string = input_string + '}' * (open_count - close_count)
        elif close_count > open_count:
            corrected_string = '{' * (close_count - open_count) + input_string
        else:
            corrected_string = input_string
        
        return corrected_string

    def extract_quiz_data(self, output):
        """Extract quiz questions and correct answers from the output."""
        corrected_output = self.correct_and_balance_braces(output)
        output_dict = ast.literal_eval(corrected_output)
        
        self.questions_with_options = []
        self.correct_answers = []
        
        for key, value in output_dict.items():
            question = value[0]
            options = value[1]
            correct_answer_str = value[2]
            correct_answer_index = int(re.search(r'\d+', correct_answer_str).group())
            correct_answer = options[correct_answer_index - 1]
            
            question_with_options = f"{key}: {question} Options: {', '.join(options)}"
            self.questions_with_options.append(question_with_options)
            self.correct_answers.append(correct_answer)
        
        return self.questions_with_options, self.correct_answers