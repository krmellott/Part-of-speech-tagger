#Kyle Mellott


#This program is an evaluator to determine the accuracy of the pos-tagger.py program.
#The program outputs the accuracy, followed by a confusion matrix containing each tag

#The first input to the program is the test_results, which are the results obtained
#from pos-tagger.py.
#The second input to the program is that gold standard results.

#An example of program operation is as follows:
#   In the command prompt:
#   >> Python pos-tagger-eval.py pos-test-answers-1.txt pos-key.txt
#   A sample of the output would look like:
#     Accuracy : 0.9323349289032803
#     #: 5
#     $ $: 375
#     '' '': 528
#     ( (: 76
#     ) ): 76
#     , ,: 3070
#     . .: 2363
#     : :: 336
#     CC CC: 1361
#     CC IN: 2
#     CC NN: 3
#     CC RB: 2

#The steps of the program are as follows:
#  The program is called from the command line, passing in the test_results
#  and gold_results, which are then passed to main().
#  main() passes the test_results and gold_results to the process() function.
#  process() opens both files, uses readlines() to read the contents, and
#  replaces the '/' between the word and tag with a space. It then appends the
#  words and tags to either test_list, or gold_list, and returns both of these.

#  main() then passes the test_list and gold_list to the compare() function.
#  compare() uses regex to retrieve the word tags from test_list and gold_list,
#  and add all of the tags to a separate list, called myAnsers and goldAnswers.
#  These values are then added to the dictionary called confusions, such that the
#  concatenated tags are the key value. The value for each key is then initialized to 0.
#  An example of a dictionary entry at this point would look similar to: {"NN NN": 0}
#  It then iterates through both arrays using an index value. It increments the value for
#  each key pair in confusion{} as it occurs in myAnswers and goldAnswers. It also keeps
#  a running count for how many of the myAnswers[index] = goldAnswers[index] are matching.
#  It calculates accuracy by dividing the total number of matching pairs by the length of
#  the myAnswers list.
#  It then sorts the confusion matrix and prints. 





import sys, re

def process(test_results, gold_results):
    file = open(test_results, "r", encoding = "utf-8")
    test_answers = file.readlines()
    test_list = []
    gold_list = []
    for line in test_answers:

        #Replaces the '/' between the word and tag with a space
        #and removes the newline character
        x = re.sub("[\/]", " ", line)
        x = re.sub(r"\\ ", "\/", x)
        x = re.sub(r"\n", "", x)
        test_list.append(x)
    file.close()
    file2 = open(gold_results, "r", encoding = "utf-8")
    gold_answers = file2.readlines()
    for line in gold_answers:
        
        #Replaces the '/' between the word and tag with a space
        #and removes the newline character
        x = re.sub("[\/]", " ", line)
        x = re.sub(r"\\ ", "\/", x)
        x = re.sub(r"\n", "", x)        
        gold_list.append(x)
    file2.close()
    return test_list, gold_list

def compare(test_list, gold_list):
    confusions = {}
    myAnswers = []
    goldAnswers = []
    correct = 0
    index = 0
    #Creates the myAnswers list, which is a list of the tags
    #that my program assigned
    for word in test_list:
        y = re.search(" (.*)", word)
        myAnswer = y.group(1)
        myAnswers.append(myAnswer)
    #Creates the goldAnswers list, which is a list of the tags
    #from the gold standard file    
    for word in gold_list:
        y = re.search(" (.*)", word)
        goldAnswer = y.group(1)
        goldAnswers.append(goldAnswer)
    #Creates a key in the confusions dictionary that consists of the concatenated
    #tags and assigns the value of 0
    while(index < len(myAnswers)):
        confusions[myAnswers[index] + " " + goldAnswers[index]] = int(0)
        index += 1
    index = 0
    #Every time a tag pair is seen in [myAnswers goldAnswers], increments
    #the corresponding tag pair in the confusions matrix
    #For example, if myAnswers[10] = "NN" and goldAnswers[10] = "CD",
    #then confusions[NN CD] will be incremented by 1.
    #If they are matching, it keeps track of the "correct" assignments
    while(index < len(myAnswers)):
        confusions[myAnswers[index] + " " + goldAnswers[index]] += 1
        if myAnswers[index] == goldAnswers[index]:
            correct += 1
        index += 1
    accuracy = correct/len(myAnswers)
    print("Accuracy : " + str(accuracy))
    sorted_confusion = sorted(confusions.items(), key = lambda key:key[0])
    for i in sorted_confusion:
        print(i[0] + ": " + str(i[1]))
    
        

def main(test_results, gold_results):
    test_list, gold_list = process(test_results, gold_results)
    compare(test_list, gold_list)


if __name__ == '__main__':
    test_results = sys.argv[1]
    gold_results = sys.argv[2]
    main(test_results, gold_results)
