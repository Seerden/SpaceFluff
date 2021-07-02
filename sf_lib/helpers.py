import json
import sys
import numpy as np
import pandas as pd

def json_parser(data):
    return json.loads(data)
    
def df_to_json(df, path):
    "Save a dataframe `df` as .json file in the specified (relative) location `path` as './path.json'"
    df.to_json('{}/{}.json'.format(sys.path[0], path))

def get_cols(df, cols):
    '''
        Extract values of the specified columns `cols` from a dataframe `df`
        @param df: input dataframe
        @param cols: list of columns, e.g. ['Name', 'Date', 'Votes']
        @returns list of lists, where each list contains all values for that column,
        @example: 
            name, date, votes = get_cols(df, ['Name', 'Date', 'Votes'])
    '''
    return df[cols].T.values

def get_column_names(s, df):
    'Retrieve from a dataframe `df` the list of column names that start with (sub)string `s`'
    cols = df.columns.tolist()
    return list(filter(lambda x: x.startswith(s), cols))

# Fleiss' kappa computation
def get_P_i(row, answers):
    '''
        Compute the proportions for each answer for a single 'subject' (Space Fluff object)
        @param row: a row in `df_votes`-like dataframe
        @param answers: list of unique answers for task for which we're computing Fleiss' kappa

    '''
    n = sum(row.values())  # number of votes for this category for this object
    if n < 2:
        return 1
    else:
        val_sum = 0
        for answer in answers:
            val = row.get(answer, 0)
            val_sum += val*val
        return val_sum/(n*(n-1))

def fleiss_kappa(df, df_votes, task):
    '''
        Compute Fleiss' kappa for a single task, for a df_votes-like dataframe.
        @param df: dataframe where each row corresponds to a single classification
        @param df_votes: dataframe derived from `df`, where each row corresponds to a single object, 
            its parameters, and the number of votes it got for each answer in each task
        @param task: one of 'T0', 'T1', etc.
    '''
    
    N = df.shape[0]  # total number of votes

    answers = df[task].unique()
    
    p_js = np.array([df_votes['T0'].apply(lambda x: x.get(ans, 0)).values.tolist() for ans in answers])/N

    P_is = df_votes[task].apply(lambda x: get_P_i(x, answers))
    P_bar = sum(P_is)/df_votes.shape[0]
    P_bar_e = np.sum(p_js**2)

    kappa = (P_bar - P_bar_e)/(1 - P_bar_e)
    
    return kappa