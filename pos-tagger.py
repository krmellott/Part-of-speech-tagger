#Kyle Mellott


#This program is a part of speech tagger that analyzes tagged training data.
#The program is trained using training data and tested on separate test data, with the results
#being saved and analyzed by a separate program.

#The first input to the program is the mode selector. Possible values can be 0 or 1. A mode 0 tagger
#chooses tags based solely on probability, with the most likely tag being chosen. A mode 1 tagger is
#a mode 0 tagger with extra enhancements to increase the accuracy. The mode 1 tagger in this case has
#10 extra rules that refine the tagger to increase accuracy.

#The mode 1 tagger increases accuracy by approximately 1.157% over the mode 0 tagger.

#The 2nd and 3rd inputs are the training and test data, respectively.

#An example of program operation is as follows:
#   In the command prompt:
#   >> Python pos-tagger.py 0 pos-train.txt pos-test.txt
#   A sample of the output would look like:
#     were/VBD
#     priced/VBN
#     at/IN
#     35/CD
#     1\/2/CD

#The steps of the program are as follows: 
#  The program is called from the command line, collecting the tagger mode, training data
#  and test data and storing them in their respective similarly named variables. This information
#  is then passed to main().
#  main() passes the training data to the process() function. The process() function opens the file,
#  replacesthe '/' between the word and the assigned tag with a space, and appends each word and tag to a list
#  called words[]. This means that one index in words[] would contain something like: 'sample NN'. The function
#  then returns the list back to main.
#  The list of words is passed to the findTags() function. The findTags() function begins by iterating through the
#  list of words, and adding each word to a dictionary, called wordDict. The value for each word is assigned as an
#  empty list. For example, after the first iteration, an entry in wordDict would look like "sample: []"
#  The second for loop iterates through the list of words. For each word, it finds the word in the dictionary and
#  adds the tag for that word to the list value.
#  An example of a word after the 2nd iteration would be: "{sample: [NN, VB, NN, VB, NN, VB, NN, NN, NN]}"
#  where "sample" is the dictionary key, and the list of tags is the key's value.
#  The word dictionary is then returned to main().

#  The word dictionary, now stored in wordTags, is next passed to probability(). probatility creates a
#  dictionary, named probabilities. It stores the dictionary keys in a temporary list, called tempList.
#  It iterates through the keys in the tempList. For each key, it retrieves the list of values and
#  inputs them all into a separate dictionary called tempDict. Every value is initialized to 0. 
#  Next, it again iterates through the word tags in tempList, and increments the tag count by 1 every
#  time it is seen. It updates the temporary dictionary such that one entry contains the word tag,
#  and the value is the number of times that word tags appears divided by the total number of tags.
#  This creates a probability that each tag will occur. This multi-value dictionary is then added
#  to the probabilities dictionary, where the key is the word and the value is the multi-value dictionary
#  of probabilities for each tag.
#  An example entry may look like: {sample: {NN: 0.5, VB: 0.5}}

#  The next step depends on the tagger mode. main() will pass the probabilities dictionary and the
#  test data to either conductTest0() or conductTest1(), depending on the tagger_mode variable.
#  Both mode 0 and mode 1 begin the same way.

#  conductTest begins by creating an empty list, called words[], and opening the test file.
#  For each line in the file, it appends the line to the list of words.
#  It then iterates through the list of words from the test data. In mode 0, if the word
#  is not in the probabilities dictionary, it is assigned a default value of "NN". Otherwise,
#  the result is calculated by finding the maximum probability from the dictionary of probabilities
#  for that word. It then prints the results in the form: word + "/" + result

#  conductTest1 is the function that handles mode 1. It operates the same way as mode 0 with the exception
#  of adding more rules to handle unknown and known word issues. Mode 1 will execute 5 rules on unknown words
#  prior to assigning the word "NN" in an attempt to increase accuracy.

#  There are 5 rules to handle unknown words, and 5 rules to handle issues with known words. I will not describe them
#  all here, as they are already described in the function.

import sys, re



#Receives training_data from main, returns words[].
#Extracts and processes the data from the training file.
def process(training_data):
    words = []
    file = open(training_data, "r", encoding = "utf-8")
    word = file.readlines()
    for line in word:
	#The following 3 regular expressions serve to delete the '/' between
	#the word and the part of speech tag. This is done so that later expressions
	#can easily extract the tag from the line.
        x = re.sub("[\/]", " ", line)
        x = re.sub(r"\\ ", "\/", x)
        x = re.sub(r"\n", "", x)
        words.append(x)
    file.close()
    return words


#Receives words[] from main, returns wordDict
def findTags(words):
    wordDict = {}
    for word in words:
        #This regex captures the word itself
        x = re.search("(.*) ", word)
        wordDict[x.group(1)] = list()
    for word in words:
        #This regex captures the word itself
        x = re.search("(.*) ", word)
        #This regex captures the part of speech tag for the word
        y = re.search(" (.*)", word)
        wordDict.get(x.group(1)).append(y.group(1))
    return wordDict


