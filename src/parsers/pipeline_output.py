"""Parser utilities for standardized pipeline summaries."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineSummary:
    sample_id: str
    reads_total: int
    pathogen_hits: int


def parse_summary_line(line: str) -> PipelineSummary:
    sample_id, reads_total, pathogen_hits = [part.strip() for part in line.split(",")]
    return PipelineSummary(
        sample_id=sample_id,
        reads_total=int(reads_total),
        pathogen_hits=int(pathogen_hits),
    )
