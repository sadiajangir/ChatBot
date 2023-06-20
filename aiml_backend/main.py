import os
import glob
import re
import spacy
from pyaiml21 import Kernel
from random import randint
from transformers import pipeline
from py2neo import Graph, Node, Relationship
from huggingface_hub import notebook_login


class ChatSession:
    def __init__(self, spacy_model, module_directory, files_directory, ):
        self.base_path = os.path.join(os.getcwd()+f'/{module_directory}/')
        self.files = glob.glob(self.base_path+f'{files_directory}/*')

        # Bot information
        self.myBot = Kernel()
        self.doc_nlp = spacy.load(spacy_model)

        # Session information
        self.id = str(randint(1000, 9999))
        self.session_running = False

        # Info to save
        self.response = ''
        self.message = ''
        self.emotion = ''

        # Load EmoBERT model
        self.classifier = pipeline(
            "text-classification",
            model='bhadresh-savani/bert-base-uncased-emotion',
            top_k=None
        )

    def learn(self):
        for file in self.files:
            self.myBot.learn_aiml(file)

    def operations(self):
        if self.message.startswith("ENTITIES:"):
            doc = self.doc_nlp(self.message.replace("ENTITIES:", ''))
            self.response = [(ent.text, ent.label_) for ent in doc.ents]

        elif self.message.startswith("POS:"):
            doc = self.doc_nlp(self.message.replace("POS:", ''))
            self.response = [(token.text, token.pos_) for token in doc]

        elif self.message.startswith("SENT_TOKENIZE:"):
            self.response = self.doc_nlp(
                self.message.replace("SENT_TOKENIZE:", '')).sents

        elif self.message.startswith("WORD_TOKENIZE:"):
            self.response = self.doc_nlp(
                self.message.replace("WORD_TOKENIZE:", ''))

        else:
            self.response = 0

    def evaluate_emotion(self):
        scores = []
        prediction = self.classifier(self.message)

        for dictionary in prediction[0]:
            scores.append(dictionary['score'])

        dominant_emotions = prediction[0][scores.index(max(scores))]
        self.emotion = dominant_emotions['label']

    def chat_log(self):
        while f"log_{self.id}.txt" in os.listdir('.') and not self.session_running:
            self.id = str(randint(1000, 9999))
            self.session_running = True

        sentence_type, question_type = self.sentence_and_question()
        with open(self.base_path + f"logs/log_{self.id}.txt", "a") as file:
            file.write(f"User said: {self.message}\n")
            file.write(f"Bot responded: {self.response}\n")
            file.write(f"---Metadata---\n")
            file.write(f"Sentiment: {self.emotion}\n")
            file.write(f"Is question: {sentence_type}\n")
            file.write(f"Asked for: {question_type}\n\n")

    def sentence_and_question(self):
        is_question = False
        sent_type = "nothing"
        if self.message.endswith("?"):
            is_question = True
            sent_type = "unknown"
        question_words = {
            "how": "method",
            "why": "cause",
            "when": "time",
            "where": "location",
            "what": "information",
            "which": "selection"
        }
        for word in question_words.keys():
            for token in self.doc_nlp(self.message):
                if word.lower() == token.text.lower():
                    is_question = True
                    sent_type = question_words[word]
        return is_question, sent_type

    def generate_response(self, text, username):
        self.message = text
        self.username = username
        if "bye" in self.message.lower():
            self.response = "Bye"
            self.emotion = 'None'
        else:
            self.operations()
            self.prompt_for_relation()
            
            if self.response == 0:
                self.myBot.setBotPredicate("name", "AVA")
                self.response = self.myBot.respond(self.message, "xyz")
            self.evaluate_emotion()

        self.chat_log()
        return self.response

    def process_matched_group(self, pattern):
        relation_matched = re.findall(pattern, self.message)
        try:
            relation_matched = relation_matched[0].lower().replace(' ', '_')
        except IndexError:
            relation_matched = False

        return relation_matched
    
    def relation(self):
        obj1 = self.process_matched_group('_(.+)_')
        relation = self.process_matched_group('\+(.+)\+')
        obj2 = self.process_matched_group('-(.+)-')

        
        if False in [obj1, relation, obj2]:
            return False
        
        if obj1.lower() in ["i", "me", "my"]: 
            obj1 = str(self.username).lower().replace(' ', '_')

        if obj2.lower() in ["i", "me", "my"]:
            obj2 = str(self.username).lower().replace(' ', '_')
        self.create_person_relationship(obj1, obj2, relation)
        return f'{relation}({obj1}, {obj2})'

    def initiate(self):
        self.learn()
        self.session_running = True
        # notebook_login()

    def prompt_for_relation(self):
        found_relations = self.relation()
        if not found_relations == False:
            self.update_knowledge_base(found_relations)
        rel_list = ["male", 'female', "sibling", "sister", " brother", "cousin", "father",
                    " mother", "uncle", "aunt", "likes", "friend", "relation", "relationship"]

        for relation in rel_list:
            for token in self.doc_nlp(self.message):
                if relation == token.text:
                    self.response = "I see, you're telling me about private stuff (Ahmmmm...). Why don't you write it in the following format so I can better understand you. You can write '_' around primary object, '-' around secondary object and '+' around relation. For example: '-Ali- is _my_ +friend+' or '_I_ have a +friend+ -Ali-' or '_Ahmad_ +likes+ -icecream-'"

    def update_knowledge_base(self, relation):
        knowledge_base_path = f"{self.base_path}logs/facts.txt"
        with open(knowledge_base_path, "r") as file:
            facts = [fact.strip() for fact in file.readlines()]
        if relation in facts:
            import pytholog as pl
            new_kb = pl.KnowledgeBase("Relations")
            new_kb(facts)
            print(f"{new_kb.query(pl.Expr(relation))[0]}, The relation {relation} exists.")
        else:
            with open(knowledge_base_path, "a") as file:
                file.write(f"{relation}\n")

    def create_person_relationship(self, person1_name, person2_name, relation):
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))

        query = "MATCH (n:USERS {name: $name}) RETURN n"
        person1_node = graph.evaluate(query, name=person1_name)
        if person1_node is None:

            person1_node = Node("USERS", name=person1_name)
            graph.create(person1_node)

        query = "MATCH (n:USERS {name: $name}) RETURN n"
        person2_node = graph.evaluate(query, name=person2_name)
        if person2_node is None:

            person2_node = Node("USERS", name=person2_name)
            graph.create(person2_node)

        knows_relationship = Relationship(person1_node, relation, person2_node)
        graph.create(knows_relationship)
