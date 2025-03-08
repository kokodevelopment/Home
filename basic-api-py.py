from flask import Flask, jsonify
import requests
import json
from flask_caching import Cache
from datetime import datetime
from typing import List

app = Flask(__name__)

# Initialize Flask-Caching with a simple in-memory cache
cache_config = {
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300  # Cache timeout in seconds
}
cache = Cache(app, config=cache_config)

@app.route('/updates')
def updates():
    send = {
        "ID": "1232133",
        "GuildID": "XXXXXXX",
        "ChannelID": "XXXXXXX",
        "CreatedTs": 3333333,
        "EditedTs": 3333333,
        "authorID": "XXXXXXX",
        "authorName": "kokofixcomputers",
        "authorImage": "https://cdn.discordapp.com/avatars/1096839213313446019/b614a5ea08657b33de938e0152c6c0ce?size=1024",
        "content": "This is a test",
        "cleanContent": "This is a test",
        "image": "https://cdn.discordapp.com/avatars/1096839213313446019/b614a5ea08657b33de938e0152c6c0ce?size=1024",
    }
    return jsonify(send)


class GHAuthor:
    def __init__(self, login: str, avatar_url: str, html_url: str):
        self.login = login
        self.avatar_url = avatar_url
        self.html_url = html_url

class GHCommitAuthor:
    def __init__(self, name: str, email: str, date: str):
        self.name = name
        self.email = email
        self.date = date

class GHCommit:
    def __init__(self, author: GHCommitAuthor, message: str):
        self.author = author
        self.message = message

class GHApiCommit:
    def __init__(self, author: GHAuthor, commit: GHCommit, html_url: str):
        self.author = author
        self.commit = commit
        self.html_url = html_url

    def to_dict(self):
        return {
            "author": {
                "login": self.author.login,
                "avatar_url": self.author.avatar_url,
                "html_url": self.author.html_url
            },
            "commit": {
                "author": {
                    "name": self.commit.author.name,
                    "email": self.commit.author.email,
                    "date": self.commit.author.date
                },
                "message": self.commit.message
            },
            "html_url": self.html_url
        }

recent_commits = []

def get_recent_commits():
    github_commit_apis = [
        "https://api.github.com/repos/kokodevelopment/kokodevelopment.github.io/commits?per_page=50",
		"https://api.github.com/repos/kokodevelopment/PenguinMod-Vm/commits?per_page=50",
		"https://api.github.com/repos/kokodevelopment/Home/commits?per_page=50",
		"https://api.github.com/repos/PenguinMod/PenguinMod-Blocks/commits?per_page=50",
		"https://api.github.com/repos/PenguinMod/PenguinMod-Paint/commits?per_page=50",
		"https://api.github.com/repos/kokodevelopment/PenguinMod-Packager/commits?per_page=50",
		"https://api.github.com/repos/kokodevelopment/OrangeMod-Render/commits?per_page=50",
		"https://api.github.com/repos/PenguinMod/PenguinMod-ExtensionsGallery/commits?per_page=50",
		"https://api.github.com/repos/kokodevelopment/Backend-Api/commits?per_page=50",
    ]

    new_recent_commits = []
    for api in github_commit_apis:
        try:
            response = requests.get(api)
            if response.status_code != 200:
                print(f"Failed fetching {api}: Non-OK status code; {response.status_code}")
                continue

            api_response = response.json()
            for commit in api_response:
                author = GHAuthor(commit['author']['login'], commit['author']['avatar_url'], commit['author']['html_url'])
                commit_author = GHCommitAuthor(commit['commit']['author']['name'], commit['commit']['author']['email'], commit['commit']['author']['date'])
                commit_obj = GHCommit(commit_author, commit['commit']['message'])
                gh_api_commit = GHApiCommit(author, commit_obj, commit['html_url'])
                new_recent_commits.append(gh_api_commit)

        except Exception as e:
            print(f"Failed fetching {api}: {e}")

    # Sort commits by date
    new_recent_commits.sort(key=lambda x: datetime.strptime(x.commit.author.date, '%Y-%m-%dT%H:%M:%SZ'), reverse=True)

    global recent_commits
    if len(new_recent_commits) >= 200:
        recent_commits = new_recent_commits[:200]
    else:
        recent_commits = new_recent_commits

commits_cache = []
cache_use = 0

@app.route('/status')
def status():
    return jsonify({"type": "warn", "text": "Python Basic API is used."})

@app.route('/commits')
@cache.cached(timeout=600)  # Cache this view for 5 minutes
def commits():
    urls = [
        "https://api.github.com/repos/kokodevelopment/kokodevelopment.github.io/commits?per_page=50",
		"https://api.github.com/repos/kokodevelopment/PenguinMod-Vm/commits?per_page=50",
		"https://api.github.com/repos/kokodevelopment/Home/commits?per_page=50",
		"https://api.github.com/repos/PenguinMod/PenguinMod-Blocks/commits?per_page=50",
		"https://api.github.com/repos/PenguinMod/PenguinMod-Paint/commits?per_page=50",
		"https://api.github.com/repos/kokodevelopment/PenguinMod-Packager/commits?per_page=50",
		"https://api.github.com/repos/kokodevelopment/OrangeMod-Render/commits?per_page=50",
		"https://api.github.com/repos/PenguinMod/PenguinMod-ExtensionsGallery/commits?per_page=50",
		"https://api.github.com/repos/kokodevelopment/Backend-Api/commits?per_page=50",
    ]
    get_recent_commits()
    return jsonify([commit.to_dict() for commit in recent_commits])

app.run(host='0.0.0.0', port=23235)