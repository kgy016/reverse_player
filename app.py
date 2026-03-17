import streamlit as st
import cv2
import tempfile
import os
import numpy as np

st.set_page_config(page_title="거꾸로 영상 제작소", page_icon="⏪")
st.title("⏪ 초간단 영상 역재생기")
st.info("웹 브라우저 재생용 코덱(H.264)이 적용된 버전입니다.")

uploaded_file = st.file_uploader("역재생할 영상을 업로드하세요", type=["mp4", "mov", "avi"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    video_path = tfile.name
    tfile.close()

    st.video(video_path)
    
    if st.button("⏪ 시간 뒤집기 시작!", use_container_width=True):
        with st.spinner("웹용 영상으로 변환 중..."):
            try:
                cap = cv2.VideoCapture(video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                frames = []
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frames.append(frame)
                cap.release()

                if len(frames) > 0:
                    frames.reverse()
                    
                    output_path = "reversed_web.mp4"
                    # --- [수정 포인트] 웹 표준 코덱 avc1 사용 ---
                    fourcc = cv2.VideoWriter_fourcc(*'avc1') 
                    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                    
                    for f in frames:
                        out.write(f)
                    out.release()

                    st.divider()
                    st.subheader("✨ 역재생 완료!")
                    
                    # --- [수정 포인트] 파일을 바이트로 읽어서 재생 (브라우저 호환성 향상) ---
                    with open(output_path, "rb") as video_file:
                        video_bytes = video_file.read()
                        st.video(video_bytes) # 이제 미리보기가 잘 나올 거예요!
                    
                    st.download_button("💾 영상 저장하기", video_bytes, "reversed.mp4", "video/mp4")
                else:
                    st.error("영상을 읽을 수 없습니다.")

            except Exception as e:
                st.error(f"오류 발생: {e}")
                st.info("코덱 문제일 경우 'avc1' 대신 'H264'로 시도해볼 수 있습니다.")
            finally:
                if os.path.exists(video_path):
                    os.remove(video_path)
