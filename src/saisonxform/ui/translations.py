"""Translation module for multi-language support.

Provides translations for English and Japanese following i18n best practices.
"""

import streamlit as st

# Nested translation structure: lang -> component -> key
TRANSLATIONS = {
    "en": {
        # Global/Header
        "global": {
            "app_title": "Saison Transform",
            "app_subtitle": "Financial Transaction Processor",
            "reset": "Reset",
            "language_selector_label": "Language",
        },

        # Workflow Steps
        "steps": {
            "step_1": "Upload",
            "step_2": "Review & Edit",
            "step_3": "Download",
            "status_complete": "✅ Complete",
            "status_in_progress": "⏳ In Progress",
            "status_ready": "📝 Ready",
            "status_locked": "🔒 Locked",
        },

        # Upload Page
        "upload": {
            "title": "Upload Your Files",
            "description": "Upload one or more Saison transaction CSV files to begin processing. Drag and drop files or click to browse.",
            "select_files": "Select Files",
            "zone_caption": "Drag and drop files here or click 'Browse files' button • Accepts CSV files • Max 200MB per file",
            "csv_files": "Upload CSV files",
            "help": "Upload Saison transaction CSV files for processing",
            "uploaded_files": "Uploaded Files",
            "files_ready": "✅ **{count} file(s)** ready for processing",
            "files_cached": "📁 {count} file(s) cached from previous upload",
            "clear_cached": "🔄 Clear cached files",
            "error_no_attendee": "⚠️ **Attendee list not loaded!**\n\nPlease load the attendee reference file (NameList.csv) from the sidebar Settings before uploading files.",
        },

        # Process Page
        "process": {
            "title": "Review & Edit",
            "description": "Process your files and review the generated data. Edit attendee information as needed.",
            "processing_files": "Processing Files",
            "files_label": "files",
            "processing_file": "Processing {filename}...",
            "error_processing": "❌ Error processing {filename}: {error}",
            "all_processed": "✅ All files processed!",
            "files_ready": "✅ **{count} file(s)** processed and ready for review",
            "select_file": "Select file to edit",
            "edit_file": "📝 Edit: {filename}",
            "warning_no_files": "⚠️ No files uploaded. Please return to Step 1 to upload files.",
        },

        # Download Page
        "download": {
            "title": "Download Results",
            "description": "Download your processed files in various formats (CSV, Excel, HTML reports).",
            "ready": "Your files are ready! Download them individually or as a batch.",
            "warning_no_files": "⚠️ No processed files available. Please return to Step 2.",
            "metric_files": "📁 Files Processed",
            "metric_transactions": "📊 Total Transactions",
            "metric_attendees": "👥 Unique Attendees",
            "metric_status": "✅ Status",
            "select_format": "Select Download Format",
            "format_csv": "📊 CSV (Processed Data)",
            "format_excel": "📈 Excel (Enhanced)",
            "format_html": "📄 HTML Report",
            "format_zip": "📦 All Formats (ZIP)",
            "individual": "Individual Downloads",
            "btn_csv": "⬇️ CSV",
            "btn_excel": "⬇️ Excel",
            "btn_html": "⬇️ HTML",
            "batch": "Batch Download",
            "batch_info": "📦 Download all files in a single ZIP archive containing CSV, Excel, and HTML reports.",
            "btn_zip": "📦 Download All (ZIP)",
            "btn_new_files": "🔄 Process New Files",
        },
    },
    "ja": {
        # Global/Header
        "global": {
            "app_title": "セゾン変換",
            "app_subtitle": "金融取引処理",
            "reset": "リセット",
            "language_selector_label": "言語",
        },

        # Workflow Steps
        "steps": {
            "step_1": "アップロード",
            "step_2": "確認・編集",
            "step_3": "ダウンロード",
            "status_complete": "✅ 完了",
            "status_in_progress": "⏳ 処理中",
            "status_ready": "📝 準備完了",
            "status_locked": "🔒 ロック中",
        },

        # Upload Page
        "upload": {
            "title": "ファイルをアップロード",
            "description": "処理を開始するには、1つ以上のセゾン取引CSVファイルをアップロードしてください。ドラッグ＆ドロップまたはクリックして参照してください。",
            "select_files": "ファイルを選択",
            "zone_caption": "ここにファイルをドラッグ＆ドロップするか、「ファイルを参照」ボタンをクリック • CSVファイルを受け付けます • 最大200MB/ファイル",
            "csv_files": "CSVファイルをアップロード",
            "help": "処理用のセゾン取引CSVファイルをアップロード",
            "uploaded_files": "アップロード済みファイル",
            "files_ready": "✅ **{count} ファイル** 処理準備完了",
            "files_cached": "📁 {count} ファイルがキャッシュされています",
            "clear_cached": "🔄 キャッシュをクリア",
            "error_no_attendee": "⚠️ **参加者リストが読み込まれていません！**\n\nファイルをアップロードする前に、サイドバーの設定から参加者参照ファイル（NameList.csv）を読み込んでください。",
        },

        # Process Page
        "process": {
            "title": "確認・編集",
            "description": "ファイルを処理し、生成されたデータを確認します。必要に応じて参加者情報を編集してください。",
            "processing_files": "ファイル処理中",
            "files_label": "ファイル",
            "processing_file": "{filename} を処理中...",
            "error_processing": "❌ {filename} の処理中にエラーが発生しました: {error}",
            "all_processed": "✅ すべてのファイルが処理されました！",
            "files_ready": "✅ **{count} ファイル** 処理完了・確認可能",
            "select_file": "編集するファイルを選択",
            "edit_file": "📝 編集: {filename}",
            "warning_no_files": "⚠️ ファイルがアップロードされていません。ステップ1に戻ってファイルをアップロードしてください。",
        },

        # Download Page
        "download": {
            "title": "結果をダウンロード",
            "description": "処理済みファイルをさまざまな形式でダウンロードできます（CSV、Excel、HTMLレポート）。",
            "ready": "ファイルの準備が整いました！個別またはバッチでダウンロードしてください。",
            "warning_no_files": "⚠️ 処理済みファイルがありません。ステップ2に戻ってください。",
            "metric_files": "📁 処理済みファイル",
            "metric_transactions": "📊 総取引数",
            "metric_attendees": "👥 一意の参加者",
            "metric_status": "✅ ステータス",
            "select_format": "ダウンロード形式を選択",
            "format_csv": "📊 CSV（処理済みデータ）",
            "format_excel": "📈 Excel（拡張版）",
            "format_html": "📄 HTMLレポート",
            "format_zip": "📦 すべての形式（ZIP）",
            "individual": "個別ダウンロード",
            "btn_csv": "⬇️ CSV",
            "btn_excel": "⬇️ Excel",
            "btn_html": "⬇️ HTML",
            "batch": "バッチダウンロード",
            "batch_info": "📦 CSV、Excel、HTMLレポートを含む単一のZIPアーカイブですべてのファイルをダウンロードします。",
            "btn_zip": "📦 すべてダウンロード（ZIP）",
            "btn_new_files": "🔄 新しいファイルを処理",
        },
    }
}


