import os
import gdown


def list_files_in_folder(folder_id, drive_service):
    """Google Drive のフォルダID内の全ファイルを取得"""
    query = f"'{folder_id}' in parents and trashed=false"
    results = (
        drive_service.files()
        .list(q=query, fields="files(id, name, mimeType)")
        .execute()
    )
    return results.get("files", [])


def download_video(file_id, save_path):
    """Google Drive から動画をダウンロード"""
    if not os.path.exists(save_path):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, save_path, quiet=False)
