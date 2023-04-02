from googleapiclient.discovery import build
import requests
import os
import googleapiclient.discovery

api_key = 'AIzaSyDgZDUHl1BoYUExQjjWG2hbOvZQdT6z4Gs'

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "YOUR_API_KEY"

youtube = build('youtube', 'v3', developerKey=api_key)


def all_comments(video_link):
    video_Id = video_link.strip().split('=')[1]
    l1 = []
    request = youtube.commentThreads().list(
        part="snippet",
        order="time",
        videoId=video_Id
    )
    response = request.execute()

    for i in range(len(response['items'])):
        l1.append(response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])

    while 'nextPageToken' in response.keys():
        request = youtube.commentThreads().list(
            part="snippet",
            order="time",
            pageToken=response['nextPageToken'],
            videoId=video_Id
        )
        response = request.execute()
        for i in range(len(response['items'])):
            l1.append(response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])


    s = ' '.join(l1)
    return s

#################################################################################



import streamlit as st
import pickle

st.title('SENTIMENTS OF YOUTUBE COMMENT SECTION')
input_key = st.text_input('Enter Your Youtube Video link')

if st.button('check'):

    comment = all_comments(input_key)






    # **TEXT PREPERATION**

    #LOWER CASING
    comment = comment.lower().strip()

     # Removing html tags
    import re


    def html_rem(tex):
        pattern = re.compile(r'<.*?>')
        return pattern.sub(r'', tex)


    comment = html_rem(comment)


    # Removing URL's
    def url(tex):
        pattern = re.compile(r'https?://\S+|www\.\S+')
        return pattern.sub(r'', tex)


    comment = url(comment)







    # Replacing meaning of emoji
    import emoji


    def demo(textx):
        return emoji.demojize(textx)


    comment = demo(comment)

    contractions = {
        "ain't": "am not",
        "aren't": "are not",
        "can't": "can not",
        "can't've": "can not have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he'll've": "he will have",
        "he's": "he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how is",
        "i'd": "i would",
        "i'd've": "i would have",
        "i'll": "i will",
        "i'll've": "i will have",
        "i'm": "i am",
        "i've": "i have",
        "isn't": "is not",
        "it'd": "it would",
        "it'd've": "it would have",
        "it'll": "it will",
        "it'll've": "it will have",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she would",
        "she'd've": "she would have",
        "she'll": "she will",
        "she'll've": "she will have",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so as",
        "that'd": "that would",
        "that'd've": "that would have",
        "that's": "that is",
        "there'd": "there would",
        "there'd've": "there would have",
        "there's": "there is",
        "they'd": "they would",
        "they'd've": "they would have",
        "they'll": "they will",
        "they'll've": "they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we would",
        "we'd've": "we would have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what'll've": "what will have",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "when's": "when is",
        "when've": "when have",
        "where'd": "where did",
        "where's": "where is",
        "where've": "where have",
        "who'll": "who will",
        "who'll've": "who will have",
        "who's": "who is",
        "who've": "who have",
        "why's": "why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "you'd": "you would",
        "you'd've": "you would have",
        "you'll": "you will",
        "you'll've": "you will have",
        "you're": "you are",
        "you've": "you have"
    }


    def deco(q):
        q_decontracted = []

        for word in q.split():
            if word in contractions:
                word = contractions[word]

            q_decontracted.append(word)

        q = ' '.join(q_decontracted)
        q = q.replace("'ve", " have")
        q = q.replace("n't", " not")
        q = q.replace("'re", " are")
        q = q.replace("'ll", " will")

        return q


    comment = deco(comment)



    # Removing Punctuation
    import string

    exclude = string.punctuation


    def remove_punc1(text):
        return text.translate(str.maketrans('', '', exclude))


    comment = remove_punc1(comment)



    # Stops word removal

    import spacy
    from spacy.lang.en.stop_words import STOP_WORDS


    def remove_stopwords(text):
        new_text = []

        for word in text.split():
            if word in STOP_WORDS:
                new_text.append('')
            else:
                new_text.append(word)
        x = new_text[:]
        new_text.clear()
        return " ".join(x)


    comment = remove_stopwords(comment)




    # # Stemming
    #import nltk
    # from spacy.load('en_core_web_sm')
    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load("en_core_web_sm")

    def stem_words(text):
        doct = nlp(text)
        return " ".join([word.lemma_ for word in doct])


    comment = stem_words(comment)


    #st.header(comment)




    tfidf = pickle.load(open('vectorizers.pkl_','rb'))
    model = pickle.load(open('models.pkl_','rb'))

    #** VECTORIZING
    vector_input = tfidf.transform([comment])


    # 3. predict
    result = model.predict(vector_input)[0]
    # 4. Display
    if result == 1:
        st.header("Positive")
    else:
        st.header("Negative")

