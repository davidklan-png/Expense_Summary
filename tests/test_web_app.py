"""Unit tests for web_app.py."""
import pandas as pd
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from web_app import (
    load_attendee_reference,
    initialize_session_state,
)


class TestLoadAttendeeReference:
    """Test attendee reference loading."""

    def test_load_existing_file(self, tmp_path):
        """Should load valid CSV file."""
        ref_file = tmp_path / "NameList.csv"
        ref_file.write_text("ID,Name,Title,Company\n1,Test,Manager,Corp\n", encoding="utf-8")

        result = load_attendee_reference(ref_file)

        assert result is not None
        assert len(result) == 1
        assert result.iloc[0]["Name"] == "Test"

    def test_missing_file(self, tmp_path):
        """Should return None for missing file."""
        result = load_attendee_reference(tmp_path / "missing.csv")
        assert result is None

    def test_load_with_japanese_encoding(self, tmp_path):
        """Should handle UTF-8 encoded Japanese text."""
        ref_file = tmp_path / "NameList.csv"
        ref_file.write_text("ID,Name,Title,Company\n1,山田太郎,部長,株式会社\n", encoding="utf-8")

        result = load_attendee_reference(ref_file)

        assert result is not None
        assert result.iloc[0]["Name"] == "山田太郎"


class TestInitializeSessionState:
    """Test session state initialization."""

    @patch('web_app.st')
    def test_initialize_session_state_creates_required_keys(self, mock_st):
        """Should create all required session state keys."""
        mock_st.session_state = {}
        mock_config = Mock()
        mock_config.min_attendees = 2
        mock_config.max_attendees = 8

        with patch('web_app.Config', return_value=mock_config):
            initialize_session_state()

        assert "attendee_ref" in mock_st.session_state
        assert "attendee_ref_path" in mock_st.session_state
        assert "config" in mock_st.session_state
        assert "processed_files" in mock_st.session_state
        assert "uploaded_files_cache" in mock_st.session_state

    @patch('web_app.st')
    def test_initialize_preserves_existing_state(self, mock_st):
        """Should not overwrite existing session state values."""
        mock_st.session_state = {
            "attendee_ref": "existing_ref",
            "config": "existing_config",
        }

        initialize_session_state()

        assert mock_st.session_state["attendee_ref"] == "existing_ref"
        assert mock_st.session_state["config"] == "existing_config"


# Fixtures
@pytest.fixture
def sample_csv_bytes():
    """Sample CSV file as bytes."""
    csv_content = """利用日,ご利用店名及び商品名,利用金額,科目＆No.
2025-01-10,Restaurant,15000,会議費
"""
    return csv_content.encode('utf-8')


@pytest.fixture
def sample_attendee_ref():
    """Sample attendee reference DataFrame."""
    return pd.DataFrame({
        "ID": ["1", "2", "3"],
        "Name": ["Alice", "Bob", "Charlie"],
        "Title": ["Manager", "Lead", "Developer"],
        "Company": ["Corp A", "Corp B", "Corp C"]
    })


@pytest.fixture
def sample_processed_data():
    """Sample processed file data."""
    return {
        "df": pd.DataFrame({
            "利用日": ["2025-01-10"],
            "ご利用店名及び商品名": ["Restaurant"],
            "利用金額": [15000],
            "科目＆No.": ["会議費"],
            "人数": [3],
            "ID1": ["1"],
            "ID2": ["2"],
            "ID3": ["3"],
            "ID4": [""],
            "ID5": [""],
            "ID6": [""],
            "ID7": [""],
            "ID8": [""],
            "備考": [""]
        }),
        "encoding": "utf-8",
        "pre_header": [],
        "unique_attendees": []
    }
