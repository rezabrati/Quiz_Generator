# AI Quiz Generator 📝

AI Quiz Generator is a Streamlit-based web application that lets users upload a PDF file and generate a customizable quiz. With this tool, users can select quiz parameters such as the number of questions, question format, and difficulty level. The quiz is then auto-generated from the PDF content, and users can complete it in-app with real-time feedback on their answers.

## Features
- **PDF Upload**: Upload any PDF file to generate quiz content.
- **Customizable Quiz Parameters**:
  - **Number of Questions**: Choose from 1, 2, 5, or 10 questions.
  - **Quiz Format**: Select question types, including true/false, multiple choice, or short answer.
  - **Difficulty Level**: Set difficulty to easy, medium, or hard.
- **Real-time Feedback**: After submitting answers, the app provides a score with correct and incorrect answers highlighted.
- **Percentage Score Display**: View your score in percentage format.

## Installation

### Option 1: Local Installation

Follow these steps to install and run the application on your local machine.


1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/AI-Quiz-Generator.git
    cd AI-Quiz-Generator
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    
3. Set Up API Credentials:
    Create a .env file in the project directory with the following contents:
    ```python
    API_KEY = "your_api_key"
    BASE_URL = "your_base_url"
    ```
    
4. Run the App Locally:
    ```bash
    streamlit run main.py
    ```  
### Option 2: Run with Docker

The application can also be run using Docker for a simplified and portable setup.

1. Pull the Docker Image:
    ```bash
    docker pull baratireza/quiz-generator-2024
    ```

2. Run the Container:
   - If you have a .env file with your API credentials:
    ```bash
    docker run --env-file .env -p 8501:8501 baratireza/quiz-generator-2024
    ```
   - Alternatively, pass API credentials directly as environment variables:
    ```bash
    docker run -p 8501:8501 -e API_KEY=your_api_key -e BASE_URL=your_base_url baratireza/quiz-generator-2024
    ```

3. Access the App: Open your browser and navigate to http://localhost:8501.

    
## Usage

1. **Upload a PDF File**:  
   Upload a `.pdf` file containing the content for quiz questions.

2. **Set Quiz Preferences**:  
   - Number of Questions  
   - Quiz Format (e.g., multiple choice, true/false)  
   - Difficulty Level  

3. **Generate the Quiz**:  
   Click **Generate Quiz** to create a quiz from the PDF content.

4. **Answer the Questions**:  
   Select answers for each question.

5. **Review Results**:  
   After submission, view your:  
   - Correct and incorrect answers for each question.  
   - Total score displayed as a percentage.


## Code Overview

- **app.py**: Main file for the Streamlit app interface and quiz logic.
- **model/QuizGenerator_model**: Model for quiz generation, which interacts with external APIs.
- **utils/QuizGenerator**: Utility for handling PDF content extraction and quiz formatting.

## Example Workflow

1. **Upload a PDF**: Start by uploading a `.pdf` file containing the content for quiz questions.
2. **Set Quiz Preferences**: Choose the number of questions, format, and difficulty.
3. **Generate and Answer the Quiz**: Questions are generated and displayed with options for user interaction.
4. **Review Results**: After submission, receive feedback and a percentage score.

## Notes
- The `quiz_generator.answer()` function is expected to interact with an external API to generate quiz content. Ensure that your API credentials are correctly set up.
- Some helper functions such as `extract_data` and `extract_quiz_data` are defined to process the PDF data and format the questions.


