message = "hey"
def sentence_and_question():
        if message.endswith("?"):
            return True
        question_words = {
            "how" : "", 
            "why" : "",
            "when" : "",
            "where" : "",
            "what" : "",
            "which" : "",
            "whom" : ""
            }
        for word in question_words.keys():
            print(word)
sentence_and_question()