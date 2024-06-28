import pandas as pd
import json

ORIGINAL_DATASET_FILEPATHS = ['conpoleDatasetPrefix.csv']
GOLDEN_DATASET_FILEPATHS = ['goldenDataset.csv']
AUTO_AUGMENTATION_JSON = []
ORIGINAL_TRAIN_SPLIT = 0.7
RANDOM_SEED = 111

def makeTask(row: int, dataset: pd.DataFrame, prefixInputIndex: int = 2, prefixOutputIndex: int = 5):
    """
    Generates (tstr -> tstr) tasks from equations read from .csv file.

    Args:
        row (integer): integer that determines the row of the dataset from 
            which the equation is read.
        dataset (pandas DataFrame): pandas dataframe containing the equations 
            dataset
        prefixInputIndex (integer): integer that determines the column index   
            corresponding to the input equation (in prefix form) in the dataset
        prefixOutputIndex (integer): integer that determines the column index 
            corresponding to the output equation (in prefix form) in the dataset 

    Returns:
        dictionary: a dictionary with the following format:
            {
                "name": <string containing the name of the task>,
                "example": [
                    {"i": <input example>, "o": <corresponding output>},
                    .....
                ]
            }
    """
    inputOutput = {"i":str(dataset.iat[row, prefixInputIndex]), "o": str(dataset.iat[row, prefixOutputIndex])}
    return {"name": "mathEq"+str(row) + ": " + inputOutput["i"] + "=>" + inputOutput["o"], "examples": [inputOutput for _ in range(5000)]}

def makeIndexTask(index:int):
    """
    Generates (tint -> tint) tasks such that the desired integer is produced as an index on solving the task

    Args:
        index (int): desired integer to be produced that can be used to index into math DSL subtree.

    Returns:
        dictionary: a dictionary with the following format:
            {
                "name": <string containing the name of the task>,
                "example": [
                    {"i": <input example>, "o": <corresponding output>},
                    .....
                ]
            }
    """
    inputOutput = {"i":0, "o": index}
    return {"name": "index_"+str(index) + ": " + str(inputOutput["i"]) + "=>" + str(inputOutput["o"]), "examples": [inputOutput for _ in range(5000)]}

def checkLemmaConpoleAccuracy(test_problem_df:pd.DataFrame, model_result_df: pd.DataFrame, model_name: str):
    """
    Check accuracy of ConPoLe/Lemma model results

    Args:
        test_df (pd.DataFrame): Dataframe containing test problems
        model_result_df (pd.DataFrame): Dataframe containing results of Conpole or Lemma
        model_name (str): model name to be printed
    
    """
    count = 0
    test_problem_df["tmp"] = test_problem_df.index
    model_result_equation_nums = model_result_df["Equation Number"].to_list()
    for index in range(len(test_problem_df)):
        if test_problem_df["tmp"].iloc[index] in model_result_equation_nums:
            count+=1
    print(f"{model_name} Num Problems Solved: {count} / {len(test_problem_df)}")
    print(f"{model_name} Accuracy: {count / len(test_problem_df)}")

