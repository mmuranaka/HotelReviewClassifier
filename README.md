# Hotel Review Classifier

## 1. Overview

This project involved implementing a Naive Bayes classifier in Python to classify Trip Advisor hotel reviews. Each review consisted of a sentence and a corresponding rating on a scale of 1 to 5. The classifier's goal was to determine the rating of a review. Two different models were built based on classification labels.

One model involved determining the exact rating of the review, labelling each data point on a scale of 1 to 5. The other model involved determining whether a review was positive or not based on its text. Reviews with ratings from 3 to 5 were labeled as positive, while those with ratings of 1 or 2 were considered negative. Since evalution of model performance was a big importance on this project, I decided to build the second binary model to make performance evaluation simpler.

To build the classifier, the review text was preprocessed, including steps such as tokenization. The Naive Bayes algorithm was then trained on the processed data, leveraging the relationship between word occurrences and review positivity. The model was evaluated based on its accuracy in correctly predicting positive or negative sentiment from new review sentences, demonstrating the utility of Naive Bayes for text classification tasks.

## 2. Feature Overview

The following are high level features this classifier has:

1. Train a Naive Bayes Classifier based on a dataset in the csv format. 
2. Output evaluation metrics including:
    Number of True Positives
    Number of True Negatives
    Number of False Positives
    Number of False Negatives
    Sensitivity (Recall)
    Specificity
    Precision
    Negative Predictive Value
    Accuracy
    F-Score
3. Allow the user to enter a sentence and gain the probability which the sentence would be classified as positive or negative as a Trip Advisor Hotel Review

Further, the program allows for certain features of the program to be enabled/disabled
1. By changing the line *import model* / *import model2* in classifier.py you can determine whether the model is trained based on a 5-class rating or positive/negative rating.
2. By altering the line *keepStopWords = True* / *keepStopWords = False* in model2.py, when using model2 on the classifier you can specify wether the model should be built with the removal of stopwords.

## 3. Usage

The program can be executed with the line:  
`python classifier.py TRAIN_SIZE`

- `classifier.py` is the name of the program which processes the dataset and builds the model.
- `TRAIN_SIZE` is the user-specified training size:
    - A percentage between 20 and 80 specifying the percent of the dataset to be considered for training.
    - If the input does not meet these requirements, the default training size (80%) will be used.

Following this input and the running of the program, you will receive:  
`Enter your sentence:`

- At this point, you can input a sentence of your choosing.
- The program classifies your sentence and asks:  
  `Do you want to enter another sentence Y/N?`

    - Answering with `Y` will allow the user to input another sentence.
    - Answering with `N` will end the program.

