import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to scrape questions from the website
def scrape_questions(url):
    response = requests.get(url, verify=False)  # Disable SSL verification
    soup = BeautifulSoup(response.content, 'html.parser')
    question_elements = soup.find_all('div', class_='bix-div-container')

    questions = []
    for idx, question_elem in enumerate(question_elements):
        question_text = question_elem.find('div', class_='bix-td-qtxt').get_text()
        options = question_elem.find_all('div', class_='bix-td-option')
        options_text = [opt.get_text() for opt in options]
        
        # Check if correct option element exists before extracting text
        correct_option_elem = question_elem.find('div', class_='jq-hdnakqb')
        correct_option = correct_option_elem.get_text() if correct_option_elem else "Correct option not found"
        
        questions.append({
            'question': question_text,
            'options': options_text,
            'correct_option': correct_option
        })

    return questions

# Main function to run the Streamlit app
def main():
    st.title("Electronics Quiz App")

    # Container with your name
    with st.container():
        st.subheader("Created by Siddhanth")
        st.write("This is a quiz app that fetches questions from a website.")

    # Scrape questions from the provided website
    url = "https://www.indiabix.com/electronics-and-communication-engineering/materials-and-components/"
    questions = scrape_questions(url)

    # Display questions and collect user answers
    for idx, question in enumerate(questions):
        st.subheader(f"Question {idx + 1}: {question['question']}")
        
        # Debug print statements
        print("Options:", question['options'])  # Print options
        
        selected_option = st.radio("Select an option:", question['options'], key=f"q{idx}")
        submit_button = st.button("Submit", key=f"s{idx}")

        if submit_button:
            if selected_option == question['correct_option']:
                st.write("Correct!")
            else:
                st.write("Incorrect. The correct answer is:", question['correct_option'])

        # Show the correct answer after submitting
        if submit_button:
            st.write(f"Correct answer: {question['correct_option']}")

if __name__ == "__main__":
    main()
