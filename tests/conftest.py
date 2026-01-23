"""Shared pytest fixtures for Saison Transform tests."""
import pandas as pd
import pytest
from pathlib import Path


@pytest.fixture
def sample_attendee_ref():
    """Standard attendee reference DataFrame for testing."""
    return pd.DataFrame({
        "ID": ["1", "2", "3", "4", "5", "6", "7", "8"],
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Henry"],
        "Title": ["Manager", "Lead", "Developer", "Analyst", "Designer", "QA", "PM", "Director"],
        "Company": ["Corp A", "Corp B", "Corp C", "Corp D", "Corp E", "Corp F", "Corp G", "Corp H"]
    })


@pytest.fixture
def sample_attendee_ref_japanese():
    """Japanese attendee reference DataFrame for testing."""
    return pd.DataFrame({
        "ID": ["1", "2", "3"],
        "Name": ["山田太郎", "佐藤花子", "鈴木一郎"],
        "Title": ["部長", "課長", "主任"],
        "Company": ["ABC株式会社", "XYZ株式会社", "DEF株式会社"]
    })


@pytest.fixture
def sample_config_dict():
    """Standard configuration dictionary for testing."""
    return {
        "min_attendees": 2,
        "max_attendees": 8,
        "primary_id_weights": {"2": 0.9, "1": 0.1},
        "input_dir": "data/input",
        "reference_dir": "data/reference",
        "output_dir": "data/output",
        "archive_dir": "data/archive",
    }


@pytest.fixture
def sample_transaction_df():
    """Sample transaction DataFrame for testing."""
    return pd.DataFrame({
        "利用日": ["2025-01-10", "2025-01-15", "2025-01-20"],
        "ご利用店名及び商品名": ["Restaurant A", "Cafe B", "Hotel C"],
        "利用金額": [15000, 8000, 25000],
        "科目＆No.": ["会議費", "接待費", "会議費"]
    })


@pytest.fixture
def sample_csv_with_header():
    """Sample CSV content with proper headers."""
    return """利用日,ご利用店名及び商品名,利用金額,科目＆No.
2025-01-10,Restaurant A,15000,会議費
2025-01-15,Cafe B,8000,接待費
"""


@pytest.fixture
def sample_csv_with_pre_header():
    """Sample CSV content with pre-header rows."""
    return """カード会員氏名：山田太郎
締日：2025年1月分
利用日,ご利用店名及び商品名,利用金額,科目＆No.
2025-01-10,Restaurant A,15000,会議費
"""


@pytest.fixture
def tmp_dir_with_files(tmp_path):
    """Create temporary directory structure with sample files."""
    # Create directory structure
    input_dir = tmp_path / "data" / "input"
    reference_dir = tmp_path / "data" / "reference"
    output_dir = tmp_path / "data" / "output"
    archive_dir = tmp_path / "data" / "archive"

    for dir_path in [input_dir, reference_dir, output_dir, archive_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Create sample reference file
    ref_file = reference_dir / "NameList.csv"
    ref_file.write_text(
        "ID,Name,Title,Company\n"
        "1,Test User,Manager,Test Corp\n"
        "2,Another User,Lead,Another Corp\n",
        encoding="utf-8"
    )

    # Create sample config file
    config_file = reference_dir / "config.toml"
    config_file.write_text(
        "[paths]\n"
        'input_dir = "data/input"\n'
        'reference_dir = "data/reference"\n'
        'output_dir = "data/output"\n'
        'archive_dir = "data/archive"\n\n'
        "[processing]\n"
        "min_attendees = 2\n"
        "max_attendees = 8\n"
    )

    return {
        "tmp_path": tmp_path,
        "input_dir": input_dir,
        "reference_dir": reference_dir,
        "output_dir": output_dir,
        "archive_dir": archive_dir,
    }
