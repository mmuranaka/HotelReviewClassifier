"""
This model classifies the hotel reviews between positive and negative:
    positive (3-5 rating)
    negative (1-2 rating)
"""
import mpmath as mp
import nltk
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
keepStopWords = True

if not keepStopWords:
    corpusStopWords = nltk.corpus.stopwords                        # corpus containing all of the stopwords
    stopwords = corpusStopWords.words()                                    # list of stopwords
    

class Classifier:
    def __init__(self):
        self.labels = [[0,0] + [dict() for _ in range(len(dictionary))] for _ in range(2)]
        self.vocab = []
# data structure is explained in slides
    
# takes a sentence and splits it into words and returns a list of those words
    def prepareSentence(self, clause):
        lst = clause.lower()
        for i in replaceWithSpace:
            lst = lst.replace(i, ' ')
        for i in replaceWithNothing:
            lst = lst.replace(i, '')
        lst = lst.split()
        return lst
    
# accounts clause to classifier
    def addClause(self, clause, label):
        self.labels[label][0] += 1
        lst = self.prepareSentence(clause)
        for word in lst:
            self.addWord(word, label)
            
# accounts word to classifier
    def addWord(self, word, label):
        if keepStopWords:
            self.labels[label][1] += 1
            try:
                self.labels[label][dictionary[word[0]]][word] += 1  
            except KeyError:                                                           # word hasn't been counted yet
                try:
                    self.labels[label][dictionary[word[0]]][word] = 1
                except KeyError:                                                       # first "letter" of word isn't valid in dictionary
                    self.labels[label][dictionary["other"]][word] = 1
                if word not in self.vocab:
                    self.vocab.append(word)
        else:               # remove stopwords
            if word not in stopwords:
                self.labels[label][1] += 1
                try:
                    self.labels[label][dictionary[word[0]]][word] += 1  
                except KeyError:                                                           # word hasn't been counted yet
                    try:
                        self.labels[label][dictionary[word[0]]][word] = 1
                    except KeyError:                                                       # first "letter" of word isn't valid in dictionary
                        self.labels[label][dictionary["other"]][word] = 1
                    if word not in self.vocab:
                        self.vocab.append(word)

    def labelPercentage(self, label):
        totalOfLabel = self.labels[label][0]
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
            occurances = self.labels[label][dictionary[word[0]]][word] + 1
        except KeyError:
            occurances = 1
        totalWords = self.labels[label][1] + len(self.vocab)
        return occurances/totalWords

# takes a cluase and returns it's probable label
    def guessLabel(self, clause):
        # print(clause)
        lst = self.prepareSentence(clause)
        percentages = []
# current max is zero
        for i in range(0,2):
            ans = mp.ln(self.labelPercentage(i))
            for word  in lst:
                ans += mp.ln(self.wordGivenLabel(word, i))
            ans = mp.exp(ans)
            percentages.append(ans)
        weight = mp.power(percentages[0] + percentages[1], -1)
        if weight*percentages[1] > mp.power(0.5, 1):
            return 1
        else:
            return 0


# returns an array of the percentages for each label and then the label with the highest percentage
# this is mostly for the user option to enter a sentence
    def classifySentence(self, clause):
        lst = self.prepareSentence(clause)
        labelPercentages = []
        for i in range(0,2):
            ans = mp.ln(self.labelPercentage(i))
            for word in lst:
                ans += mp.ln(self.wordGivenLabel(word, i))
                if ans==mp.ln(1):
                    raise Exception("\nUNDERFLOW\n")
            labelPercentages.append(mp.exp(ans))
        if labelPercentages[1] > labelPercentages[0]:
            return [labelPercentages[0], labelPercentages[1], 1]
        else:
            return [labelPercentages[0], labelPercentages[1], 0]

# takes the testSet and given the classifier, counts the positives
    def testing(self, testSet):
        results = [0 for _ in range(0, 4)]
# results is the confusion matrix
        #   index = 0 - true positive
        #   index = 1 - false positive
        #   index = 2 - true negative
        #   index = 3 - false negative
        for data in testSet:
            guess = self.guessLabel(data[0])
            actual = int(data[1])
            if (actual<3):
                actual = 0
            else:
                actual = 1

            if guess == 0:
                if actual == 0:
                    results[2] += 1
                elif actual ==1:
                    results[3] += 1
                else:
                    Exception("Actual is not valid")
            elif guess == 1:
                if actual == 1:
                    results[0] += 1
                elif actual == 0:
                    results[1] += 1
                else:
                    Exception("Actual is not valid")
            else:
               Exception("Guess is not valid") 
        return results