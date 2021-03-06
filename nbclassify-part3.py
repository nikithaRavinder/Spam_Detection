import os
import sys
import math
import json

model = {}
doc_files = []
P_spam_log = 0
P_ham_log = 0
op = open("nboutput.txt", "w")


def read_nbmmodel():
    global model, P_ham_log, P_spam_log
    fop = open("nbmodel.txt", "r")
    f = fop.readlines()
    P_spam = f[0].split(':')[1].split()
    P_spam_log = math.log(float(P_spam[0]))
    P_ham = f[1].split(':')[1].split()
    P_ham_log = math.log(float(P_ham[0]))
    model = json.loads(f[2])
    fop.close()


def read_document():
    global doc_files
    path = sys.argv[1]
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                if "spam" in os.path.join(root, file):
                    doc_files.append(os.path.join(root, file))
                elif "ham" in os.path.join(root, file):
                    doc_files.append(os.path.join(root, file))
                else:
                    doc_files.append(os.path.join(root, file))


def tokenize():
    global doc_files, op
    for doc in doc_files:
        P_msg_spam = P_msg_ham = 0
        mop = open(doc, "r", encoding="latin1")
        message = mop.read()
        words = message.split()
        words = remove_punctuation(words)
        words = remove_stop_words(words)
        for word in words:
            if word+"_spam" in model.keys():
                P_msg_spam += math.log(model[word+"_spam"])
            if word+"_ham" in model.keys():
                P_msg_ham += math.log(model[word+"_ham"])
        mop.close()
        result = find_probability(P_msg_spam, P_msg_ham)
        op.write(str(result)+" "+os.path.abspath(doc)+"\n")


def remove_punctuation(wordlist):
    for key in wordlist:
        if key.isalpha() == False:
            wordlist.remove(key)
    return wordlist


def remove_stop_words(wordlist):
    stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
                 "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
                 "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't",
                 "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
                 "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him",
                 "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't",
                 "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor",
                 "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours	ourselves", "out",
                 "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
                 "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then",
                 "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those",
                 "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll",
                 "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
                 "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd",
                 "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "Subject:"]
    for key in wordlist:
        if key in stopwords:
            wordlist.remove(key)
    return wordlist


def find_probability(P_msg_spam, P_msg_ham):
    num_spam = P_spam_log + P_msg_spam
    num_ham = P_ham_log + P_msg_ham
    if float(num_spam) > float(num_ham):
        return "spam"
    elif num_spam < num_ham:
        return "ham"


read_nbmmodel()
read_document()
tokenize()
op.close()
