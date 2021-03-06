import pandas as pd
import numpy as np
import os
import json
from datetime import date

def getFilename(subject_data):
    """
    Given the subject_data field from a row of one of our SpaceFluff dataframes, extract the name of the object being classified
    by extracting the 'Filename'|'image'|'IMAGE' field".

    To be used with df[column].apply()

    @returns {string} filename of the object being classified, including the extension '_insp.png'
    """

    keys = list(subject_data.values())[0].keys()
    accessKey = (
        "Filename" if "Filename" in keys else "image" if "image" in keys else "IMAGE" if "IMAGE" in keys else None)

    if accessKey:
        return list(subject_data.values())[0][accessKey][:-9]
    else:
        print("No filename found!")

def getMetadataValue(metadata, field):
    '''
        @param metadata metadata column from a row in a SpaceFluff dataframe
        @param {string} field: 'retired' | 'already_seen'
        @returns {boolean} value of `field` within the row's metadata column
    '''
    return metadata['subject_selection_state'][field]

def parseTime(created_at):
    '''
    @param {df column} created_at: df['created_at'] column
    '''
    return pd.to_datetime(created_at, format="%Y-%m-%d %H:%M:%S %Z")

def getGroupSize(group):
    '''
        @param {pd.core.frame.DataFrame} pandas dataframe group
        @returns number of rows in group (corresponds to number of columns in case of parsed SpaceFluff dataframe)
    '''
    return group.shape[0]

def extract_task_value(task_index, row):
    try:
        return row[task_index]['value']
    except:
        return

def percentageVotesForAnswer(counts, answer):
    '''
    @param counts: a df column like {galaxy: 15, group of objects (cluster): 10, something else/empty center: 2}
    @paramanswer: one of the keys of `counts`
    '''

    totalVotes = sum(counts.values())

    if not answer in counts.keys():
        return 0

    votesForAnswer = counts[answer]

    return round(100*votesForAnswer/totalVotes, 1)

def extractTaskValue(annotations, task):
    '''
    @param {list} annotations: annotations column for a row in a SpaceFluff dataframe
    @param {string} task: one of 'Ti', where i \in 0,2,1,3,4,5,9
    @returns {string | None} value the user provided for the given task, or None
    '''

    filtered = list(filter(lambda x: x['task'] == task, annotations))
    if len(filtered) > 0:
        return filtered[0]['value']

def extract_retired_info(subject_data):
    '''
        @param subject_data: (dataframe 'subject_data' column)
    '''
    return list(subject_data.values())[0]["retired"]

def get_power_users(df, vote_count_threshold):
    """
    @param df: parsed dataframe where each row is a single classification
    @param {int} vote_count_threshold: return only users that made at least this many valid classifications
    """
    
    groupby_username = df[['user_name']].groupby(['user_name'])
    groupby_username_filtered = groupby_username.filter(lambda x: x.shape[0] >= vote_count_threshold)

    grouped = groupby_username_filtered.groupby(['user_name'])

    filtered_usernames_and_votes = []
    for username, vote_count in grouped:
        filtered_usernames_and_votes.append({
            "username": username,
            "votes": len(vote_count)
        })

    return filtered_usernames_and_votes

def get_task_0_value_counts(row):
    "Get task 0 value counts for one row of a group of classifications"
    row = list(row)

    # value_counts = {answer: 0 for answer in answer_types}
    value_counts = {}
    for vote in row:
        if value_counts.get(vote):
            value_counts[vote] += 1
        else:
            value_counts[vote] = 1
    
    return value_counts, len(row)

def as_array(lst):
    'Turn a Python list into a NumPy array'
    if type(lst) == np.ndarray:
        return lst
    return np.array(lst)

def get_running_vote_fraction(df):
    """
    Returns a list of 
        (% votes by users that case <= n votes)/total votes 
    as a function of n
    @param df: `df`-like dataframe, where each row corresponds to a single classification made by a single user
    """
    users_and_classification_counts = []

    for k, v in df.groupby('user_name').groups.items():
        users_and_classification_counts.append({
            'username': k, 
            'classifications': len(v)
        })
        
    cls_per_user = [entry['classifications'] for entry in users_and_classification_counts]    
    total_votes = sum(cls_per_user)  # total number of votes made
    sorted_vote_counts = sorted(cls_per_user)  # sorted list of number of classifications per user

    # create dictionary with keys: # votes per user, values: # users that cast that amount of votes
    countDict = {}
    for entry in sorted_vote_counts:
        countDict[entry] = countDict.get(entry, 0) + 1

    fractions = []
    for vote_count, occurrence_rate in countDict.items():
        fractions.append([vote_count, vote_count*occurrence_rate/total_votes, occurrence_rate])
    counts, fractions, users_included = as_array(fractions).T

    # create a running fraction of total votes cast in a single loop
    running_fraction = []
    for i, fr in enumerate(fractions):
        if i == 0:
            val = fr
        else:
            val = fr+running_fraction[i-1]
        running_fraction.append(val)    

    return [   
        users_and_classification_counts,
        cls_per_user, 
        counts,
        running_fraction
    ]