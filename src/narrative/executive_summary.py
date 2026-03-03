"""Generate executive-level conclusions from technical output."""

from src.parsers.pipeline_output import PipelineSummary


def build_executive_summary(summary: PipelineSummary) -> str:
    risk = "elevated" if summary.pathogen_hits > 0 else "low"
    return (
        f"Sample {summary.sample_id}: total reads {summary.reads_total}. "
        f"Pathogen signal: {summary.pathogen_hits} hits. "
        f"Operational risk assessment: {risk}."
    )


def build_portfolio_summary(summaries: list[PipelineSummary]) -> str:
    if not summaries:
        return "No samples processed. Portfolio risk: unknown."

    total_samples = len(summaries)
    total_reads = sum(item.reads_total for item in summaries)
    total_hits = sum(item.pathogen_hits for item in summaries)
    highest = max(summaries, key=lambda item: item.pathogen_hits)
    risk = "elevated" if total_hits > 0 else "low"

    return (
        f"Portfolio summary: {total_samples} samples, {total_reads} total reads, "
        f"{total_hits} pathogen hits. Highest-signal sample: {highest.sample_id} "
        f"({highest.pathogen_hits} hits). Aggregate risk: {risk}."
    )
