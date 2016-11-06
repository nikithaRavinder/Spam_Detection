import os
import sys
import json

spam_files = []
ham_files = []
all_files = []
spam_dict = {}
ham_dict = {}
model = {}


def read_files():
    global spam_files, ham_files, spam_dict, ham_dict, combined_vocab_count
    path = sys.argv[1]
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                if "spam" in os.path.join(root, file):
                    spam_files.append(os.path.join(root, file))
                elif "ham" in os.path.join(root, file):
                    ham_files.append(os.path.join(root, file))

    for file in spam_files:
        fp = open(file, "r", encoding="latin1")
        contents = fp.read()
        tokens = contents.split()
        for token in tokens:
            spam_dict[token] = spam_dict.get(token, 0) + 1
        fp.close()

    for file in ham_files:
        fp = open(file, "r", encoding="latin1")
        contents = fp.read()
        tokens = contents.split()
        for token in tokens:
            ham_dict[token] = ham_dict.get(token, 0) + 1
        fp.close()


def add_one_smoothing():
    global spam_dict, ham_dict
    combined_vocab_list = list(set(list(spam_dict.keys()) + list(ham_dict.keys())))
    for word in combined_vocab_list:
        if word not in spam_dict.keys():
            spam_dict.update({word: 0})
        if word not in ham_dict.keys():
            ham_dict.update({word: 0})


def output(word, label, value):
    global model
    key = str(word+"_"+label)
    model.update({key: value})


def calculate_probability(word, label, combined_vocab_count, count):
    if label == "spam":
        num = int(spam_dict[word]+1)
        den = count + combined_vocab_count
    else:
        num = int(ham_dict[word]+1)
        den = count + combined_vocab_count
    value = float(num / den)
    output(word, label, value)


read_files()
add_one_smoothing()

combined_vocab_count = len(set(list(spam_dict.keys()) + list(ham_dict.keys())))
spam_count = sum(list(spam_dict.values()))
ham_count = sum(list(ham_dict.values()))

op = open("nbmodel.txt", 'w')
for each in spam_dict:
    calculate_probability(each, "spam", combined_vocab_count, spam_count)
for each in ham_dict:
    calculate_probability(each, "ham", combined_vocab_count, ham_count)

spam_files_count = len(spam_files)
ham_files_count = len(ham_files)
print(spam_files_count, ham_files_count)
total_files = spam_files_count+ham_files_count
P_spam = float(spam_files_count/total_files)
P_ham = float(ham_files_count/total_files)
op.write("P_spam"+":"+str((P_spam))+"\n")
op.write("P_ham"+":"+str((P_ham))+"\n")

json_data = json.dumps(model)
op.write(json_data)
op.close()
