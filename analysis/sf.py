import pandas as pd
import numpy as np
import os

def getFilename(subject_data):
    """
    Given the subject_data column from a row of one of our SpaceFluff dataframes, extract the name of the object being classified
    by extracting the 'Filename'|'image'|'IMAGE' field"

    @returns {string} filename of the object being classified, including the extension '_insp.png'
    """

    keys = list(subject_data.values())[0].keys()
    accessKey = (
        "Filename" if "Filename" in keys else "image" if "image" in keys else "IMAGE" if "IMAGE" in keys else None)

    if accessKey:
        return list(subject_data.values())[0][accessKey]
    else:
        print("No filename found!")


def getObjectName(subject_data):
    '''
        @param {subject_data} subject_data column of one row of a SpaceFluff dataframe
        @returns {string} name of the object that was classified, without the _insp.png extension
    '''
    return getFilename(subject_data)[:-9]


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
    `counts` is a df column like {galaxy: 15, group of objects (cluster): 10, something else/empty center: 2}
    `answer` is one of the keys of counts
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

def make_df_task0(df, candidate_names):
    # group df by filename, so that each group contains only rows belonging to that object
    gr = df.groupby('Filename')

    # create empty list to push results to
    task0Values = []

    # loop over every group created above to accumulate 'task 0' votes ('galaxy'/'group of objects'/'something else')
    
    for objectName in candidate_names:
        try:
            task0 = gr.get_group(objectName)['Task0']

            counts = task0.value_counts().to_dict()

            countObj = {
                "name": objectName,
                "counts": counts,
            }

            task0Values.append(countObj)
        except:
            continue

    df_task0 = pd.DataFrame(task0Values)

    answer_types = ['Galaxy', 'Group of objects (Cluster)', 'Something else/empty center']

    df_task0['# votes'] = df_task0['counts'].apply(lambda x: sum(x.values()))

    for ans_type in answer_types:
        vote_percentage_column = df_task0['counts'].apply(lambda x: percentageVotesForAnswer(x, ans_type))
        df_task0['% votes {}'.format(ans_type)] = vote_percentage_column

    df_task0['name'] = df_task0['name'].apply(lambda x: x[:-9])

    # filter dataframe and only leave objects with more than 5 votes
    df_task0 = df_task0[df_task0['# votes'] > 5]
    
    return df_task0

def extract_retired_info(subject_data):
    '''
        @param subject_data: (dataframe 'subject_data' column)
    '''
    return list(subject_data.values())[0]["retired"]

def make_df_with_props(df, candidate_names):
    df["retired"] = df["subject_data"].apply(extract_retired_info)
    df_retired = df[~df["retired"].isnull()]

    gr_retired = df_retired.groupby(["Filename"])  # group by filename
    props = ["R", "RA", "DEC", "G-I"]              # extract object properties

    props_list = []

    for objectName in candidate_names:
        # get group
        try:
            row = gr_retired.get_group(objectName)['subject_data']

            # get first entry in the group (props should be the same for every entry since they all describe the same object)
            firstEntry = row.iloc[0]
            values  = list(firstEntry.values())[0]

            # create object with name, properties
            entry = {'name': objectName[:-9]}

            for key in props:
                entry[key] = values[key]

            props_list.append(entry)
        except:
            continue
            
    df_props = pd.DataFrame(props_list)

    df_task0 = make_df_task0(df, candidate_names)
    df_with_props = df_task0.merge(df_props, how='outer')

    return df_with_props

def make_df_tasks_with_props(df, candidate_names, object_info):
    # create a temporary dataframe containing only classifications where 'task0' == 'Galaxy'
    # df_galaxy = df[(df['Task0'] == 'Galaxy') & (df['annotations'].map(len) > 1)]
    df_galaxy = df[(df['Task0'] == 'Galaxy')]
    galaxy_names = df_galaxy['Filename']

    gr_by_name = df.groupby(['Filename'])

    galaxy_task1_values = []

    for name in set(galaxy_names):
        group = gr_by_name.get_group(name)        # get all classifications of this object from df
        group = group[group['Task0'] == 'Galaxy'] # select only rows where task0 was answered with 'galaxy'
        
        rowObj = {}
        
        # add 'fluffy' and 'bright' rows
        for answer in ['Fluffy', 'Bright']:
            rowObj['% {}'.format(answer)] = round(list(group['Task1']).count(answer)*100/group.shape[0], 1)
        
        # also manually add 'None' row since None is parsed to NaN otherwise
        none_count = group[group['Task1'].isnull()].shape[0]
        rowObj['% None'] = round(none_count*100/group.shape[0], 1)
        rowObj['name'] = name[:-9]  # add object's name to rowObj
        
        galaxy_task1_values.append(rowObj)  # append rowObj to list

    df_task1 = pd.DataFrame(galaxy_task1_values)

    df_task0 = make_df_task0(df, candidate_names)
    df_tasks = df_task1.merge(df_task0, on='name', how='outer')

    # merge properties onto dataframe
    df_tasks_with_props = df_tasks.merge(object_info, how='outer', on='name')

    # filter out objects without actual votes
    df_tasks_with_props = df_tasks_with_props[~df_tasks_with_props['# votes'].isnull()]

    return df_tasks_with_props 

def get_power_users(df, vote_count_threshold):
    """
    @param df: parsed dataframe where each row is a single classification
    @param {int} vote_count_threshold: return only users that made at least this many valid classifications
    """
    
    groupby_username = df.groupby(['user_name'])
    groupby_username_filtered = groupby_username.filter(lambda x: x.shape[0] >= vote_count_threshold)

    grouped = groupby_username_filtered.groupby(['user_name'])

    filtered_usernames_and_votes = []
    for username, vote_count in grouped:
        filtered_usernames_and_votes.append({
            "username": username,
            "votes": len(vote_count)
        })

    return filtered_usernames_and_votes

def make_df_vote_threshold(df, vote_count_threshold):
    users_and_votes = get_power_users(df, vote_count_threshold)
    usernames = [user['username'] for user in users_and_votes]
    
    df = df[df['user_name'].isin(usernames)]
    
    return df