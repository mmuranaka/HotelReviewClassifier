# python classifier.py matt
import sys
import csv
import model2
# dataset to evaluate (can be changed)
dataset = "tripadvisor_hotel_reviews.csv" # name of data file

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
myClassifier = model2.Classifier()
for review in trainingSet:
    if (int(review[1]) < 3):
        myClassifier.addClause(review[0], 0)
    else:
        myClassifier.addClause(review[0], 1)
print("Testing classifier…")
results = myClassifier.testing(testSet)
print("Test results / metrics:\n")
print("Size of Training Set: " + str(len(trainingSet)))
print("Size of Test Set: " + str(len(testSet)))
print("Number of True Positives: " + str(results[0]))
print("Number of True Negatives: " + str(results[2]))
print("Number of False Positives: " + str(results[1]))
print("Number of False Negatives: " + str(results[3]))
recall = results[0]/(results[0]+results[3])
print("Sensitivity (Recall): " + str(recall))
print("Specificity: " + str(results[2]/(results[2]+results[1])))
precision = results[0]/(results[0]+results[1])
print("Precision: " + str(precision))
print("Negative Predictive Value: " + str(results[2]/(results[2]+results[3])))
print("Accuracy: " + str((results[0]+results[2])/(results[0]+results[2]+results[1]+results[3])))
print("F-Score: " + str(2*recall*precision/(recall+precision)))

flag = True             # if user enters N flag gets set to false
while flag:
    print("\nEnter your sentence:")
    sentence = str(input())
    print("\nSentence S:\n" + sentence)
    labelPercentages = myClassifier.classifySentence(sentence)
    if (labelPercentages[2] == 0):
        sentenceGuess = "Negative"
    else:
        sentenceGuess = "Positive"
    print("\nwas classified as " + str(sentenceGuess))
    print("P( + | S) = " + str(labelPercentages[1]))
    print("P( - | S) = " + str(labelPercentages[0]))
    print("\nDo you want to enter another sentence [Y/N]?")
    response = str(input()).upper()
    if (not response == 'Y'):
        flag = False


               
