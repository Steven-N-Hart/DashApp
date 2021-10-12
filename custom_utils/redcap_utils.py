import os
import requests
import pandas as pd


def _get_rc_token(study='DLMP-AI/ID-Consultation'):
    if study == 'DLMP-AI/ID-Consultation':
        token = os.environ['REDCAP_IDC_TOKEN']
    elif study == 'DLMP-AI/m087494_ganomaly':
        token = os.environ['REDCAP_TSR_TOKEN']
    else:
        raise KeyError(f"This study ({study}) is not configured! ")
    return token


def get_redcap_data(study='DLMP-AI/ID-Consultation'):
    token = _get_rc_token(study=study)
    data = {
        'token': token,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'rawOrLabel': 'label',
        'rawOrLabelHeaders': 'label',
        'exportCheckboxLabel': 'true',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    r = requests.post('https://redcapcln-prod.mayo.edu/redcap/api/', data=data, verify=False)
    df = pd.DataFrame(r.json())
    return df
