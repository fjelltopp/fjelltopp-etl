import requests
import pandas as pd
import xmltodict


class OdkError(Exception):
    pass


def get_odk_data(aggregate_url: str, username: str, password: str, form_id: str) -> pd.DataFrame:
    submissions = __get_odk_submissions(aggregate_url, form_id, password, username)
    return pd.DataFrame(submissions)

def get_flattened_odk_data(aggregate_url: str, username: str, password: str, form_id: str, form_structure: list) -> pd.DataFrame:
    submissions = __get_odk_submissions(aggregate_url, form_id, password, username)
    return pd.DataFrame(submissions)


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
    submissions = []
    for submission_id in submissions_dict["idList"]["id"]:
        submissions.append(
            __get_odk_submission(aggregate_url,
                                 auth,
                                 form_id,
                                 submission_id))
    return submissions


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
