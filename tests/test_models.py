from agent_crawl.models import ok


def test_ok_result_has_provenance() -> None:
    result = ok("https://example.com", {"title": "Example"})

    payload = result.to_dict()

    assert payload["status"] == "ok"
    assert payload["source_url"] == "https://example.com"
    assert payload["retrieved_at"]
    assert payload["data"]["title"] == "Example"

