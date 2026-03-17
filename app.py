import streamlit as st
import cv2
import tempfile
import os
import numpy as np

st.set_page_config(page_title="거꾸로 영상 제작소", page_icon="⏪")
st.title("⏪ 초간단 영상 역재생기 (OpenCV 버전)")
st.info("MoviePy 에러를 극복한 새로운 버전입니다! 짧은 영상을 올려주세요.")

uploaded_file = st.file_uploader("역재생할 영상을 업로드하세요", type=["mp4", "mov", "avi"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    video_path = tfile.name
    tfile.close()

    st.video(video_path)
    
    if st.button("⏪ 시간 뒤집기 시작!", use_container_width=True):
        with st.spinner("프레임을 거꾸로 조립하는 중..."):
            try:
                # 영상 읽기
                cap = cv2.VideoCapture(video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                # 모든 프레임 읽어서 리스트에 저장
                frames = []
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frames.append(frame)
                cap.release()

                if len(frames) > 0:
                    # 프레임 뒤집기
                    frames.reverse()
                    
                    # 저장 설정
                    output_path = "reversed_result.mp4"
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # 코덱 설정
                    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                    
                    for f in frames:
                        out.write(f)
                    out.release()

                    st.divider()
                    st.subheader("✨ 역재생 완료!")
                    st.video(output_path)
                    
                    with open(output_path, "rb") as file:
                        st.download_button("💾 영상 저장하기", file, "reversed.mp4", "video/mp4")
                else:
                    st.error("영상을 읽을 수 없습니다.")

            except Exception as e:
                st.error(f"오류 발생: {e}")
            finally:
                if os.path.exists(video_path):
                    os.remove(video_path)
