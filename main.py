import config
from model import QuizGenerator_model
from utils import QuizGenerator
import streamlit as st


# Streamlit UI
st.title("🤖 AI Quiz Generator 📝")

uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
quiz_gen = QuizGenerator(uploaded_file)
quiz_generator = QuizGenerator_model(config.API_KEY, config.BASE_URL)


co1, co2, co3 = st.columns(3)

context = ""
if uploaded_file is not None:
    # Here you would define a function to extract data from the PDF
    context = quiz_gen.extract_data()

with co1:
    num_quiz = st.selectbox("Number of Questions", [1, 2, 5, 10])
with co2:
    quiz_format = st.selectbox("Quiz Format", ["true/false", "multiple choice", "short answer"])
with co3:    
    diff_level = st.selectbox("Difficulty Level", ["easy", "medium", "hard"])

# Create a horizontal layout for the "Generate Quiz" button
generate_col = st.columns(1)
with generate_col[0]:
    s = st.button("Generate Quiz")

col2, col3 = st.columns(2)

# State to check if quiz has been generated
if 'quiz_generated' not in st.session_state:
    st.session_state.quiz_generated = False

with col2: 
    if s:
        with st.spinner("Generating your quiz..."):
            # Assume `answer` and `extract_quiz_data` are defined functions
            quiz_text = quiz_generator.answer(num_quiz, quiz_format, diff_level, context)
            questions, correct_answers = quiz_gen.extract_quiz_data(quiz_text)

            # Store questions and correct answers in session state
            st.session_state['questions'] = questions
            st.session_state['correct_answers'] = correct_answers

            # Update quiz_generated state
            st.session_state.quiz_generated = True  # Set this to True after quiz generation

    if 'questions' in st.session_state and 'correct_answers' in st.session_state:
        questions = st.session_state['questions']
        correct_answers = st.session_state['correct_answers']

        user_answers = []

        # Open scroll-box div
        with st.container(height=400):
            for idx, question in enumerate(questions):
                # Split the question string into question and options
                q_text, q_options = question.split(" Options: ")
                q_options = q_options.split(", ")  # Split options into a list
                
                # Display question text in scrollable box
                st.markdown(f"**Q{idx + 1}: {q_text}**")
                
                # Display options as radio buttons for multiple-choice questions
                user_answer = st.radio(f"Choose your answer for question {idx + 1}:", q_options, key=f"q_{idx}")
                
                user_answers.append(user_answer)

# Create a horizontal layout for buttons
button_col1, button_col2 = st.columns([2, 1])  # Adjust the width ratio if needed

with button_col1:
    if st.session_state.quiz_generated:  # Show the button only if the quiz has been generated
        s2 = st.button("Submit Answers")

with button_col2:
    # If the quiz has been generated, you can also show other buttons here if needed
    pass

if st.session_state.quiz_generated:
    with col3:
        # Button to submit answers
        if s2:
            with st.container(height=400):
                # Compare user's answers with the correct ones
                for idx, user_answer in enumerate(user_answers):
                    correct_answer = correct_answers[idx]
                    correct_answer_text = correct_answer.split(") ")[1].strip()
                    
                    st.write(f"{questions[idx].split(' Options: ')[0]}")  # Display the question text
                    st.write(f"Your answer: {user_answer}")
                    st.write(f"Correct answer: {correct_answer_text}")
                    
                    # Check if the user's answer matches the correct answer
                    if user_answer.strip() == correct_answer.strip():
                        st.write("✅ Correct")
                    else:
                        st.write("❌ Incorrect")
