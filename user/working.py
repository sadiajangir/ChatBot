import random
import json
import pickle
import numpy as np
import nltk
import os
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from keras.models import load_model
import spacy
doc_nlp = spacy.load('en_core_web_sm')

cwd = os.getcwd()

lemmatizer = WordNetLemmatizer()
intents = json.loads(open(cwd+"/user/bot/intents.json").read())

words = pickle.load(open(cwd+"/user/bot/words.pkl", "rb"))
classes = pickle.load(open(cwd+"/user/bot/classes.pkl", "rb"))
model = load_model(cwd+"/user/bot/chatbot_model.h5")

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def store_log(message, response):
    with open(cwd+"/user/bot/log_ML.txt", "a") as log:
        log.write(f"User:\t{message}\n")
        log.write(f"Bot:\t{response}\n")

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append(
            {'intent': classes[r[0]], 'probability': str([r[1]])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def response(message):
    if message.startswith("ENTITIES:"):
        doc = doc_nlp(message[9:])
        res = f"Here is a list of entities with NER {[(ent.text, spacy.explain(ent.label_)) for ent in doc.ents]}"
        store_log(message, res)
        return res
    
    
    if message.startswith("POS:"):
        doc = doc_nlp(message[4:])
        res =f"Here is a list of Parts of Speech {[(word.text, spacy.explain(word.pos_)) for word in doc]}"
        store_log(message, res)
        return res


    ints = predict_class(message)
    res = get_response(ints, intents)
    store_log(message, res)
    return res