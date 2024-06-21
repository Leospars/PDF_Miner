import logging
from dotenv import load_dotenv
from pdf_extract import extracted
import google.generativeai as genai
import os

if __name__ == '__main__':
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    chatModel = genai.GenerativeModel("gemini-1.5-flash")


    def sanitize_data(extracted=extracted):
        """ Remove any sensitive or inappropriate content from the data
            before sending it to the model
        """
        return extracted


    def train_chat_response(questions, answers):
        if (len(questions) != len(answers)):
            logging.error("Questions and answers must be of equal length")
            return

        chat = chatModel.start_chat(
            history=[
                {"role": "user", "parts":
                    f"""Please respond to each question with standard format json code so that your 
                        response can easily convertible to code, responding with markdown syntax will not make this possible.
                        Also for any data that can be listed and comma seperated values should be written as an array. For example, if you
                        have a list of experience you should write it as 'Experience': [experience1, experience2, experience3],. 
                        Respond ALWAYS respond as plain text NEVER markdown."""
                 },
                {"role": "model", "parts": "I understand and I will only respond with your following question in easily "
                                           "convertible plain text json format."},
            ]
        )
        return chat


    def infer_data(extracted=extracted):
        extracted = sanitize_data(extracted)
        chat = train_chat_response(["What university does client attend here",
                                    "what did year the student started university"],
                                   ['{ "University" : Amigo Universidad }', '{ "year" : 2019 }'])

        def get_chat_response(question, context):
            print(f"Question: {question}")
            return chat.send_message(f"Context: [{context}]\n Question: {question}").text

        print('Inferred Data: \n\x1b[32m')  # Print text green
        errMessage = "if information not found say 'None'."
        response = get_chat_response("What university does client attend here", f"Education: {extracted['Education']}")
        print("University Attended: " + response)

        response = get_chat_response("what did year the student started university",
                                     f"Education: {extracted['Education']}")
        print("Started: " + response)

        requirements = ["Two programming language, 100%", "One year experience, 100%", "Completed Projects:"
                        "2 impactful projects = 100%, 1 partial impactful: 40%", "web development, intermediate proficiency: 80%"]
        context = f"Requirements include {requirements}. Experience: {extracted['Experience']}."
        response = get_chat_response("Match any experience given with the listed requirements and state an estimated"
                                     "percentage of how closely each section matches with the client info.", context)
        print("Experience: " + response)


    infer_data()
