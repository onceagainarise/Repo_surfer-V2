import argparse
from reposurfer.app.reposurfer_app import RepoSurferApp

def main():
    parser = argparse.ArgumentParser("RepoSurfer")
    sub = parser.add_subparsers(dest="command")

    index = sub.add_parser("index")
    index.add_argument("repo_url")

    query = sub.add_parser("query")
    query.add_argument("repo_path")
    query.add_argument("issue")

    args = parser.parse_args()
    app = RepoSurferApp()

    if args.command == "index":
        app.index_repo(args.repo_url)

    elif args.command == "query":
        app.query(args.repo_path, args.issue)

if __name__ == "__main__":
    main()
