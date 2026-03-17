import streamlit as st
import cv2
import tempfile
import os
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="거꾸로 영상 제작소", page_icon="⏪")
st.title("⏪ 초간단 영상 역재생기")
st.info("안정적인 프레임 역재생 버전입니다. (소리 미포함)")

uploaded_file = st.file_uploader("역재생할 영상을 업로드하세요", type=["mp4", "mov", "avi"])

if uploaded_file:
    # 원본 파일 임시 저장
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    video_path = tfile.name
    tfile.close()

    st.video(video_path)
    
    if st.button("⏪ 시간 뒤집기 시작!", use_container_width=True):
        with st.spinner("영상을 뒤집어 새 파일을 만드는 중..."):
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
                    
                    # --- [핵심 수정] 가장 안전한 mp4v 코덱 사용 ---
                    output_path = os.path.join(tempfile.gettempdir(), "reversed_final.mp4")
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
                    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                    
                    if not out.isOpened():
                        st.error("비디오 기록기를 초기화할 수 없습니다. 코덱 호환성 문제입니다.")
                    else:
                        for f in frames:
                            out.write(f)
                        out.release()

                        # 파일이 실제로 생성되었는지 확인
                        if os.path.exists(output_path):
                            st.divider()
                            st.subheader("✨ 역재생 완료!")
                            
                            with open(output_path, "rb") as video_file:
                                video_bytes = video_file.read()
                                # 브라우저 미리보기 시도 (안 나올 경우 다운로드 버튼 이용)
                                st.video(video_bytes)
                                
                            st.download_button(
                                label="💾 역재생 영상 저장하기",
                                data=video_bytes,
                                file_name="reversed_video.mp4",
                                mime="video/mp4"
                            )
                        else:
                            st.error("파일 생성에 실패했습니다.")
                else:
                    st.error("영상의 프레임을 읽을 수 없습니다.")

            except Exception as e:
                st.error(f"오류 발생: {e}")
            finally:
                # 임시 파일 정리
                if os.path.exists(video_path):
                    os.remove(video_path)
