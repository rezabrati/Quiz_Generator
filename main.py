import config
from model import QuizGenerator_model
from utils import QuizGenerator
import streamlit as st
import time

# Streamlit UI
st.title("AI Quiz Generator 📝")

uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")    
quiz_gen = QuizGenerator(uploaded_file)
quiz_generator = QuizGenerator_model(config.API_KEY, config.BASE_URL)

co1, co2, co3 = st.columns(3)

context = ""
if uploaded_file is not None:
    context = quiz_gen.extract_data()

with co1:
    num_quiz = st.selectbox("Number of Questions", [1, 2, 5, 10])
with co2:
    quiz_format = st.selectbox("Quiz Format", ["true/false", "multiple choice"])
with co3:    
    diff_level = st.selectbox("Difficulty Level", ["easy", "medium", "hard"])

# Timer based on number of questions (30 seconds per question)
exam_duration = num_quiz * 30
if 'time_left' not in st.session_state:
    st.session_state.time_left = exam_duration

# Create a horizontal layout for the "Generate Quiz" button
generate_col = st.columns(1)
with generate_col[0]:
    s = st.button("Generate Quiz")

# State to check if quiz has been generated
if 'quiz_generated' not in st.session_state:
    st.session_state.quiz_generated = False
flag2 = False

# Generate Quiz
if s:
    with st.spinner("Generating your quiz..."):
        text = quiz_generator.answer(num_quiz, quiz_format, diff_level, context)
        quiz_text = quiz_generator.validate_and_format_quiz(text)
        questions, correct_answers = quiz_gen.extract_quiz_data(quiz_text)

        # Store questions and correct answers in session state
        st.session_state['questions'] = questions
        st.session_state['correct_answers'] = correct_answers
        st.session_state.quiz_generated = True  # Set this to True after quiz generation

# Display the quiz and start the timer if the quiz is generated
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
            st.markdown(f"**{q_text}**")
            
            # Display options as radio buttons for multiple-choice questions
            user_answer = st.radio(f"Choose your answer for question {idx + 1}:", q_options, key=f"q_{idx}")
            
            user_answers.append(user_answer)
        flag2 = True
        check = True
        flag  = False

    # Countdown timer display with st.empty() for dynamic updates
    timer_placeholder = st.empty()

    # Reduce time left by 1 second every second
    start_time = time.time()
    while st.session_state.time_left > 0 and flag2:

        # Break loop if timer runs out
        if st.session_state.time_left == 0:
            break
        elapsed_time = time.time() - start_time
        st.session_state.time_left = exam_duration - int(elapsed_time)
        timer_placeholder.header(f"Time Left: {st.session_state.time_left} seconds")


        time.sleep(1)
        
        if flag2 and check:  # Show the button only if the quiz has been generated
            s2 = st.button("Submit Answers")
            flag = True

        check =False
        # Auto-submit answers and display results when time is up or if "Submit Answers" clicked
        if st.session_state.time_left <= 0 or s2:
                flag2 = False
                flag = False
                score = 0
                with st.container(height=400):
                    for idx, user_answer in enumerate(user_answers):
                        correct_answer = correct_answers[idx]
                        correct_answer_text = correct_answer.split(") ")[1].strip()
                        
                        st.write(f"{questions[idx].split(' Options: ')[0]}")
                        st.write(f"Your answer: {user_answer}")
                        st.write(f"Correct answer: {correct_answer_text}")
                        
                        if user_answer.strip() == correct_answer.strip():
                            st.write("✅ Correct")
                            score += 1
                        else:
                            st.write("❌ Incorrect")
                
                # Calculate and display the score
                if score > 0:
                    with st.popover("📊 Your Results"):
                        percentage_score = (score / len(questions)) * 100
                        st.markdown(f"### 🎉 Your Score: {percentage_score}%")

       
        
