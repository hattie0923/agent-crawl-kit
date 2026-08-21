from __future__ import annotations

import argparse

from agent_crawl.channels.github import inspect_repo
from agent_crawl.channels.rss import read_feed
from agent_crawl.channels.search import search_web
from agent_crawl.channels.video import inspect_video
from agent_crawl.channels.web import read_url
from agent_crawl.doctor import run_checks
from agent_crawl.extract.article import extract_article
from agent_crawl.extract.table import extract_tables
from agent_crawl.output import emit


FORMATS = ("json", "jsonl", "csv", "markdown")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent-crawl")
    parser.add_argument("--version", action="version", version="agent-crawl 0.1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subparsers.add_parser("doctor", help="Check available crawl channels")
    _add_format(doctor_parser, default="markdown")

    read_parser = subparsers.add_parser("read-url", help="Read a URL")
    read_parser.add_argument("url")
    _add_format(read_parser)

    search_parser = subparsers.add_parser("search", help="Search through configured local search tooling")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=5)
    _add_format(search_parser)

    rss_parser = subparsers.add_parser("rss", help="Read an RSS or Atom feed")
    rss_parser.add_argument("url")
    rss_parser.add_argument("--limit", type=int, default=20)
    _add_format(rss_parser, default="jsonl")

    github_parser = subparsers.add_parser("github", help="Inspect a GitHub repository")
    github_parser.add_argument("repo", help="Repository in owner/name form")
    _add_format(github_parser)

    video_parser = subparsers.add_parser("video", help="Inspect video metadata")
    video_parser.add_argument("url")
    _add_format(video_parser)

    extract_parser = subparsers.add_parser("extract", help="Extract structured data")
    extract_subparsers = extract_parser.add_subparsers(dest="extractor", required=True)

    article_parser = extract_subparsers.add_parser("article", help="Extract article fields")
    article_parser.add_argument("url")
    _add_format(article_parser)

    table_parser = extract_subparsers.add_parser("table", help="Extract HTML tables")
    table_parser.add_argument("url")
    _add_format(table_parser, default="json")

    args = parser.parse_args(argv)
    payload = _dispatch(args)
    emit(payload, args.format)
    return 0


def _add_format(parser: argparse.ArgumentParser, default: str = "json") -> None:
    parser.add_argument("--format", choices=FORMATS, default=default)


def _dispatch(args: argparse.Namespace) -> object:
    if args.command == "doctor":
        return [check.to_dict() for check in run_checks()]
    if args.command == "read-url":
        return read_url(args.url)
    if args.command == "search":
        return search_web(args.query, args.limit)
    if args.command == "rss":
        return read_feed(args.url, args.limit)
    if args.command == "github":
        return inspect_repo(args.repo)
    if args.command == "video":
        return inspect_video(args.url)
    if args.command == "extract" and args.extractor == "article":
        return extract_article(args.url)
    if args.command == "extract" and args.extractor == "table":
        return extract_tables(args.url)
    raise SystemExit(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
