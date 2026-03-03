from src.narrative.executive_summary import build_executive_summary, build_portfolio_summary
from src.parsers.pipeline_output import parse_summary_line, parse_summary_lines
import pytest


def test_parse_summary_line() -> None:
    summary = parse_summary_line("S01, 1520000, 3")
    assert summary.sample_id == "S01"
    assert summary.reads_total == 1520000
    assert summary.pathogen_hits == 3


def test_executive_summary_elevated_risk() -> None:
    summary = parse_summary_line("S01, 1520000, 3")
    text = build_executive_summary(summary)
    assert "elevated" in text


def test_parse_summary_lines_ignores_comments_and_blanks() -> None:
    data = """
    # sample_id,reads_total,pathogen_hits
    S01, 1520000, 3

    S02, 830000, 0
    """
    summaries = parse_summary_lines(data)
    assert len(summaries) == 2
    assert summaries[1].sample_id == "S02"


def test_parse_summary_lines_reports_invalid_line() -> None:
    with pytest.raises(ValueError):
        parse_summary_lines("S01,broken_line")


def test_build_portfolio_summary() -> None:
    summaries = parse_summary_lines("S01, 1000, 1\nS02, 2000, 0")
    text = build_portfolio_summary(summaries)
    assert "2 samples" in text
    assert "3000 total reads" in text
    assert "S01" in text


def test_build_portfolio_summary_empty() -> None:
    text = build_portfolio_summary([])
    assert "No samples processed" in text
