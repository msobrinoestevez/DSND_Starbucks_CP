# Starbucks Capstone Challenge
This project is a part of Udacity Data Science Nanodegree

### Table of Contents

1. [Project Overview](#overview)
2. [Project Components](#components)
3. [Installation](#installation)
4. [File Descriptions](#files)
5. [Instructions](#instructions)
6. [Acknowledgements](#licensing)
7. [Results](#results)
### 1. Project Overview<a name="overview"></a>

Starbucks provided simulated data that mimics customer behavior on the Starbucks rewards mobile app. Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free). Some users might not receive any offer during certain weeks. Not all users receive the same offer, and that is the challenge to solve with this data set.
The task is to combine transaction, demographic and offer data to determine which demographic groups respond best to which offer type.


### 2. Project Components<a name="components"></a>


The problem that I choose to solve was to build a model that predicts whether a customer will respond to an offer. These are the steps taken to achieve this:

a. Exploratory data analysis, data cleaning and data preprocess with portfolio, profile and transaction datasets<br>
b. Combine these clean datasets containing relevant features which can be used to train our model<br>
c. Split data to train and test datasets (and scaling variables), selecting the appropriate performance matrix<br>
d. Calculate features importance given by the best estimator<br>  
e. Compute performance of the model using test data, and plot a confusion matrix<br>
 

### 3. Installation<a name="installation"></a>

 - The code should run with no issues using Python versions 3.*.
 - No extra besides the built-in libraries from Anaconda needed to run this project
 - Data Processing & Machine Learning Libraries: NumPy, SciPy, Pandas, Sciki-Learn
 - Data Visualization: Matplotlib, Seaborn

### 4. File Descriptions<a name="files"></a>

1. **Starbucks_Capstone_notebook.ipynb**  The analysis is contained within the jupyter notebook
2. **data_clean.py** Cleaning and preprocessing code for portfolio, profile and transcript datasets
3. **data_merge.py** Merge and proccessing code for for portfolio, profile and transcript datasets
4. README file
5. data folder containing three different files:

* portfolio.json - containing offer ids and meta data about each offer (duration, type, etc.)
* profile.json - demographic data for each customer
* transcript.json - records for transactions, offers received, offers viewed, and offers completed

Here is the schema and explanation of each variable in the files:

**portfolio.json**
* id (string) - offer id
* offer_type (string) - type of offer ie BOGO, discount, informational
* difficulty (int) - minimum required spend to complete an offer
* reward (int) - reward given for completing an offer
* duration (int) - time for offer to be open, in days
* channels (list of strings)

**profile.json**
* age (int) - age of the customer 
* became_member_on (int) - date when customer created an app account
* gender (str) - gender of the customer (note some entries contain 'O' for other rather than M or F)
* id (str) - customer id
* income (float) - customer's income

**transcript.json**
* event (str) - record description (ie transaction, offer received, offer viewed, etc.)
* person (str) - customer id
* time (int) - time in hours since start of test. The data begins at time t=0
* value - (dict of strings) - either an offer id or transaction amount depending on the record



### 5. Instructions<a name="instructions"></a>

1. The analysis is contained within the jupyter notebook.
2. All 3 json files should be located in data folder.


### 6. Acknowledgements<a name="licensing">

This project was completed as part of the [Udacity Data Science Nanodegree]. The dataset used in this project contains simulated data that mimics customer behavior on the Starbucks rewards mobile app. [Starbucks® Rewards program: Starbucks Coffee Company](https://www.starbucks.com/rewards/).

### 7. Results<a name="results"></a>
The main observations of the code are published on medium [here](https://medium.com/@m.sobrino.estevez/starbucks-customer-behavior-challenge-122a567f5b61)
