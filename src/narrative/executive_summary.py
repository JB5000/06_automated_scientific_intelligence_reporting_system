"""Generate executive-level conclusions from technical output."""

from src.parsers.pipeline_output import PipelineSummary


def build_executive_summary(summary: PipelineSummary) -> str:
    risk = "elevated" if summary.pathogen_hits > 0 else "low"
    return (
        f"Sample {summary.sample_id}: total reads {summary.reads_total}. "
        f"Pathogen signal: {summary.pathogen_hits} hits. "
        f"Operational risk assessment: {risk}."
    )
