from src.narrative.executive_summary import build_executive_summary
from src.parsers.pipeline_output import parse_summary_line


def test_parse_summary_line() -> None:
    summary = parse_summary_line("S01, 1520000, 3")
    assert summary.sample_id == "S01"
    assert summary.reads_total == 1520000
    assert summary.pathogen_hits == 3


def test_executive_summary_elevated_risk() -> None:
    summary = parse_summary_line("S01, 1520000, 3")
    text = build_executive_summary(summary)
    assert "elevated" in text
