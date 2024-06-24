# Datasets For The Math Domain

Before running any experiments, unzip goldenDataset/test/tasks.json.zip to goldenDataset/test/tasks.json and trainingAugmentedGoldenDataset/train/tasks.json.zip to trainingAugmentedGoldenDataset/train/tasks.json

The datasets for the experiments run in the Math Domain are defined as follows:

* cognitiveTutorDataset.txt contains the original math equations used by ConPoLe, and conpoleDatasetPrefix.csv contains these equations in prefix format. The cognitiveTutor folder contains these tasks split in 70-30 ratio in favor of training tasks, in json files under train/tasks.json and test/tasks.json

* goldenDataset.csv contains an example of a "Golden Dataset" built by the authors by examining the ConPoLe dataset closely so that Dreamcoder would develop the abstractions needed to solve the mathematical equations in the dataset. These tasks are stored in json format under goldenDataset/train/tasks.json, whereas goldenDataset/test/tasks.json contains the original 284 Cognitive Tutor Equations used in the ConPoLe paper.

*trainingAugmentedGoldenDataset/train/tasks.json contains the equations in cognitiveTutorDataset/train/tasks.json combined with the equations in goldenDataset/train/tasks.json. trainingAugmentedGoldenDataset/test/tasks.json contains the testing tasks present in cognitiveTutor/test/tasks.json