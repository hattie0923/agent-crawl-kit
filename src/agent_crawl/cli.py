from __future__ import annotations

import argparse

from agent_crawl.channels.github import inspect_repo
from agent_crawl.channels.openrouter import list_models
from agent_crawl.channels.platforms import search_platform
from agent_crawl.channels.rss import read_feed
from agent_crawl.channels.search import search_web
from agent_crawl.channels.video import inspect_video
from agent_crawl.channels.web import read_url
from agent_crawl import __version__
from agent_crawl.config import list_entries, read_env_secret, read_file_secret, read_stdin_secret, write_secret
from agent_crawl.doctor import run_checks
from agent_crawl.extract.article import extract_article
from agent_crawl.extract.table import extract_tables
from agent_crawl.output import emit


FORMATS = ("json", "jsonl", "csv", "markdown")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent-crawl")
    parser.add_argument("--version", action="version", version=f"agent-crawl {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subparsers.add_parser("doctor", help="Check available crawl channels")
    _add_format(doctor_parser, default="markdown")

    configure_parser = subparsers.add_parser("configure", help="Configure local credentials or cookies")
    configure_subparsers = configure_parser.add_subparsers(dest="config_command", required=True)

    cookie_parser = configure_subparsers.add_parser("cookie", help="Store a platform cookie locally")
    cookie_parser.add_argument("platform", help="Platform name, for example twitter, reddit, xiaohongshu, facebook, instagram")
    _add_secret_sources(cookie_parser)
    _add_format(cookie_parser)

    token_parser = configure_subparsers.add_parser("token", help="Store a service token locally")
    token_parser.add_argument("service", help="Service name, for example openrouter")
    _add_secret_sources(token_parser)
    _add_format(token_parser)

    openrouter_parser = configure_subparsers.add_parser("openrouter", help="Store an OpenRouter API key locally")
    _add_secret_sources(openrouter_parser)
    _add_format(openrouter_parser)

    list_parser = configure_subparsers.add_parser("list", help="List local configuration entries without secret values")
    _add_format(list_parser, default="markdown")

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

    openrouter_parser = subparsers.add_parser("openrouter", help="Inspect OpenRouter availability")
    openrouter_subparsers = openrouter_parser.add_subparsers(dest="openrouter_command", required=True)
    models_parser = openrouter_subparsers.add_parser("models", help="List OpenRouter models")
    models_parser.add_argument("--limit", type=int, default=20)
    _add_format(models_parser)

    platform_parser = subparsers.add_parser("platform", help="Use configured platform backends")
    platform_subparsers = platform_parser.add_subparsers(dest="platform_command", required=True)
    platform_search_parser = platform_subparsers.add_parser("search", help="Search a configured platform backend")
    platform_search_parser.add_argument("platform", help="bilibili, twitter, x, reddit, xiaohongshu, xhs, facebook, instagram, linkedin")
    platform_search_parser.add_argument("query")
    platform_search_parser.add_argument("--limit", type=int, default=10)
    _add_format(platform_search_parser)

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


def _add_secret_sources(parser: argparse.ArgumentParser) -> None:
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--from-stdin", action="store_true", help="Read the secret value from stdin")
    source.add_argument("--from-file", help="Read the secret value from a local file")
    source.add_argument("--from-env", help="Read the secret value from an environment variable")


def _dispatch(args: argparse.Namespace) -> object:
    if args.command == "doctor":
        return [check.to_dict() for check in run_checks()]
    if args.command == "configure":
        return _dispatch_configure(args)
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
    if args.command == "openrouter" and args.openrouter_command == "models":
        return list_models(args.limit)
    if args.command == "platform" and args.platform_command == "search":
        return search_platform(args.platform, args.query, args.limit)
    if args.command == "extract" and args.extractor == "article":
        return extract_article(args.url)
    if args.command == "extract" and args.extractor == "table":
        return extract_tables(args.url)
    raise SystemExit(f"unsupported command: {args.command}")


def _dispatch_configure(args: argparse.Namespace) -> object:
    if args.config_command == "list":
        return [entry.to_dict() for entry in list_entries()]

    if args.from_stdin:
        value = read_stdin_secret()
    elif args.from_file:
        value = read_file_secret(args.from_file)
    elif args.from_env:
        value = read_env_secret(args.from_env)
    else:
        raise SystemExit("missing secret source")

    if args.config_command == "cookie":
        entry = write_secret("cookie", args.platform, value)
    elif args.config_command == "token":
        entry = write_secret("token", args.service, value)
    elif args.config_command == "openrouter":
        entry = write_secret("token", "openrouter", value)
    else:
        raise SystemExit(f"unsupported configure command: {args.config_command}")

    payload = entry.to_dict()
    payload["value"] = "<stored>"
    return payload


if __name__ == "__main__":
    raise SystemExit(main())
