# python test.py matt
import sys
import csv
import model
# dataset to evaluate (can be changed)
dataset = "tripadvisor_hotel_reviews.csv"                                                        # name of data file

if (len(sys.argv) == 2):
    try:
        train_size = float(sys.argv[1])
    except ValueError:
        train_size = 80                 # if there happens to be no size value or the float doesn't work auto set
else:
    train_size = 80
if train_size<20 or train_size>80:      # auto set for invalid size
    train_size = 80
# train_size is a percentage of the data set to be used for training
print("Training set size: " + str(train_size) + "%\n")
print("Processing file...")
train_size = train_size/100
try:
    with open(dataset, mode ='r')as file:
        csvFile = csv.reader(file)
        file = []
        for lines in csvFile:
            file.append(lines)
except FileNotFoundError:
    print("ERROR: Not enough/too many/illegal input arguments.")
    exit()
total_size = len(file)-1
# this is the total amount of reviews
trainingSize = int((train_size*total_size)//1)      # math for training size 
trainingSet = []                                    # this will hold all the rows for the training set
for i in range(1, trainingSize+1):
    trainingSet.append(file[i])
testSet = []                                        # this holds all the rows for the test set
firstTestRow = int((0.8*total_size)//1)+1           # math for first test row (always last 20%)
for i in range(firstTestRow, len(file)):
    testSet.append(file[i])
print("Training classifier…")
myClassifier = model.Classifier()
for review in trainingSet:
    myClassifier.addClause(review[0], review[1])
# print(len(myClassifier.vocab))
print("Testing classifier…")
positives, results = myClassifier.testing(testSet)
print("Test results / metrics:\n")
print("Size of Test Set: " + str(len(testSet)))
print("Number of True Positives: " + str(positives))
print("Number of True Positive 1 Ratings: " + str(results[0][0]))
falsePositiveOne = 0
for i in range(0, 5):
    if i != 0:
        falsePositiveOne += results[0][i]
print("Number of False Positive 1 Ratings: " + str(falsePositiveOne))

print("Number of True Positive 2 Ratings: " + str(results[1][1]))
falsePositiveTwo = 0
for i in range(0, 5):
    if i != 1:
        falsePositiveTwo += results[1][i]
print("Number of False Positive 2 Ratings: " + str(falsePositiveTwo))

print("Number of True Positive 3 Ratings: " + str(results[2][2]))
falsePositiveThree = 0
for i in range(0, 5):
    if i != 2:
        falsePositiveThree += results[2][i]
print("Number of False Positive 3 Ratings: " + str(falsePositiveThree))

print("Number of True Positive 4 Ratings: " + str(results[3][3]))
falsePositiveFour = 0
for i in range(0, 5):
    if i != 3:
        falsePositiveFour += results[3][i]
print("Number of False Positive 4 Ratings: " + str(falsePositiveFour))

print("Number of True Positive 5 Ratings: " + str(results[4][4]))
falsePositiveFive = 0
for i in range(0, 5):
    if i != 4:
        falsePositiveFive += results[4][i]
print("Number of False Positive 5 Ratings: " + str(falsePositiveFive))

flag = True             # if user enters N flag gets set to false
while flag:
    print("\nEnter your sentence:")
    sentence = str(input())
    print("\nSentence S:\n" + sentence)
    labelPercentages = myClassifier.classifySentence(sentence)
    print("\nwas classified as " + str(labelPercentages[5]))
    for i in range(0,5):
        print("P(" + str(i+1) + " | S) = " + str(labelPercentages[i]))
    print("\nDo you want to enter another sentence [Y/N]?")
    response = str(input()).upper()
    if (not response == 'Y'):
        flag = False
# print("Guess: " + str(labelPercentages[5]))
# for i in range(0,5):
#     print("Label " + str(i+1) + ": " + str(labelPercentages[i]))

# positives = []      # index is label



        
        

# myClass = Classifier()
# print(myClass.labels)

# sentence = "We can see in the above can code"
# myClass.addClause(sentence, 1)
# print(myClass.labels)
# secondSentence = "the variables that store each "
# myClass.addClause(secondSentence, 5)
# print(myClass.labels)

# print(len(myClass.vocab))
# print(myClass.wordGivenLabel("can", 1))

# print(myClass.labelPercentage(1))
# print(myClass.wordGivenLabel("can", 5))
               
