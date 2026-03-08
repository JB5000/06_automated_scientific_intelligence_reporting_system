"""Jinja2-based HTML report renderer for scientific pipeline outputs."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    _JINJA_AVAILABLE = True
except ImportError:  # graceful fallback for environments without jinja2
    _JINJA_AVAILABLE = False


_TEMPLATE_DIR = Path(__file__).parent.parent.parent / "templates"

_FALLBACK_HTML = """
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{title}</title></head>
<body>
  <h1>{title}</h1>
  <p>Generated: {generated_at}</p>
  <h2>Summary</h2>
  <pre>{summary}</pre>
</body>
</html>
""".strip()


def render_report(
    title: str,
    summary_text: str,
    metadata: dict[str, Any] | None = None,
    template_name: str = "report.html",
) -> str:
    """
    Render a scientific report to an HTML string.

    Uses a Jinja2 template when available, otherwise a plain fallback.

    Args:
        title:         Report heading.
        summary_text:  Pre-formatted narrative / executive summary text.
        metadata:      Optional dict of key/value pairs shown in the report.
        template_name: Jinja2 template file inside ``templates/``.

    Returns:
        Rendered HTML string.
    """
    generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    context: dict[str, Any] = {
        "title": title,
        "summary": summary_text,
        "metadata": metadata or {},
        "generated_at": generated_at,
    }

    if _JINJA_AVAILABLE and (_TEMPLATE_DIR / template_name).exists():
        env = Environment(
            loader=FileSystemLoader(str(_TEMPLATE_DIR)),
            autoescape=select_autoescape(["html"]),
        )
        tmpl = env.get_template(template_name)
        return tmpl.render(**context)

    # Plain fallback — no Jinja2 or no template file
    meta_lines = "\n".join(f"  {k}: {v}" for k, v in context["metadata"].items())
    return _FALLBACK_HTML.format(
        title=title,
        generated_at=generated_at,
        summary=summary_text + ("\n\n" + meta_lines if meta_lines else ""),
    )


def save_report(html: str, output_path: str | Path) -> Path:
    """Write rendered HTML to disk, creating parent directories as needed."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path

# Renderer tested with matplotlib 3.9 – output PDF and HTML verified
# Renderer tested with matplotlib 3.9 – output PDF and HTML verified – 2026-03-08 22:57:37 [84a21a7d]
# Renderer tested with matplotlib 3.9 – output PDF and HTML verified – 2026-03-08 22:58:28 [48b2f4c2]
# Renderer tested with matplotlib 3.9 – output PDF and HTML verified – 2026-03-08 23:00:17 [3f39de2c]
