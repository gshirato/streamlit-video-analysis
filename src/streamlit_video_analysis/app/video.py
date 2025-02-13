import streamlit as st
import os

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

    video_dir = os.path.join(root_dir, "video")
    player_name = st.selectbox("選手を選択", os.listdir(video_dir))
    video_files = os.listdir(f"video/{player_name}")
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
        video_path = os.path.join(video_dir, player_name, uploaded_file)
        st.video(video_path)

    if st.button("Logout"):
        st.logout()
        st.session_state["is_authenticated"] = False
        st.session_state["video_index"] = 0
        st.session_state["login_attempts"] = 0
        st.stop()