if __name__ =="__main__":
    datasetExpVal = "INDEX" #Can be ORIGINAL, GOLDEN, TRAININGAUGMENTEDGOLDEN, OR AUGMENTED FOR GENERATING DATASETS

    #  Experiment Type 1: Original Cognitive Tutor Problems Only
    if datasetExpVal == "ORIGINAL":
        allEqDatasets = [pd.read_csv(dataset) for dataset in ORIGINAL_DATASET_FILEPATHS]
        allEqDf = pd.concat([data for data in allEqDatasets], ignore_index=True)
        conpoleDf = pd.read_csv("generatedConpoleSolutions-CScores.csv")
        lemmaDf = pd.read_csv("generatedLemmaSolutions-CScores.csv")
        numEqs = allEqDf.shape[0]
        numTrainSamples = int(numEqs*ORIGINAL_TRAIN_SPLIT)
        print("Number of training samples: ", numTrainSamples)
        print("Number of testing samples: ", numEqs - numTrainSamples)
        trainDf = allEqDf.sample(n=numTrainSamples, random_state=RANDOM_SEED)
        testDf = allEqDf.drop(trainDf.index).sample(frac=1, random_state=RANDOM_SEED)
        checkLemmaConpoleAccuracy(testDf, conpoleDf, "ConPoLe")
        checkLemmaConpoleAccuracy(testDf, lemmaDf, "Lemma")
        trainTasks = [makeTask(i, trainDf) for i in range(numTrainSamples)]
        testTasks = [makeTask(i, testDf) for i in range(numEqs - numTrainSamples)]
        # save train and test datasets json
        with open('cognitiveTutor/train/tasks.json', 'w') as f:
            json.dump(trainTasks, f)
        with open('cognitiveTutor/test/tasks.json', 'w') as f:
            json.dump(testTasks, f)

    # Experiment Type 2: Golden Dataset Problems in training, Cognitive Tutor Problem in Testing
    
    if datasetExpVal == "GOLDEN":
        trainDatasets = [pd.read_csv(dataset) for dataset in GOLDEN_DATASET_FILEPATHS]
        trainDf = pd.concat([data for data in trainDatasets], ignore_index=True)
        numTrainSamples = trainDf.shape[0]
        testDatasets = [pd.read_csv(dataset) for dataset in ORIGINAL_DATASET_FILEPATHS]
        testDf = pd.concat([data for data in testDatasets], ignore_index=True)
        numTestSamples = testDf.shape[0]
        print("Number of training samples: ", numTrainSamples)
        print("Number of testing samples: ", numTestSamples)
        trainTasks = [makeTask(i, trainDf) for i in range(numTrainSamples)]
        testTasks = [makeTask(i, testDf) for i in range(numTestSamples)]
        # save train and test datasets json
        with open('goldenDataset/train/tasks.json', 'w') as f:
            json.dump(trainTasks, f)
        with open('goldenDataset/test/tasks.json', 'w') as f:
            json.dump(testTasks, f)
    
    # Experiment Type 2: Golden Dataset Problems in training, Cognitive Tutor Problem in Testing
    
    if datasetExpVal == "TRAININGAUGMENTEDGOLDEN":
        allEqDatasets = [pd.read_csv(dataset) for dataset in ORIGINAL_DATASET_FILEPATHS]
        allEqDf = pd.concat([data for data in allEqDatasets], ignore_index=True)
        numEqs = allEqDf.shape[0]
        numTrainSamples = int(numEqs*ORIGINAL_TRAIN_SPLIT)
        goldenDatasets = [pd.read_csv(dataset) for dataset in GOLDEN_DATASET_FILEPATHS]
        goldenDf = pd.concat([data for data in goldenDatasets], ignore_index=True)
        numGoldenSamples = goldenDf.shape[0]
        print("Number of training samples: ", numTrainSamples + numGoldenSamples)
        print("Number of testing samples: ", numEqs - numTrainSamples)
        trainDf = allEqDf.sample(n=numTrainSamples, random_state=RANDOM_SEED)
        testDf = allEqDf.drop(trainDf.index).sample(frac=1, random_state=RANDOM_SEED)
        trainTasks = [makeTask(i, trainDf) for i in range(numTrainSamples)] + [makeTask(i, goldenDf) for i in range(numGoldenSamples)]
        testTasks = [makeTask(i, testDf) for i in range(numEqs - numTrainSamples)]
        # save train and test datasets json
        with open('trainingAugmentedGoldenDataset/train/tasks.json', 'w') as f:
            json.dump(trainTasks, f)
        with open('trainingAugmentedGoldenDataset/test/tasks.json', 'w') as f:
            json.dump(testTasks, f)
    
    if datasetExpVal == "AUTOAUGMENTATION":
        pass

    if datasetExpVal == "INDEX":
        allEqDatasets = [pd.read_csv(dataset) for dataset in ORIGINAL_DATASET_FILEPATHS]
        allEqDf = pd.concat([data for data in allEqDatasets], ignore_index=True)
        numEqs = allEqDf.shape[0]
        numTrainSamples = int(numEqs*ORIGINAL_TRAIN_SPLIT)
        print("Number of training samples: ", numTrainSamples+15)
        print("Number of testing samples: ", numEqs - numTrainSamples)
        trainDf = allEqDf.sample(n=numTrainSamples, random_state=RANDOM_SEED)
        testDf = allEqDf.drop(trainDf.index).sample(frac=1, random_state=RANDOM_SEED)
        trainTasks = [makeTask(i, trainDf) for i in range(numTrainSamples)] + [makeIndexTask(index) for index in range(11, 25)]
        testTasks = [makeTask(i, testDf) for i in range(numEqs - numTrainSamples)]
        # save train and test datasets json
        with open('trainingWithIndex/train/tasks.json', 'w') as f:
            json.dump(trainTasks, f)
        with open('trainingWithIndex/test/tasks.json', 'w') as f:
            json.dump(testTasks, f)