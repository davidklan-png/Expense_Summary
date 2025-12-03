"""Translation module for multi-language support.

Provides translations for English and Japanese.
"""

TRANSLATIONS = {
    "en": {
        # App Title
        "app_title": "Saison Transform",
        "app_subtitle": "Financial Transaction Processor",

        # Header
        "reset": "Reset",

        # Step Labels
        "step_1": "Upload",
        "step_2": "Review & Edit",
        "step_3": "Download",

        # Step Status
        "status_complete": "✅ Complete",
        "status_in_progress": "⏳ In Progress",
        "status_ready": "📝 Ready",
        "status_locked": "🔒 Locked",

        # Step 1: Upload
        "upload_title": "Upload Your Files",
        "upload_description": "Upload one or more Saison transaction CSV files to begin processing. Drag and drop files or click to browse.",
        "select_files": "Select Files",
        "upload_zone_caption": "Drag and drop files here or click 'Browse files' button • Accepts CSV files • Max 200MB per file",
        "upload_csv_files": "Upload CSV files",
        "upload_help": "Upload Saison transaction CSV files for processing",
        "uploaded_files": "Uploaded Files",
        "files_ready": "✅ **{count} file(s)** ready for processing",
        "files_cached": "📁 {count} file(s) cached from previous upload",
        "clear_cached_files": "🔄 Clear cached files",
        "error_no_attendee_list": "⚠️ **Attendee list not loaded!**\n\nPlease load the attendee reference file (NameList.csv) from the sidebar Settings before uploading files.",

        # Step 2: Process & Edit
        "process_title": "Review & Edit",
        "process_description": "Process your files and review the generated data. Edit attendee information as needed.",
        "processing_files": "Processing Files",
        "files_label": "files",
        "processing_file": "Processing {filename}...",
        "error_processing_file": "❌ Error processing {filename}: {error}",
        "all_files_processed": "✅ All files processed!",
        "files_processed_ready": "✅ **{count} file(s)** processed and ready for review",
        "select_file_to_edit": "Select file to edit",
        "edit_file": "📝 Edit: {filename}",
        "warning_no_files": "⚠️ No files uploaded. Please return to Step 1 to upload files.",

        # Step 3: Download
        "download_title": "Download Results",
        "download_description": "Download your processed files in various formats (CSV, Excel, HTML reports).",
        "download_ready": "Your files are ready! Download them individually or as a batch.",
        "warning_no_processed_files": "⚠️ No processed files available. Please return to Step 2.",
        "metric_files_processed": "📁 Files Processed",
        "metric_total_transactions": "📊 Total Transactions",
        "metric_unique_attendees": "👥 Unique Attendees",
        "metric_status": "✅ Status",
        "select_download_format": "Select Download Format",
        "format_csv": "📊 CSV (Processed Data)",
        "format_excel": "📈 Excel (Enhanced)",
        "format_html": "📄 HTML Report",
        "format_zip": "📦 All Formats (ZIP)",
        "individual_downloads": "Individual Downloads",
        "download_csv_button": "⬇️ CSV",
        "download_excel_button": "⬇️ Excel",
        "download_html_button": "⬇️ HTML",
        "batch_download": "Batch Download",
        "batch_download_info": "📦 Download all files in a single ZIP archive containing CSV, Excel, and HTML reports.",
        "download_all_zip_button": "📦 Download All (ZIP)",
        "process_new_files_button": "🔄 Process New Files",

        # Sidebar
        "settings": "⚙️ Settings",
        "attendees_loaded": "✅ {count} attendees loaded",
        "reference_data": "📂 Reference Data",
        "processing_params": "🔧 Processing Parameters",

        # Common
        "complete": "Complete",
        "kb": "KB",
    },
    "ja": {
        # App Title
        "app_title": "セゾン変換",
        "app_subtitle": "金融取引処理",

        # Header
        "reset": "リセット",

        # Step Labels
        "step_1": "アップロード",
        "step_2": "確認・編集",
        "step_3": "ダウンロード",

        # Step Status
        "status_complete": "✅ 完了",
        "status_in_progress": "⏳ 処理中",
        "status_ready": "📝 準備完了",
        "status_locked": "🔒 ロック中",

        # Step 1: Upload
        "upload_title": "ファイルをアップロード",
        "upload_description": "処理を開始するには、1つ以上のセゾン取引CSVファイルをアップロードしてください。ドラッグ＆ドロップまたはクリックして参照してください。",
        "select_files": "ファイルを選択",
        "upload_zone_caption": "ここにファイルをドラッグ＆ドロップするか、「ファイルを参照」ボタンをクリック • CSVファイルを受け付けます • 最大200MB/ファイル",
        "upload_csv_files": "CSVファイルをアップロード",
        "upload_help": "処理用のセゾン取引CSVファイルをアップロード",
        "uploaded_files": "アップロード済みファイル",
        "files_ready": "✅ **{count} ファイル** 処理準備完了",
        "files_cached": "📁 {count} ファイルがキャッシュされています",
        "clear_cached_files": "🔄 キャッシュをクリア",
        "error_no_attendee_list": "⚠️ **参加者リストが読み込まれていません！**\n\nファイルをアップロードする前に、サイドバーの設定から参加者参照ファイル（NameList.csv）を読み込んでください。",

        # Step 2: Process & Edit
        "process_title": "確認・編集",
        "process_description": "ファイルを処理し、生成されたデータを確認します。必要に応じて参加者情報を編集してください。",
        "processing_files": "ファイル処理中",
        "files_label": "ファイル",
        "processing_file": "{filename} を処理中...",
        "error_processing_file": "❌ {filename} の処理中にエラーが発生しました: {error}",
        "all_files_processed": "✅ すべてのファイルが処理されました！",
        "files_processed_ready": "✅ **{count} ファイル** 処理完了・確認可能",
        "select_file_to_edit": "編集するファイルを選択",
        "edit_file": "📝 編集: {filename}",
        "warning_no_files": "⚠️ ファイルがアップロードされていません。ステップ1に戻ってファイルをアップロードしてください。",

        # Step 3: Download
        "download_title": "結果をダウンロード",
        "download_description": "処理済みファイルをさまざまな形式でダウンロードできます（CSV、Excel、HTMLレポート）。",
        "download_ready": "ファイルの準備が整いました！個別またはバッチでダウンロードしてください。",
        "warning_no_processed_files": "⚠️ 処理済みファイルがありません。ステップ2に戻ってください。",
        "metric_files_processed": "📁 処理済みファイル",
        "metric_total_transactions": "📊 総取引数",
        "metric_unique_attendees": "👥 一意の参加者",
        "metric_status": "✅ ステータス",
        "select_download_format": "ダウンロード形式を選択",
        "format_csv": "📊 CSV（処理済みデータ）",
        "format_excel": "📈 Excel（拡張版）",
        "format_html": "📄 HTMLレポート",
        "format_zip": "📦 すべての形式（ZIP）",
        "individual_downloads": "個別ダウンロード",
        "download_csv_button": "⬇️ CSV",
        "download_excel_button": "⬇️ Excel",
        "download_html_button": "⬇️ HTML",
        "batch_download": "バッチダウンロード",
        "batch_download_info": "📦 CSV、Excel、HTMLレポートを含む単一のZIPアーカイブですべてのファイルをダウンロードします。",
        "download_all_zip_button": "📦 すべてダウンロード（ZIP）",
        "process_new_files_button": "🔄 新しいファイルを処理",

        # Sidebar
        "settings": "⚙️ 設定",
        "attendees_loaded": "✅ {count} 人の参加者が読み込まれました",
        "reference_data": "📂 参照データ",
        "processing_params": "🔧 処理パラメータ",

        # Common
        "complete": "完了",
        "kb": "KB",
    }
}


def get_text(key: str, lang: str = "en", **kwargs) -> str:
    """Get translated text for a given key.

    Args:
        key: Translation key
        lang: Language code ('en' or 'ja')
        **kwargs: Format parameters for the text

    Returns:
        Translated text with format parameters applied
    """
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text
