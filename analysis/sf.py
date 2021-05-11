import pandas as pd
from dateutil.parser import parse


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


def parseTime(time_string):
    '''
        @param {string} time_string: time string from `created_at` field in a SpaceFluff dataframe, e.g. 2020-09-02 07:47:42 UTC
        @returns {pd.Timestamp} `time_string` parsed as pandas Timestamp
    '''
    return pd.Timestamp(parse(time_string))


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
