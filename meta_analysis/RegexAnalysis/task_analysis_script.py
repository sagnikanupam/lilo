import json

from difflib import SequenceMatcher

def find_matching_substrings(input_list: list[str]):
    
    """
    Find all the matching substrings between the strings in the input list
    Args:
        input_list: list of strings
    Returns: 
        dict: dictionary with matching substrings as keys and their counts as values
    """

    substring_count = {}
    for i in range(0, len(input_list)):
        for j in range(i+1,len(input_list)):
            first_string = input_list[i]
            second_string = input_list[j]
            match = SequenceMatcher(None, first_string, second_string).find_longest_match(0, len(first_string), 0, len(second_string))
            matching_substring=first_string[match.a:match.a+match.size]
            if(matching_substring not in substring_count):
                substring_count[matching_substring]=1
            else:
                substring_count[matching_substring]+=1
    return dict(sorted(substring_count.items(), key=lambda item: item[1], reverse=True))

if __name__=="__main__":
    FILENAME = "lilo_paper_recreated_dreamcoder_iteration_15.json"
    data = {}
    with open(FILENAME) as f:
        data = json.load(f)
    summary = data["_summary"]
    train = data["train"]
    test = data["test"]
    train_solved_task_strings = []
    test_solved_task_strings = []
    train_unsolved_task_strings = []
    test_unsolved_task_strings = []
    solved_programs = []
    for task in train.keys():
        if len(train[task]["programs"])!=0:
            train_solved_task_strings.append(train[task]["task"])
            for program in train[task]["programs"]:
                solved_programs.append(program["program"])
        else:
            train_unsolved_task_strings.append(train[task]["task"])
    for task in test.keys():
        if len(test[task]["programs"])!=0:
            test_solved_task_strings.append(test[task]["task"])
            for program in test[task]["programs"]:
                solved_programs.append(program["program"])
        else:
            test_unsolved_task_strings.append(test[task]["task"])
    test_solved_matching_dict = find_matching_substrings(test_solved_task_strings)
    test_unsolved_matching_dict = find_matching_substrings(test_unsolved_task_strings)
    train_solved_matching_dict = find_matching_substrings(train_solved_task_strings)
    train_unsolved_matching_dict = find_matching_substrings(train_unsolved_task_strings)
    solved_programs_matching_dict = find_matching_substrings(solved_programs)
    with open("train_solved_tasks.json", "w") as fp:
        json.dump(train_solved_matching_dict, fp)
    with open("test_solved_tasks.json", "w") as fp:
        json.dump(test_solved_matching_dict , fp)
    with open("train_unsolved_tasks.json", "w") as fp:
        json.dump(train_unsolved_matching_dict, fp)
    with open("test_unsolved_tasks.json", "w") as fp:
        json.dump(test_unsolved_matching_dict, fp)
    with open("solved_programs.json", "w") as fp:
        json.dump(solved_programs_matching_dict, fp)
    with open("all_solved_programs.txt", "w") as fp:
        json.dump(solved_programs, fp)
    unsolved_set = set(train_unsolved_matching_dict.keys()).union(set(test_unsolved_matching_dict.keys()))
    solved_set = set(train_solved_matching_dict.keys()).union(set(test_solved_matching_dict.keys()))
    distinct_unsolved_set = unsolved_set - solved_set
    unsolved_problems_dict = {}
    for key in list(distinct_unsolved_set):
        selected_key_count = 0
        if (key in train_unsolved_matching_dict.keys() and train_unsolved_matching_dict[key]>9):
            selected_key_count += train_unsolved_matching_dict[key]
        if (key in test_unsolved_matching_dict.keys() and test_unsolved_matching_dict[key]>9):
            selected_key_count += test_unsolved_matching_dict[key]
        if selected_key_count>0:
            unsolved_problems_dict[key] = selected_key_count
    unsolved_problems_dict = dict(sorted(unsolved_problems_dict.items(), key=lambda item: item[1], reverse=True))
    with open("unsolved_problems.json", "w") as fp:
        json.dump(unsolved_problems_dict, fp)
