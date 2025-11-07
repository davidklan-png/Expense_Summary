"""HTML report generation using Jinja2 templates."""
from pathlib import Path
from typing import Dict, Any, List

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_unique_attendees(
    transactions: pd.DataFrame,
    attendee_reference: pd.DataFrame
) -> pd.DataFrame:
    """
    Extract unique attendee IDs from transactions and join with reference data.

    Args:
        transactions: DataFrame with ID1-ID8 columns
        attendee_reference: DataFrame with attendee details (ID, Name, Title, Company)

    Returns:
        DataFrame with unique attendees sorted by ID numerically
    """
    # Collect all ID values from ID1-ID8 columns
    id_columns = [f'ID{i}' for i in range(1, 9)]

    # Ensure columns exist
    existing_id_cols = [col for col in id_columns if col in transactions.columns]

    if not existing_id_cols:
        return pd.DataFrame(columns=['ID', 'Name', 'Title', 'Company'])

    # Stack all ID columns into a single series
    all_ids = pd.concat([transactions[col] for col in existing_id_cols], ignore_index=True)

    # Filter out empty strings and get unique values
    unique_ids = all_ids[all_ids != ''].unique()

    if len(unique_ids) == 0:
        return pd.DataFrame(columns=['ID', 'Name', 'Title', 'Company'])

    # Create DataFrame of unique IDs
    unique_df = pd.DataFrame({'ID': unique_ids})

    # Ensure ID column is string type in reference
    attendee_ref_copy = attendee_reference.copy()
    attendee_ref_copy['ID'] = attendee_ref_copy['ID'].astype(str)

    # Join with reference data
    result = unique_df.merge(
        attendee_ref_copy[['ID', 'Name', 'Title', 'Company']],
        on='ID',
        how='left'
    )

    # Sort by ID numerically
    result['_sort_key'] = result['ID'].apply(lambda x: int(x) if x.isdigit() else float('inf'))
    result = result.sort_values('_sort_key').drop('_sort_key', axis=1)

    return result.reset_index(drop=True)


def prepare_report_context(
    transactions: pd.DataFrame,
    attendee_reference: pd.DataFrame,
    filename: str
) -> Dict[str, Any]:
    """
    Prepare context dictionary for template rendering.

    Args:
        transactions: Processed transaction DataFrame
        attendee_reference: Attendee reference DataFrame
        filename: Source filename for the report

    Returns:
        Dictionary with template context variables
    """
    # Get unique attendees
    unique_attendees = get_unique_attendees(transactions, attendee_reference)

    # Calculate metadata
    total_transactions = len(transactions)
    total_amount = transactions['利用金額'].sum() if '利用金額' in transactions.columns else 0

    # Convert DataFrames to list of dicts for template
    transactions_list = transactions.to_dict('records')
    attendees_list = unique_attendees.to_dict('records')

    return {
        'filename': filename,
        'transactions': transactions_list,
        'unique_attendees': attendees_list,
        'total_transactions': total_transactions,
        'total_amount': int(total_amount),
    }


def generate_html_report(
    transactions: pd.DataFrame,
    attendee_reference: pd.DataFrame,
    output_path: Path,
    source_filename: str,
    template_dir: Path = None,
    handle_duplicates: bool = False
) -> Path:
    """
    Generate HTML report from transaction data.

    Args:
        transactions: Processed transaction DataFrame
        attendee_reference: Attendee reference DataFrame
        output_path: Path where HTML should be written
        source_filename: Original source CSV filename
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
        # Default to project's templates directory
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        template_dir = project_root / 'templates'

    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(['html', 'xml'])
    )

    # Load template
    template = env.get_template('report.html.j2')

    # Prepare context
    context = prepare_report_context(transactions, attendee_reference, source_filename)

    # Render template
    html_content = template.render(**context)

    # Write to file
    output_path.write_text(html_content, encoding='utf-8')

    return output_path
