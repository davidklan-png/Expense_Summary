"""HTML and PDF report generation using Jinja2 templates and WeasyPrint."""

from io import BytesIO
from pathlib import Path
from typing import Any, Optional

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

PDF_SYSTEM_DEPENDENCY_ERROR_MARKERS = (
    "cannot load library",
    "ctypes.util.find_library",
    "libcairo",
    "libgobject",
    "libpango",
    "gobject-2.0",
    "pango-1.0",
)


def _numeric_sort_key(id_value: str) -> int | float:
    """Convert ID to numeric sort key, placing non-numeric IDs at end.

    Args:
        id_value: ID string value

    Returns:
        Integer value for numeric IDs, infinity for non-numeric
    """
    return int(id_value) if id_value.isdigit() else float("inf")


def _is_pdf_system_dependency_error(error: BaseException) -> bool:
    """Return True when PDF generation failed because native libraries are missing."""
    error_text = str(error).lower()
    return any(marker in error_text for marker in PDF_SYSTEM_DEPENDENCY_ERROR_MARKERS)


def get_unique_attendees(transactions: pd.DataFrame, attendee_reference: pd.DataFrame) -> pd.DataFrame:
    """
    Extract unique attendee IDs from transactions and join with reference data.

    Args:
        transactions: DataFrame with ID1-ID8 columns
        attendee_reference: DataFrame with attendee details (ID, Name, Title, Company)

    Returns:
        DataFrame with unique attendees sorted by ID numerically
    """
    # Collect all ID values from ID1-ID8 columns
    id_columns = [f"ID{i}" for i in range(1, 9)]

    # Ensure columns exist
    existing_id_cols = [col for col in id_columns if col in transactions.columns]

    if not existing_id_cols:
        return pd.DataFrame(columns=["ID", "Name", "Title", "Company"])

    # Stack all ID columns into a single series
    all_ids = pd.concat([transactions[col] for col in existing_id_cols], ignore_index=True)

    # Filter out empty strings, NaN values, and ensure string type
    # Convert to string first to handle any numeric or NaN values
    all_ids = all_ids.astype(str)
    unique_ids = all_ids[(all_ids != "") & (all_ids != "nan")].unique()

    if len(unique_ids) == 0:
        return pd.DataFrame(columns=["ID", "Name", "Title", "Company"])

    # Create DataFrame of unique IDs
    unique_df = pd.DataFrame({"ID": unique_ids})

    # Ensure ID column is string type in reference
    attendee_ref_copy = attendee_reference.copy()
    attendee_ref_copy["ID"] = attendee_ref_copy["ID"].astype(str)

    # Join with reference data (explicitly exclude Core column from output)
    reference_columns = ["ID", "Name", "Title", "Company"]
    if "Core" in attendee_ref_copy.columns:
        # Core column is used for selection logic but not included in output
        attendee_ref_copy = attendee_ref_copy.drop(columns=["Core"])
    result = unique_df.merge(attendee_ref_copy[reference_columns], on="ID", how="left")

    # Sort by ID numerically
    result["_sort_key"] = result["ID"].apply(_numeric_sort_key)
    result = result.sort_values("_sort_key").drop("_sort_key", axis=1)

    return result.reset_index(drop=True)


def prepare_report_context(
    transactions: pd.DataFrame,
    attendee_reference: pd.DataFrame,
    filename: str,
    pre_header_rows: list[str],
) -> dict[str, Any]:
    """
    Prepare context dictionary for template rendering.

    Args:
        transactions: Processed transaction DataFrame
        attendee_reference: Attendee reference DataFrame
        filename: Source filename for the report
        pre_header_rows: Raw pre-header lines from CSV

    Returns:
        Dictionary with template context variables
    """
    # Get unique attendees
    unique_attendees = get_unique_attendees(transactions, attendee_reference)

    # Convert Int64 columns to object type to allow fillna with empty string
    transactions_copy = transactions.copy()
    # Use select_dtypes for efficient column selection
    int64_cols = transactions_copy.select_dtypes(include=["Int64", "Int32", "Int16", "Int8"]).columns
    for col in int64_cols:
        # Direct conversion to object (avoid intermediate float)
        transactions_copy[col] = transactions_copy[col].astype(object)

    # Replace NaN values with empty string before converting to dict
    # This prevents Jinja2 from rendering them as "nan"
    transactions_clean = transactions_copy.fillna("")
    attendees_clean = unique_attendees.fillna("")

    # Convert DataFrames to list of dicts for template
    transactions_list = transactions_clean.to_dict("records")
    attendees_list = attendees_clean.to_dict("records")

    # Get column names from DataFrame (preserves order)
    column_names = transactions.columns.tolist()

    return {
        "filename": filename,
        "transactions": transactions_list,
        "unique_attendees": attendees_list,
        "column_names": column_names,
        "pre_header_rows": pre_header_rows,
    }


