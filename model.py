"""
This model involves a 5 label classifier which classifies the hotel reviews by their rating (1-5 star).
"""
import mpmath as mp
import math
# mpmath
dictionary = {
    'a': 2,
    'b': 3,
    'c': 4,
    'd': 5,
    'e': 6,
    'f': 7,
    'g': 8,
    'h': 9,
    'i': 10,
    'j': 11,
    'k': 12,
    'l': 13,
    'm': 14,
    'n': 15,
    'o': 16,
    'p': 17,
    'q': 18,
    'r': 19,
    's': 20,
    't': 21,
    'u': 22,
    'v': 23,
    'w': 24,
    'x': 25,
    'y': 26,
    'z': 27,
    '0': 28,
    '1': 29,
    '2': 30,
    '3': 31,
    '4': 32,
    '5': 33,
    '6': 34,
    '7': 35,
    '8': 36,
    '9': 37,
    'other': 38
# current;y only accounts for words starting in a-z and numbers
}
replaceWithSpace = ['.', ',', '/', '!', '?', ';', ':','-', '_', '(', ')']
replaceWithNothing = ['\'']

class Classifier:
    def __init__(self):
        self.labels = [[0,0] + [dict() for _ in range(len(dictionary))] for _ in range(5)]
        self.vocab = []
    
# takes a sentence and splits it into words and returns a list of those words
    def prepareSentence(self, clause):
        lst = clause.lower()
        for i in replaceWithSpace:
            lst = lst.replace(i, ' ')
        for i in replaceWithNothing:
            lst = lst.replace(i, '')
        lst = lst.split()
        return lst
    
    
    def addClause(self, clause, label):
        self.labels[label-1][0] += 1
        lst = self.prepareSentence(clause)
        for word in lst:
            self.addWord(word, label)
            
    
    def addWord(self, word, label):
        self.labels[label-1][1] += 1
        try:
            self.labels[label-1][dictionary[word[0]]][word] += 1  
        except KeyError:                                                           # word hasn't been counted yet
            try:
                self.labels[label-1][dictionary[word[0]]][word] = 1
            except KeyError:                                                       # first "letter" of word isn't valid in dictionary
                self.labels[label-1][dictionary["other"]][word] = 1
            if word not in self.vocab:
                self.vocab.append(word)

    def labelPercentage(self, label):
        totalOfLabel = self.labels[label-1][0]
        totalClauses = 0
        for i in range(0, len(self.labels)):
            totalClauses += self.labels[i][0]
        try:
            if totalOfLabel == 0:
                Exception("FIX: lack of label data")
            else:
                return totalOfLabel/totalClauses
        except ZeroDivisionError:
            Exception("FIX: lack of clause data")
    
    def wordGivenLabel(self, word, label):
        try:
            occurances = self.labels[label-1][dictionary[word[0]]][word] + 1
        except KeyError:
            occurances = 1
        totalWords = self.labels[label-1][1] + len(self.vocab)
        return occurances/totalWords

# takes a cluase and returns it's probable label
    def guessLabel(self, clause):
        # print(clause)
        lst = self.prepareSentence(clause)
        max = mp.ln(1)                                  # i was just too lazy to lookup how to represent zero
# current max is zero
        label = str(0)
        for i in range(1,6):
            ans = mp.ln(self.labelPercentage(i))
            for word  in lst:
                ans += mp.ln(self.wordGivenLabel(word, i))
# FROM BELOW
                if math.e ** ans==0:
                    raise Exception("\nUNDERFLOW\n")
# TO ABOVE
            ans = mp.exp(ans)
            if ans > max:
                # print(ans)
                label = str(i)
                max = ans
        return label

# returns an array of the percentages for each label and then the label with the highest percentage
# this is mostly for the user option to enter a sentence
    def classifySentence(self, clause):
        lst = self.prepareSentence(clause)
        labelPercentages = []
        for i in range(1,6):
            ans = mp.ln(self.labelPercentage(i))
            for word in lst:
                ans += mp.ln(self.wordGivenLabel(word, i))
                if ans==mp.ln(1):
                    raise Exception("\nUNDERFLOW\n")
            labelPercentages.append(math.e ** ans)
        label = 0
        max = mp.ln(1)
        for i in range(0, 5):
            if labelPercentages[i] > max:
                label = i+1
                max = labelPercentages[i]
        labelPercentages.append(label)
        return labelPercentages

# takes the testSet and given the classifier, counts the positives
    def testing(self, testSet):
        positives = 0
        results = [[0 for i in range(0,5)] for i in range (0,5)]
# results is the confusion matrix
        for data in testSet:
            guess = self.guessLabel(data[0])
            actual = data[1]
            if guess == '1':
                if actual == '1':
                    positives += 1
                    results[0][0] += 1
                elif actual == '2':
                    results[0][1] += 1
                elif actual == '3':
                    results[0][2] += 1
                elif actual == '4':
                    results[0][3] += 1
                elif actual == '5':
                    results[0][4] += 1
                else:
                    print(actual)
                    print(type(actual))
                    raise Exception("Testset contains invalid label")
            elif guess == '2':
                if actual == '2':
                    positives += 1
                    results[1][1] += 1
                elif actual == '1':
                    results[1][0] += 1
                elif actual == '3':
                    results[1][2] += 1
                elif actual == '4':
                    results[1][3] += 1
                elif actual == '5':
                    results[1][4] += 1
                else:
                    print(actual)
                    print(type(actual))
                    raise Exception("Testset contains invalid label")
            elif guess == '3':
                if actual == '3':
                    positives += 1
                    results[2][2] += 1
                elif actual == '1':
                    results[2][0] += 1
                elif actual == '2':
                    results[2][1] += 1
                elif actual == '4':
                    results[2][3] += 1
                elif actual == '5':
                    results[2][4] += 1
                else:
                    print(actual)
                    print(type(actual))
                    raise Exception("Testset contains invalid label")
            elif guess == '4':
                if actual == '4':
                    positives += 1
                    results[3][3] += 1
                elif actual == '1':
                    results[3][0] += 1
                elif actual == '2':
                    results[3][1] += 1
                elif actual == '3':
                    results[3][2] += 1
                elif actual == '5':
                    results[3][4] += 1
                else:
                    print(actual)
                    print(type(actual))
                    raise Exception("Testset contains invalid label")
            elif guess == '5':
                if actual == '5':
                    positives += 1
                    results[4][4] += 1
                elif actual == '1':
                    results[4][0] += 1
                elif actual == '2':
                    results[4][1] += 1
                elif actual == '3':
                    results[4][2] += 1
                elif actual == '4':
                    results[4][3] += 1
                else:
                    print(actual)
                    print(type(actual))
                    raise Exception("Testset contains invalid label")
            else:
                raise Exception("Program brought up invalid guess")
        return positives, results