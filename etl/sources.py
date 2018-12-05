import requests
import pandas as pd
import xmltodict
from pandas.io.json import json_normalize


class OdkError(Exception):
    pass


def get_odk_data(aggregate_url: str, username: str, password: str, form_id: str) -> pd.DataFrame:
    submissions = __get_odk_submissions(aggregate_url, form_id, password, username)
    return pd.DataFrame(submissions)

def get_flattened_odk_data(aggregate_url: str, username: str, password: str, form_id: str, deep_nested_column: str, to_split_column: str) -> pd.DataFrame:
    result = pd.DataFrame()
    for submission in __get_odk_submissions(aggregate_url, form_id, password, username):
        activity_group_ = submission[deep_nested_column]
        if type(activity_group_) != list:
            submission[deep_nested_column] = [activity_group_]

        activities_df = json_normalize(submission[deep_nested_column], errors='ignore')
        activities_df_prop_split = pd.DataFrame(columns=activities_df.columns)
        for _, activity in activities_df.iterrows():
            for settlement in activity[to_split_column].split():
                new_row = activity.copy()
                new_row[to_split_column] = settlement
                activities_df_prop_split = activities_df_prop_split.append(new_row)
        activities_df_prop_split.reset_index(drop=True, inplace=True)
        size = len(activities_df_prop_split)
        data_frame = json_normalize(submission).drop(columns=[deep_nested_column])
        data_frame_ext = pd.concat([data_frame] * size, ignore_index=True)

        submission_df = pd.concat([activities_df_prop_split, data_frame_ext], axis=1)
        result = pd.concat([result, submission_df])
    return result


def __get_odk_submissions(aggregate_url, form_id, password, username):
    auth = requests.auth.HTTPDigestAuth(username, password)
    submissions = requests.get(aggregate_url + "/view/submissionList",
                               params={"formId": form_id}, auth=auth)
    if submissions.status_code >= 400:
        raise OdkError(f"Failed to get submissions for form {form_id}")
    try:
        submissions_dict = xmltodict.parse(submissions.text)["idChunk"]
    except xmltodict.ParsingInterrupted:
        raise ValueError("Can not parse xml")
    for submission_id in submissions_dict["idList"]["id"]:
        yield __get_odk_submission(aggregate_url, auth, form_id, submission_id)


def __get_odk_submission(aggregate_url: str, auth: requests.auth.HTTPDigestAuth,
                         form_id: str, uuid: str) -> dict:
    form_id_string = f'{form_id}[@version=null and @uiVersion=null]/{form_id}[@key={uuid}]'
    submission = requests.get(aggregate_url + "/view/downloadSubmission",
                              params={"formId": form_id_string}, auth=auth)
    if submission.status_code >= 400:
        raise OdkError(f"Failed to get submissions for form {form_id}")
    submission = xmltodict.parse(submission.text)["submission"]["data"][form_id]
    return __fix_odk_data(submission)


def __fix_odk_data(form_submission: dict) -> dict:
    return_submission = {}
    for key, value in form_submission.items():
        if key not in ["orx:meta"]:
            new_key = key.replace("@", "")
            return_submission[new_key] = value
    return return_submission
