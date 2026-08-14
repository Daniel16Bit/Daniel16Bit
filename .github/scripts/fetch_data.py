#!/usr/bin/env python3
"""
Mescla projects.json (curado por voce) com dados ao vivo do GitHub.
Roda dentro da Action com GITHUB_TOKEN. Produz merged.json para o gerador.

Voce controla: name, repo, logo, description, tags, ordem (ordem do array).
Auto-buscado:  stars, languages (para o donut), pushed_at.
Se a API falhar para um repo, o card ainda renderiza so com a config.
"""
import json, os, sys, urllib.request

TOKEN = os.environ.get("GITHUB_TOKEN", "")


def gh(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}" if TOKEN else "",
        "User-Agent": "projects-panel",
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def main():
    with open("projects.json") as f:
        projects = json.load(f)
    for p in projects:
        repo = p.get("repo", "").strip()
        repo = repo.replace("https://github.com/", "").replace("http://github.com/", "").rstrip("/")
        p["repo"] = repo
        try:
            info = gh(f"https://api.github.com/repos/{repo}")
            p["stars"] = info.get("stargazers_count", 0)
            p["pushed_at"] = info.get("pushed_at")
            if not p.get("description"):
                p["description"] = info.get("description") or ""
            p["languages"] = gh(f"https://api.github.com/repos/{repo}/languages")
        except Exception as e:
            print(f"warn: could not fetch {repo}: {e}", file=sys.stderr)
            p.setdefault("stars", 0)
            p.setdefault("languages", {})
            p.setdefault("pushed_at", None)
    with open("merged.json", "w") as f:
        json.dump(projects, f)
    print(f"merged {len(projects)} projects")


if __name__ == "__main__":
    main()
