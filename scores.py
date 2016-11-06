results = []

file = open("p.txt", "r").readlines()
for line in file:
    op_label = line.split(" ")[0]
    path = line.split(" ")[1]
    fname = path[path.rfind("/")+1:]
    if "spam" in fname:
        label = "spam"
    else:
        label = "ham"
    results.append([op_label, label])

counts = [[0, 0], [0, 0]]
for res in results:
    if res[0] == res[1] == "ham":
        counts[0][0] += 1
    elif res[0] == res[1] == "spam":
        counts[1][1] += 1
    elif res[0] == "ham" and res[1] == "spam":
        counts[1][0] += 1
    elif res[0] =="spam" and res[1] == "ham":
        counts[0][1] += 1

ham_precision = counts[0][0] / (counts[0][0] + counts[1][0])
ham_recall = counts[0][0] / (counts[0][0] + counts[0][1])
ham_fscore = 2 * ham_precision * ham_recall / (ham_precision + ham_recall)

spam_precision = counts[1][1] / (counts[1][1] + counts[0][1])
spam_recall = counts[1][1] / (counts[1][1] + counts[1][0])
spam_fscore = 2 * spam_precision * spam_recall / (spam_precision + spam_recall)

print("Ham: Precision= {0}, Recall= {1}, F-Score= {2}".format(ham_precision, ham_recall, ham_fscore))
print("Spam: Precision= {0}, Recall= {1}, F-Score= {2}".format(spam_precision, spam_recall, spam_fscore))

total_count = counts[0][0] + counts[0][1] + counts[1][0] + counts[1][1]
weighted_avg = ((counts[1][0]+counts[1][1]) * spam_fscore / total_count) + ((counts[0][0]+counts[0][1]) * ham_fscore / total_count)
print("Weighted Avg: "+str(weighted_avg))


