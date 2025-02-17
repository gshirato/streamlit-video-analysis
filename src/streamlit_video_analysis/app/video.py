import streamlit as st
import os
import gdown


def gdrive_folder_url(folder_id):
    return f"https://drive.google.com/drive/folders/{folder_id}"


def download_folder(folder_id, output, **kwargs):
    gdown.download_folder(url=gdrive_folder_url(folder_id), output=output, **kwargs)


def create_hierarchical_structure(input_dict):
    # Initialize the root structure
    root = {}

    for key, value in input_dict.items():
        parts = key.split("/")

        if len(parts) == 4:
            byType, id, play_name, team = parts

            # Ensure the structure exists step by step
            if byType not in root:
                root[byType] = {}
            if id not in root[byType]:
                root[byType][id] = {}
            if play_name not in root[byType][id]:
                root[byType][id][play_name] = {}

            # Assign the value to the deepest level
            root[byType][id][play_name][team] = value

    return root


st.title("Video Analysis")

MAX_LOGIN_ATTEMPTS = 3
if "login_attempts" not in st.session_state:
    st.session_state["login_attempts"] = 0
if "is_authenticated" not in st.session_state:
    st.session_state["is_authenticated"] = False

if not st.experimental_user.is_logged_in:
    if st.button("Googleでログイン"):
        st.login("google")
    st.stop()


allowed_users = st.secrets["auth"].get("allowed_users", [])
user_email = st.experimental_user.email
if user_email in allowed_users:
    st.session_state["is_authenticated"] = True
    st.session_state["login_attempts"] = 0
else:
    st.session_state["login_attempts"] += 1
    st.warning(f"ログイン失敗: {user_email}")
    if st.button("再ログイン"):
        st.login("google")
        st.stop()

if st.session_state["is_authenticated"]:
    root_dir = os.path.abspath(os.path.curdir)
    match_map = st.secrets["meta"].get("matches")
    FOLDER_IDS: list = st.secrets["data"].get("folders")
    hierarchical_data = create_hierarchical_structure(FOLDER_IDS)

    temp_dir = os.path.join(".", "temp")

    by_type = st.selectbox("種類", list(hierarchical_data.keys()))
    by_id = st.selectbox(
        "試合", list(hierarchical_data[by_type].keys()), format_func=match_map.get
    )
    by_play_name = st.selectbox(
        "プレーの種類", list(hierarchical_data[by_type][by_id].keys())
    )
    by_team = st.selectbox(
        "チーム", list(hierarchical_data[by_type][by_id][by_play_name].keys())
    )

    folder_id = hierarchical_data[by_type][by_id][by_play_name][by_team]

    foldername = os.path.join(
        temp_dir,
        by_type,
        by_id,
        by_play_name,
        by_team,
    )

    st.markdown("---")

    with st.spinner(f"動画を準備中: {gdrive_folder_url(folder_id)}", show_time=True):

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            download_folder(folder_id, foldername)

    video_files = sorted(
        [name for name in os.listdir(foldername) if name != ".DS_Store"]
    )
    index = st.session_state.get("video_index", 0)

    col1, col2 = st.columns([1, 1])
    with col1:
        previous_button = st.button("◀ 前の動画", disabled=(index == 0))
        if previous_button:
            index = max(0, index - 1)
    with col2:
        next_button = st.button("次の動画 ▶", disabled=(index == len(video_files) - 1))
        if next_button:
            index = min(len(video_files) - 1, index + 1)
        index = max(0, index - 1)
    if next_button:
        index = min(len(video_files) - 1, index + 1)
    uploaded_file = st.selectbox("動画を選択してください", video_files, index=index)
    st.session_state["video_index"] = index
    st.session_state["video_index"] = video_files.index(uploaded_file)

    if uploaded_file:
        video_path = os.path.join(foldername, uploaded_file)
        st.markdown(f"#### [{by_team}] {by_play_name} ({by_id})")
        st.video(video_path, autoplay=True, muted=True)

    if st.button("Logout"):
        st.logout()
        st.session_state["is_authenticated"] = False
        st.session_state["video_index"] = 0
        st.session_state["login_attempts"] = 0
        st.stop()