def generate_html_report(
    transactions: pd.DataFrame,
    attendee_reference: pd.DataFrame,
    output_path: Path,
    source_filename: str,
    pre_header_rows: list[str] = None,
    template_dir: Optional[Path] = None,
    handle_duplicates: bool = False,
) -> Path:
    """
    Generate HTML report from transaction data.

    Args:
        transactions: Processed transaction DataFrame
        attendee_reference: Attendee reference DataFrame
        output_path: Path where HTML should be written
        source_filename: Original source CSV filename
        pre_header_rows: Raw pre-header lines from CSV (optional)
        template_dir: Directory containing Jinja2 templates (default: project templates/)
        handle_duplicates: If True, append numeric suffix for existing files

    Returns:
        Actual path where HTML was written
    """
    output_path = Path(output_path)

    # Handle duplicate filenames
    if handle_duplicates and output_path.exists():
        counter = 2
        while True:
            new_path = output_path.parent / f"{output_path.stem}_{counter}{output_path.suffix}"
            if not new_path.exists():
                output_path = new_path
                break
            counter += 1

    # Determine template directory
    if template_dir is None:
        # Default to package's templates directory
        current_file = Path(__file__)
        template_dir = current_file.parent / "templates"

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=select_autoescape(["html", "xml"]))

    # Load template
    template = env.get_template("report.html.j2")

    # Prepare context
    context = prepare_report_context(transactions, attendee_reference, source_filename, pre_header_rows or [])

    # Render template
    html_content = template.render(**context)

    # Write to file
    output_path.write_text(html_content, encoding="utf-8")

    return output_path


def generate_pdf_bytes(
    transactions: pd.DataFrame,
    attendee_reference: pd.DataFrame,
    source_filename: str,
    pre_header_rows: list[str] = None,
    template_dir: Optional[Path] = None,
) -> tuple[BytesIO, str]:
    """
    Generate PDF report from transaction data as bytes for download.

    Args:
        transactions: Processed transaction DataFrame
        attendee_reference: Attendee reference DataFrame
        source_filename: Original source CSV filename
        pre_header_rows: Raw pre-header lines from CSV (optional)
        template_dir: Directory containing Jinja2 templates (default: package templates/)

    Returns:
        Tuple of (BytesIO object containing PDF data, file extension)
        Falls back to HTML if PDF generation fails due to missing system libraries.
    """
    # Determine template directory
    if template_dir is None:
        current_file = Path(__file__)
        template_dir = current_file.parent / "templates"

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=select_autoescape(["html", "xml"]))

    # Load template
    template = env.get_template("report.html.j2")

    # Prepare context
    context = prepare_report_context(transactions, attendee_reference, source_filename, pre_header_rows or [])

    # Render template to HTML
    html_content = template.render(**context)

    # Try to import WeasyPrint and generate PDF
    try:
        from weasyprint import HTML

        # Convert HTML to PDF bytes
        pdf_bytes = HTML(string=html_content, base_url=str(template_dir)).write_pdf()
        return BytesIO(pdf_bytes), ".pdf"
    except (ImportError, OSError) as e:
        # System libraries not available - fall back to HTML
        if _is_pdf_system_dependency_error(e):
            # Return HTML with instructions for browser print-to-PDF
            html_with_print = html_content + """
<script>
window.onload = function() {
    if (confirm('PDF generation requires system libraries. Would you like to open the print dialog to save as PDF?')) {
        window.print();
    }
};
</script>
<style>
@media print {
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
</style>
"""
            return BytesIO(html_with_print.encode("utf-8")), ".html"
        raise
    except Exception:
        raise


def generate_html_bytes(
    transactions: pd.DataFrame,
    attendee_reference: pd.DataFrame,
    source_filename: str,
    pre_header_rows: list[str] = None,
    template_dir: Optional[Path] = None,
) -> BytesIO:
    """
    Generate HTML report as bytes for download (fallback option).

    Args:
        transactions: Processed transaction DataFrame
        attendee_reference: Attendee reference DataFrame
        source_filename: Original source CSV filename
        pre_header_rows: Raw pre-header lines from CSV (optional)
        template_dir: Directory containing Jinja2 templates (default: package templates/)

    Returns:
        BytesIO object containing HTML data
    """
    # Determine template directory
    if template_dir is None:
        current_file = Path(__file__)
        template_dir = current_file.parent / "templates"

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=select_autoescape(["html", "xml"]))

    # Load template
    template = env.get_template("report.html.j2")

    # Prepare context
    context = prepare_report_context(transactions, attendee_reference, source_filename, pre_header_rows or [])

    # Render template to HTML
    html_content = template.render(**context)

    # Add print instruction message
    html_with_message = html_content.replace(
        "</body>",
        """
<div style="position: fixed; top: 10px; right: 10px; background: #ffeb3b; padding: 10px; border-radius: 4px; z-index: 1000;">
    <strong>Tip:</strong> Use Ctrl+P to save as PDF
</div>
</body>
""",
    )

    return BytesIO(html_with_message.encode("utf-8"))