def load_translations():
    """Load translations into session state if not already loaded.

    This should be called once at app initialization.
    """
    if 'translations' not in st.session_state:
        st.session_state.translations = TRANSLATIONS

    # Initialize language preference
    if 'lang' not in st.session_state:
        st.session_state.lang = 'en'


def get_text(key_path: str, **kwargs) -> str:
    """Get translated text for a given key path.

    Follows i18n best practices with dot-notation key paths.

    Args:
        key_path: Dot-separated path to translation key (e.g., 'global.app_title' or 'upload.title')
        **kwargs: Format parameters for dynamic text (e.g., count=5, filename='test.csv')

    Returns:
        Translated text with format parameters applied

    Examples:
        >>> get_text('global.app_title')
        'Saison Transform'
        >>> get_text('upload.files_ready', count=3)
        '✅ **3 file(s)** ready for processing'
    """
    # Get current language from session state
    lang = st.session_state.get('lang', 'en')

    # Navigate nested dictionary using dot notation
    keys = key_path.split('.')
    text = TRANSLATIONS.get(lang, TRANSLATIONS['en'])

    for key in keys:
        if isinstance(text, dict):
            text = text.get(key, key_path)
        else:
            return key_path  # Return key path if navigation fails

    # Apply format parameters if provided
    if kwargs and isinstance(text, str):
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            # Return text as-is if formatting fails
            pass

    return text
