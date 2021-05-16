import os
from .sf import (
    getFilename, 
    extract_task_value, 
    parseTime, 
    get_power_users, 
    percentageVotesForAnswer, 
    extractTaskValue,
    get_task_0_value_counts)
from .helpers import json_parser
from datetime import date
import pandas as pd
import numpy as np
import json

def make_df_classify():
    converters = {}  # create converters dict to pass to pd.read_csv (speed up the read_csv call by quite a bit)
    for column in ['annotations', 'subject_data', 'metadata']:
        converters[column] = json_parser

    cwd = os.path.dirname(os.path.abspath(__file__))
    loc = os.path.join(cwd, '../SpaceFluff/zooniverse_exports/classify-classifications.csv')
    df = pd.read_csv(loc, delimiter=",", converters=converters)
    
    df['Filename'] = df['subject_data'].apply(getFilename)

    task_indices = [0,1]  # these are the task indices from the 'classify' workflow. we can make this function work for the 'hardcore' workflow by making this a function param
    tasks = ['T{}'.format(i) for i in task_indices]
    for task in tasks:
        df[task] = df['annotations'].apply(lambda x: extractTaskValue(x, task))

    df = df[~df['T0'].isnull()]  # if user didn't answer T0, the classification is void and can be removed safely

    # filter out classifications from beta
    df['created_at'] = parseTime(df['created_at'])
    end_of_beta = pd.Timestamp(date(2020, 10, 20), tz='utc')
    df = df[df['created_at'] > end_of_beta]

    # create temporary isRetired and alreadySeen rows
    df['isRetired'] = df['metadata'].apply(lambda x: x['subject_selection_state']['retired'])
    df['alreadySeen'] = df['metadata'].apply(lambda x: x['subject_selection_state']['already_seen'])

    df = df[~df['isRetired'] & ~df['alreadySeen']]  # remove rows where isRetired or alreadySeen
    df.drop(['isRetired', 'alreadySeen'], axis=1, inplace=True)  # remove isRetired and alreadySeen columns since they're obsolete hereafter

    return df

def make_df_vote_threshold(df, vote_count_threshold):
    users_and_votes = get_power_users(df, vote_count_threshold)
    usernames = [user['username'] for user in users_and_votes]
    
    df = df[df['user_name'].isin(usernames)]
    
    return df

def make_df_tasks_with_props(df, candidate_names, object_info):
    # create a temporary dataframe containing only classifications where 'task0' == 'Galaxy'
    df_galaxy = df[df['T0'] == 'Galaxy']
    galaxy_names = df_galaxy['Filename']

    groupby_name = df_galaxy[['Filename', 'T0', 'T1']].groupby(['Filename'])

    galaxy_task1_values = []
    for name in set(galaxy_names):
        group = groupby_name.get_group(name)        # get all classifications of this object from df
        
        rowObj = {
            "name": name
        }
        
        for answer in ['Fluffy', 'Bright']:  # add 'fluffy' and 'bright' columns
            rowObj['% {}'.format(answer)] = round(list(group['T1']).count(answer)*100/group.shape[0], 1)
        
        none_count = group[group['T1'].isnull()].shape[0]  # also manually add 'None' row since None is parsed to NaN otherwise
        rowObj['% None'] = round(none_count*100/group.shape[0], 1)
        
        galaxy_task1_values.append(rowObj)  # append rowObj to list

    df_task1 = pd.DataFrame(galaxy_task1_values)
    df_task0 = make_df_task0(df, candidate_names)
    df_tasks = df_task1.merge(df_task0, on='name', how='outer')
    df_tasks_with_props = df_tasks.merge(object_info, how='outer', on='name')  # merge properties onto dataframe
    df_tasks_with_props = df_tasks_with_props[~df_tasks_with_props['# votes'].isnull()]  # filter out objects without actual votes

    return df_tasks_with_props 

def make_df_task0(df, candidate_names):
    # group df by filename, so that each group contains only rows belonging to that object
    gr = df[['Filename', 'T0']].groupby('Filename')

    task0Values = []  # create empty list to push results to
    for objectName in candidate_names:
        # loop over every group created above to accumulate 'task 0' votes ('galaxy'/'group of objects'/'something else')
        try:
            task0_values = gr.get_group(objectName)['T0']
            counts, votes = get_task_0_value_counts(task0_values)

            countObj = {
                "name": objectName,
                "counts": counts,
                "# votes": votes
            }

            task0Values.append(countObj)
        except:
            continue

    df_task0 = pd.DataFrame(task0Values)

    answer_types = ['Galaxy', 'Group of objects (Cluster)', 'Something else/empty center']

    for ans_type in answer_types:
        vote_percentage_column = df_task0['counts'].apply(
            lambda x: percentageVotesForAnswer(x, ans_type))
        df_task0['% votes {}'.format(ans_type)] = vote_percentage_column

    # filter dataframe and only leave objects with more than 5 votes
    # df_task0 = df_task0[df_task0['# votes'] > 5]

    return df_task0

def make_df_vote_threshold(df, vote_count_threshold):
    users_and_votes = get_power_users(df, vote_count_threshold)
    usernames = [user['username'] for user in users_and_votes]
    
    df = df[df['user_name'].isin(usernames)]
    
    return df