#Receives wordTags from main, returns probabilities{}
def probability(wordTags):
    probabilities = {}
    for key in wordTags.keys():
        total = 0
        tempDict = {}
        tempList = wordTags[key]
        for tag in tempList:
            tempDict[tag] = 0
            total += 1
        for tag in tempList:
            tempDict[tag] += 1
        tempKey = key
        for key, value in tempDict.items():
            tempDict.update({key: value/total})
        probabilities[tempKey] = tempDict
    return probabilities



def conductTest0(probabilities, test_data):
    words = []
    file = open(test_data, "r", encoding = "utf-8")
    word = file.readlines()
    for line in word:
        #Eliminates the \n character at the end of each tag. This is necessary
        #because of the use of readlines() to prevent double newlines
        x = re.sub(r"\n", "", line)
        words.append(x)
    for word in words:
        if word not in probabilities:
            print(word + "/NN")
        else:
            result = max(probabilities[word], key=probabilities[word].get)
            print(word + "/" + result)
    file.close()
    

def conductTest1(probabilities, test_data):
    lastResult = ""
    result = ""
    words = []
    file = open(test_data, "r", encoding = "utf-8")
    word = file.readlines()
    i = 0
    for line in word:
        #Eliminates the \n character at the end of each tag. This is necessary
        #because of the use of readlines() to prevent double newlines        
        x = re.sub(r"\n", "", line)
        words.append(x)
    while i < len(words):
        if words[i] not in probabilities:
            
            #U-1
            #If the unknown word starts with a capital letter and ends in ies, assign it plural proper noun
            #Example: Securities
            x = re.search(r"[A-Z].*ies\Z", words[i])
            if (x != None):
                print(words[i] + "/NNPS")
                i += 1
                continue
            #U-2
            #If the unknown word starts with a capital letter and ends in s, assigns it proper noun
            #Example: Teachers
            x = re.search(r"[A-Z].*s\Z", words[i])
            if (x != None):
                print(words[i] + "/NNP")
                i += 1
                continue

            #U-3
            #If the unknown word starts with a capital letter and ends in something other than S, assigns it proper noun
            #Example: Wendy
            x = re.search(r"[A-Z].*[^s]\Z", words[i])
            if (x != None):
                print(words[i] + "/NNP")
                i += 1
                continue

            #U-4
            #If the unknown word doesn't start with a capital and ends in an s, assigns plural noun
            #Example: teachers
            x = re.search(r"[a-z].*[s]\Z", words[i])
            if (x != None):
                print(words[i] + "/NNS")
                i += 1
                continue

            #U-5
            #If the unknown word has no word characters assigns CD
            #Examples: 108.9
            x = re.search(r"\W", words[i])
            if (x != None):
                print(words[i] + "/CD")
                i += 1
                continue
            #If the unknown word does not meet any of the rules above, assigns the default "NN"
            else:
                print(words[i] + "/NN")
                i += 1

                
        else:
            #This if statement allows for storage of the previous word's tag
            if result != "":
                lastResult = result

            #Determines the maximum probability tag for the given word    
            result = max(probabilities[words[i]], key=probabilities[words[i]].get)

            
            #E-1
            #Assigns proper nouns that start with a capital and end in ies as a singular proper noun
            #Example: Securities
            x = re.search(r"[A-Z].*ies\Z", words[i])
            if ((x != None) and (result != "NNP")):
                print(words[i] + "/NNP")
                i += 1
                continue

            #E-2
            #Proper nouns that end in "es" were being marked as NNPS contrary to the expected NNP in the gold standard data
            #Example: Airlines
            x = re.search("[A-Z].*es\Z", words[i])
            if ((x != None) and (result == "NNPS")):
                print(words[i] + "/NNP")
                i += 1
                continue            

            #E-3
            #If the known word is "well" and not classified as a noun, checks to see if the previous word
            #was a determiner such as "The". If yes, assigns "well" as a noun.
            #Example: The well vs well-off
            x = re.search(r"well", words[i])
            if ((x!= None) and (result != "NN")):
                if (lastResult == "DT"):
                    print(words[i] + "/NN")
                    i += 1
                    continue

            #E-4
            #If the known word is a hyphenated word, and is assigned CD, it's most likely an adverb.
            #example: 12th-worst
            x = re.search("\W*-\W*", words[i])
            if ((x!= None) and (result == "CD")):
                print(words[i] + "/JJ")
                i += 1
                continue                


            #If the known word ends in -est and a verb follows, assigns it as superlative adverb
            #Example: Hardest hit
            x = re.search(".*est\Z", word[i])
            if ((x!= None) and max(probabilities[words[i+1]], key=probabilities[words[i+1]].get) == ("VB" or "VBD" or "VBN")):
                print(words[i] + "/RBS")
                i += 1
                continue
                
            
            
            print(words[i] + "/" + result)
            i += 1
    file.close()

            
def main(tagger_mode, training_data, test_data):
    words = process(training_data)
    wordTags = findTags(words)
    probabilities = probability(wordTags)
    if tagger_mode == '0':
        conductTest0(probabilities, test_data)
    elif tagger_mode == '1':
        conductTest1(probabilities, test_data)
    
if __name__ == '__main__':
    tagger_mode = sys.argv[1]
    training_data = sys.argv[2]
    test_data = sys.argv[3]
    main(tagger_mode, training_data, test_data)
