import openai
import streamlit as st
import PyPDF2


# Initialize OpenAI client
client = openai.OpenAI(
    base_url = "https://api.fireworks.ai/inference/v1",
    api_key="fw_3ZYkiWjHCT8XV74Nu7AN6grN",
)

# Function to extract text from a PDF
def extract_data(uploaded_file):
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    
    # Initialize an empty string to hold the text
    extracted_text = ""
    
    # Loop through all the pages in the PDF
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        extracted_text += page.extract_text()
    
    return extracted_text

# Function to generate the quiz
def answer(num_quiz, quiz_format, diff_level, context):
    response = client.chat.completions.create(
        model="accounts/fireworks/models/llama-v3-8b-instruct",
        messages=[
            {
            "role": "system",
            "content": f"You are an expert quiz maker. You generate quizzes based on the given {context}. " \
            "Just give me questions and answers and do not add anything else. " \
            "For multiple-choice and true/false questions, format the options like this:\n\n" \
            "1- What is the capital of Iran?\n" \
            "   1) Tehran   2) Rasht   3) Paris   4) Mashhad\n\n" \
            "Please write the answers in a numbered list at the end, do not use bold font."
            },
            {
                "role": "user",
                "content": f"Please create a {num_quiz}-question quiz in {quiz_format} format. The difficulty level should be {diff_level}. At the end, provide the answers in a numbered list without any explanation."
            }
        ],
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("AI Quiz Generator")

col1, col2 = st.columns(2)
with col1:

    # Create a file uploader for the PDF file
    uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
    
    context = ""
    if uploaded_file is not None:
        # Extract text from the PDF file
        context = extract_data(uploaded_file)

    num_quiz = st.selectbox("Number of Questions", [1, 2, 5, 10])
    quiz_format = st.selectbox("Quiz Format", ["true/false", "multiple choice", "short answer"])
    diff_level = st.selectbox("Difficulty Level", ["easy", "medium", "hard"])
    s =st.button("Generate Quiz")

with col2:
    # Button to generate the quiz
    if s:
        with st.spinner("Generating your quiz..."):
            # Call the answer function to generate the quiz
            quiz = answer(num_quiz, quiz_format, diff_level,context)
            
            # Display the quiz in a text box
            st.text_area("Generated Quiz", value=quiz, height=300)

            # Add a download button for the generated quiz
            st.download_button(
                label="Download",
                data=quiz,
                file_name="quiz.txt",
                mime='text/plain'
            )
