from github import Github
import os
import pandas as pd
import datetime as dt


def get_gh_issues(repo='DLMP-AI/ID-Consultation') -> object:
    g = Github(os.environ["GH_TOKEN"])
    u = g.get_user()
    login = u.login  # Bug in pyGithub
    r = g.get_repo(repo)
    issue_df = pd.DataFrame()
    dt_now = dt.datetime.now()

    for e in r.get_issues():
        try:
            due_date = (e.milestone.due_on - dt_now) < dt.timedelta(days=0)
        except:
            due_date = False

        if hasattr(e, 'assignees'):
            if e.assignees.__len__() < 1:
                assignees = 'Unassigned'
            else:
                try:
                    assignees = ','.join([x.name for x in e.assignees])
                except TypeError:
                    assignees = ','.join([x.login for x in e.assignees])
        else:
            assignees = 'Unassigned'

        try:
            created = e.created_at.date().strftime("%Y-%m-%d")
        except:
            created = dt_now.strftime("%Y-%m-%d")

        tmp = {
            'title': [e.title],
            'state': [e.state],
            'overdue': [due_date],
            'assignees': [assignees],
            'created': [created]
        }
        tmp_df = pd.DataFrame(tmp, index=[0])
        issue_df = issue_df.append(tmp_df)

    return issue_df


def get_gh_milestones(repo='DLMP-AI/ID-Consultation'):
    g = Github(os.environ["GH_TOKEN"])
    u = g.get_user()
    login = u.login  # Bug in pyGithub
    r = g.get_repo(repo)
    milestones_df = pd.DataFrame()
    dt_now = dt.datetime.now().strftime("%Y-%m-%d")

    for m in r.get_milestones():

        if not m.due_on:
            due_date = dt_now
            overdue = False
        else:
            due_date = m.due_on.strftime("%Y-%m-%d")
            try:
                overdue = (m.due_on - dt_now) < dt.timedelta(days=0)
            except:
                overdue = False

        tmp = {
            'title': [m.title],
            'state': [m.state],
            'due_date': [due_date],
            'open_issues': [m.open_issues],
            'overdue': [overdue],
            'now': [dt_now]
        }
        tmp_df = pd.DataFrame(tmp, index=[0])
        milestones_df = milestones_df.append(tmp_df)

    return milestones_df
