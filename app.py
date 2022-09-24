# Import the necessary libraries
import streamlit as st 
import requests
import pandas as pd

# Get the API key from the user
api_key = st.sidebar.text_input("Type OneAI API Key and press Enter:", type="password")

st.sidebar.write("Made with ❤️ by [@Saboo_Shubham_](https://twitter.com/Saboo_Shubham_)")

# Set the title of the app
st.title('🎧 Analyze Customer Support Converstaions')

# Set the subtitle of the app
st.write('**_This application uses the OneAI API to analyse customer centre data._**')  

st.image('poster.png', use_column_width=True)

# Sample Call Centre Conversation
conversation = """
Customer:
Hi, I'm having trouble with my account.
Agent:
Hi, I'm sorry to hear that. What seems to be the problem?
Customer:
I can't log in.
Agent:
I'm sorry to hear that. Can you tell me what happens when you try to log in?
Customer:
I get an error message.
Agent:
What does the error message say?
Customer:
It says my password is incorrect.
Agent:
Can you try resetting your password?
Customer: 
That worked, thank you."""

st.markdown('### **Sample Call Centre Conversation** 📝')
st.text(conversation)



# Input the text to be analysed
input = st.text_area('Enter the converstation with customer here 👇')

# Select the insights to be returned
skills = [st.selectbox('Select an intelligence feature 🕹', ['summarize', 'names', 'emotions', 'sentiments', 'article-topics'])]
print(skills[0])

# split the input into a list of sentences and store in two lists
def split_conversation(conversation):
    speakers = []
    utterances = []
    for line in conversation.split('\n'):
        line = line.rstrip()
        if line.strip():
            if line.endswith(':'):
                speakers.append(line.strip(':'))
            else:
                utterances.append(line)
    return speakers, utterances



url = "https://api.oneai.com/api/v0/pipeline"

# Set the headers
headers = {
  "api-key": api_key, 
  "content-type": "application/json"
}


# create a button to call the API
if st.button('Analyse'):
        
    speakers, utterance = split_conversation(input)

    # create a dictionary with the key input and the value as a list of dictionaries
    input_dict = {"input": []}
    # loop through the speakers and utterances lists and create a dictionary for each speaker and utterance
    for i in range(len(speakers)):
        # create a dictionary with the speaker and utterance
        speaker_utterance = {"speaker": speakers[i], "utterance": utterance[i]}
        # append the dictionary to the list
        input_dict["input"].append(speaker_utterance)
    
    payload = {
        "input": input_dict["input"],
        "input_type": "conversation",
            "content_type": "application/json",
        "steps": [
            {
            "skill": skills[0]
            }
        ],
    }

    r = requests.post(url, json=payload, headers=headers)
    data = r.json()

    # create a dataframe from the data
    if 'summarize' in skills:
        st.subheader("Conversation Summary")
        st.write(data["output"][0]["text"])
    
    if 'names' in skills:
        st.subheader("Named Entity Recognition")
        df = pd.DataFrame(columns=['skill', 'name', 'speaker', 'value'])

        for i in range(len(data['output'][0]['labels'])):
            df.loc[i] = [data['output'][0]['labels'][i]['skill'], data['output'][0]['labels'][i]['name'], data['output'][0]['labels'][i]['speaker'], data['output'][0]['labels'][i]['span_text']]

        st.write(df[df["skill"]=="names"])

    if 'emotions' in skills:
        st.subheader("Emotion Detection")
        df = pd.DataFrame(columns=['skill', 'name', 'speaker', 'value'])

        for i in range(len(data['output'][0]['labels'])):
            df.loc[i] = [data['output'][0]['labels'][i]['skill'], data['output'][0]['labels'][i]['name'], data['output'][0]['labels'][i]['speaker'], data['output'][0]['labels'][i]['span_text']]

        st.write(df[df["skill"]=="emotions"])

    if 'sentiments' in skills:
        st.subheader("Sentiments Analysis")
        df = pd.DataFrame(columns=['skill', 'type', 'speaker', 'span_text'])

        for i in range(len(data['output'][0]['labels'])):
            df.loc[i] = [data['output'][0]['labels'][i]['skill'], data['output'][0]['labels'][i]['value'], data['output'][0]['labels'][i]['speaker'], data['output'][0]['labels'][i]['span_text']]

        st.write(df)

    if 'article-topics' in skills:
        st.subheader("Topic Detection")
        df = pd.DataFrame(columns=['skill', 'value'])

        for i in range(len(data['output'][0]['labels'])):
            st.code("#"+data['output'][0]['labels'][i]['value'])

        
