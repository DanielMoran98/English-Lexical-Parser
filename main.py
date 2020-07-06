# @author: Daniel Moran
# @version: Python 2.7

import pandas as p

sentenceWords = "The woman likes the green dog".lower().split()
sentenceTags = []
sentencePlural = []
tree = [[],[],[],[],[]]
treeParents = [[],[],[],[],[]]

rulesCSV = p.read_csv('rules.csv', delimiter=",")
lexiRules = p.read_csv('lexicon_rules.csv', delimiter=",")

rulesNonSplit = rulesCSV["nodes"].tolist()
rulesList = [ [] , rulesCSV["parent"].tolist()]

x=0
while(x < len(rulesNonSplit)): # Splits the nodes rules down into their single components
    rulesList[0].append(rulesNonSplit[x].split())
    x=x+1

def assignPOS(sentence): # Populates our lists and POS-tags our input sentence based on our lexicon rules file
    for word in sentenceWords: # For each word in sentence
        filtered = lexiRules[lexiRules.word == word]
        for row in filtered[['lexicon']].values:
                sentenceTags.append(row[0])
        for row in filtered[['plural']].values:
                sentencePlural.append(row[0])

    tree[0] = sentenceWords
    tree[1] = sentenceTags
    for x in range(len(sentenceWords)): # Populate the first row of the treeParents with values
        treeParents[0].append(x)

    print("--------------------------------")
    print("Rule list: " + str(rulesList))
    print("words : "+ str(sentenceWords))
    print("Lexicons : "+ str(sentenceTags))
    print("Plurals  : "+ str(sentencePlural))
    print("--------------------------------")


def checkRule(nodes, treeLevel): # Checks each node and its neighbors to see if any rules can be applied, if so we append it to the next level of our list
    counter = 0
    i = 0

    while(i < len(nodes)): # For each tree node


    #   ----- Rule file interaction -----
    #     j = 0
    #
    #     while(j < len(rulesList[0])): # for each rulelist entry
    #         k = 0
    #         while(k < len(rulesList[0][j])): #for each inner rulelist entry
    #
    #             if(nodes[i]  == rulesList[0][j][k]): # If node matches first rule value, check next
    #                 if(len(rulesList[0][j])+1 < k+1   and  nodes[i+1] == rulesList[0][j][k+1]): # If node+1 matches second rule value, check next
    #                     if(len(rulesList[0][j]) == 3): #If there is a 3rd rule value - check that
    #                         if(nodes[i+2] == rulesList[0][j][k+2]): #If rules match, append corressponding parent to the next tree level
    #                             tree[treeLevel+1].append(rulesList[1][j])
    #             k=k+1s
    #         j=j+1

        if (nodes[i] == "NP") and (nodes[i+1] == "VP"):
            tree[treeLevel+1].append("S")
            for x in range(2):
                treeParents[treeLevel].append(counter)
                i=i+1
            counter = counter+1
            # print("NP + VP = S")
        elif (nodes[i] == "V") and (nodes[i+1] == "NP"):
            tree[treeLevel+1].append("VP")
            for x in range(2):
                treeParents[treeLevel].append(counter)
                i=i+1
            counter = counter+1
            # print("V + NP = VP")
        elif (nodes[i] == "DET") and (nodes[i+1] == "N"):
            tree[treeLevel+1].append("NP")
            for x in range(2):
                treeParents[treeLevel].append(counter)
                i=i+1
            counter = counter+1
            # print("DET + N = NP")
        elif (nodes[i] == "DET") and (nodes[i+1] == "ADJ") and (nodes[i+2] == "N"): # If node is DET followed by an ADJ and N, we can replace them with an NP in the next level
            tree[treeLevel+1].append("NP")
            for x in range(3): # Since this rule uses 3 nodes, we skip all three before moving on
                treeParents[treeLevel].append(counter)
                i=i+1
            counter = counter+1
            # print("DET + ADJ + N = NP")
        else:
            tree[treeLevel+1].append(nodes[i]) # If no rules can be applied we carry it over to the next level
            for x in range(1):
                treeParents[treeLevel].append(counter)
                i=i+1
            counter = counter+1
            # print("No rule found")


def checkValidity(): # Checks a number of rules to make sure our sentence input is a valid statement

    valid = True
    i = 0
    while(i < len(sentenceWords)):
        # 1 - Check if determiner is "The" if following noun is plural
        if(sentenceTags[i] == "N"  and  sentenceTags[i-1] == "DET"):
            if(str(sentencePlural[i]) == "True"  and  sentenceWords[i-1] == "a"):
                print("Contains \"A\" followed by a plural noun ")
                valid = False
        if(sentenceTags[i] == "V"  and  sentenceTags[i-1] == "N"):
            # 2 - Check verb contains no S if previous noun is plural
            if(sentenceWords[i][len(sentenceWords[i])-1] == "s"  and str(sentencePlural[i-1]) == "True"  ):
                print("Verb ending in \'s\' , while noun is plural")
                valid = False
            # 3 - Check verb contains an S if previous noun is singular
            if(sentenceWords[i][len(sentenceWords[i])-1] != "s"  and str(sentencePlural[i-1]) == "False"  ):
                print("Verb doesn't end in \'s\' , while noun is singular")
                valid = False
        i=i+1
    if(valid == True):
        print("Input sentence is VALID")
    else:
        print("Input sentence is NOT VALID")
    print("--------------------------------")


def printTree(): #Prints the tree to the console
    print("Lexicon tree\n")

    i = len(tree)-1
    while i >= 0:
        print("["+str(i)+"] "+str(tree[i]))
        i=i-1
    print("--------------------------------")
    print("Parent index tree\n")
    i = len(tree)-1
    while i >= 0:
        print("["+str(i)+"] "+str(treeParents[i]))
        i=i-1


def printBracketed(): # Prints the bracketed output
    print("--------------------------------")
    print("Bracketed syntax:")
    bracketArray = []
    highestLevel = 3
    treeLevel = 4
    i = 0
    while(treeLevel >= 0):
        if(treeLevel >= 0 or tree[treeLevel][i] != tree[treeLevel-1][i]):
            print("[", end=""),
            print(tree[treeLevel][i], end=""),
            bracketArray.append(tree[treeLevel][i])
            treeLevel = treeLevel-1
            if treeLevel < 0:
                print("]", end=""),
                treeLevel = highestLevel
                highestLevel = highestLevel-1
                i = i+1
    print("]")

    print("--------------------------------")

##################### BEGIN #####################

assignPOS(sentenceWords)

checkValidity()


x=1
while(x <= 3): # Calls the checkRule function on each level of our tree
    checkRule(tree[x], x)
    x = x+1

printTree()

printBracketed()
