from github import Github
import os
import pandas as pd
import datetime as dt
import logging

def get_gh_issues(repo='DLMP-AI/ID-Consultation') -> object:
    g = Github(os.environ["GH_TOKEN"])
    u = g.get_user()
    login = u.login # Bug in pyGithub
    r = g.get_repo(repo)
    issue_df = pd.DataFrame()
    dt_now = dt.datetime.now()

    for e in r.get_issues():
        try:
            due_date = (e.milestone.due_on - dt_now) < dt.timedelta(days=0)
        except AttributeError:
            due_date = None

        try:
            assignees = ','.join([x.name for x in e.assignees])
        except TypeError:
            assignees = None

        tmp = {
            'title': [e.title],
            'state': [e.state],
            'overdue': [due_date],
            'assignees': [assignees],
            'created': [e.created_at.date().strftime("%m-%d-%Y")]
        }
        tmp_df = pd.DataFrame(tmp, index=[0])
        issue_df = issue_df.append(tmp_df)

    return issue_df


def get_gh_milestones(repo='DLMP-AI/ID-Consultation'):
    g = Github(os.environ["GH_TOKEN"])
    u = g.get_user()
    login = u.login # Bug in pyGithub
    r = g.get_repo(repo)
    milestones_df = pd.DataFrame()
    dt_now = dt.datetime.now()

    for m in r.get_milestones():
        tmp = {
            'title': m.title,
            'state': m.state,
            'due_date': m.due_on.strftime("%m-%d-%Y"),
            'open_issues': m.open_issues,
            'overdue': (m.due_on - dt_now) < dt.timedelta(days=0)
        }
        tmp_df = pd.DataFrame(tmp, index=[0])
        milestones_df = milestones_df.append(tmp_df)

    return milestones_df
