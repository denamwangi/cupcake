from flask import Flask, request, jsonify, redirect, Response, json
import os
import pprint
import requests


def get_repo_commits():
    """ Grabs all the authors and their number of commits to the repo
        returns {'author_name': int no_of_commits}
    """
    request_url = 'https://api.github.com/repos/denamwangi/CupCake/commits'
    response = json.loads(requests.get(request_url).content)

    committers = {}
    for each_commit in response:
        # import ipdb; ipdb.set_trace()
        author = each_commit['author']['login']
        committers[author] = committers.get(author, 0) + 1

    return committers


def get_repo_reviews():
    """ Grabs all the reviewers and the number of reviews to the repo
        returns {'reviewer_name': int no_of_reviews}
    """
    request_url = 'https://api.github.com/repos/denamwangi/skills_flask/pulls?state=all'
    response = json.loads(requests.get(request_url).content)

    repo_reviewers = {}
    for each_pr in response:
        # grab the pr id, pass that to the reviews function, which asks 
        # for all the reviews for that pr and grabs all the authors of the reviews
        # import ipdb; ipdb.set_trace()
        id = each_pr.get('number')
        reviewers = get_pr_reviews(id)
        for reviewer in reviewers:
            repo_reviewers[reviewer] = repo_reviewers.get(reviewer, 0) + 1

    return repo_reviewers

def get_pr_reviews(id):
    """ Grabs all the reviews for this pr. Returns a set of all reviewers
    """

    request_url = 'https://api.github.com/repos/denamwangi/skills_flask/pulls/{}/reviews'.format(id)

    response = json.loads(requests.get(request_url).content)
    pr_reviewers = set()
    for each_review in response:
        reviewer = each_review['user']['login']
        pr_reviewers.add(reviewer)
    return pr_reviewers