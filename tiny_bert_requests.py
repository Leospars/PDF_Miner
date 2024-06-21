from pdf_extract import cls, keywords
from colorama import Fore as Color
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

cls()
tokenizer = AutoTokenizer.from_pretrained("Intel/dynamic_tinybert")
model = AutoModelForQuestionAnswering.from_pretrained("Intel/dynamic_tinybert")

def tinybertLM(prompt:str, context:str, max_length=1000) :  
    print("Cleaning up context...")
    for char in context:
        if char in [ "•", "*"] :
            context = context.replace(char, '\b.\n') 

    for word in keywords:
        if (index := context.find(word)) != -1:
            endOfSentence = context.find(".", index)
            context = context[index:endOfSentence]
            break
    
    print("New Context: " + Color.YELLOW + context + Color.RESET)

    if len(context) > max_length:
        print("Context too long, truncating...")
        print( "Removing: " + Color.RED + context[max_length:] + Color.RESET)
        context = context[:max_length]
        
        print( "New Context: " + Color.GREEN + context + Color.RESET)

    tokens = tokenizer.encode_plus(
        prompt, 
        context,
        add_special_tokens=True,
        max_length=max_length, 
        return_tensors="pt",
        padding=True,
        truncation=True
    )
    
    # Get the input IDs and attention mask
    input_ids = tokens["input_ids"]
    attention_mask = tokens["attention_mask"]

    # Perform question answering
    outputs = model(input_ids, attention_mask=attention_mask)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # Find the start and end positions of the answer
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores) + 1
    return (response := tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[0][answer_start:answer_end])))

context = "Education: University of the West Indies, Mona (2023-26) • Recipient of New Fortress Energy Full Scholarship given to 10 students per academic year,\
    nationally, for outstanding academic performance, financial need and demonstrable community involvement and leadership qualities • Pursuing a BSc. in Electronics Engineering, \
    I am currently a member of Semester 1 (2023) Dean’s List; 1st year included completing 13 rigorous courses over the maximum credit which covered C, C++, Arduino, Java (OOP), \
    Android, MySQL, MATLAB, CAD, Calculus (I, II and III), Electronics, and other tools for engineering applications. Jamaica College Sixth Form (2021-23) • Passed all 10 Cape Units,\
    more rigorous than required. Perfect score (Distinction): Computer Science (CS) Unit 1&2 and Physics Unit 1&2. • National Merit List (2023): 23rd CS Unit 2, 26th Integrated Mathematics,\
    and Physics Unit 2. Jamaica College (2016-21) • GPA: 3.81. Passed 9 CSEC Subjects. Perfect score: Mathematics, Chemistry, Physics, IT. • National Merit List (2021): 36th in Industrial Technology: \
    Electrical Engineering. • Clubs and Societies: Prefect Body, Jamaica College Chess Team, STEM Club, Robotics Club"

prompt = "What university is attended?"

# Print the answer
print("Answer:", answer := tinybertLM(prompt, context))
