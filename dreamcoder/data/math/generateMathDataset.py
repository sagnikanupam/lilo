import pandas as pd
import json

ORIGINAL_DATASET_FILEPATHS = ['conpoleDatasetPrefix.csv']
GOLDEN_DATASET_FILEPATHS = ['goldenDataset.csv']
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

if __name__ =="__main__":
    datasetExpVal = "ORIGINAL" #Can be ORIGINAL, GOLDEN, TRAININGAUGMENTEDGOLDEN, OR AUGMENTED FOR GENERATING DATASETS

    #  Experiment Type 1: Original Cognitive Tutor Problems Only
    if datasetExpVal == "ORIGINAL":
        allEqDatasets = [pd.read_csv(dataset) for dataset in ORIGINAL_DATASET_FILEPATHS]
        allEqDf = pd.concat([data for data in allEqDatasets], ignore_index=True)
        numEqs = allEqDf.shape[0]
        numTrainSamples = int(numEqs*ORIGINAL_TRAIN_SPLIT)
        print("Number of training samples: ", numTrainSamples)
        print("Number of testing samples: ", numEqs - numTrainSamples)
        trainDf = allEqDf.sample(n=numTrainSamples, random_state=RANDOM_SEED)
        testDf = allEqDf.drop(trainDf.index).sample(frac=1, random_state=RANDOM_SEED)
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