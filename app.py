import streamlit as st
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx
import tempfile
import os

# 1. 페이지 설정
st.set_page_config(page_title="거꾸로 영상 제작소", page_icon="⏪")

st.title("⏪ 초간단 영상 역재생기")
st.write("영상을 올리면 시간을 뒤집어 드립니다. (짧은 영상 권장!)")

# 2. 파일 업로드
uploaded_file = st.file_uploader("역재생할 영상을 업로드하세요 (mp4, mov, avi)", type=["mp4", "mov", "avi"])

if uploaded_file:
    # 임시 파일로 저장 (moviepy는 파일 경로가 필요함)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(uploaded_file.read())
        video_path = tmp_file.name

    st.video(video_path) # 원본 미리보기
    
    if st.button("⏪ 시간 뒤집기 시작!", use_container_width=True):
        with st.spinner("영상을 거꾸로 돌리는 중... 잠시만 기다려주세요."):
            try:
                # 3. 영상 처리 로직
                clip = VideoFileClip(video_path)
                
                # 역재생 적용
                reversed_clip = clip.fx(vfx.time_mirror)
                
                # 결과 파일 저장 경로
                output_path = "reversed_video.mp4"
                reversed_clip.write_videofile(output_path, codec="libx264", audio=True)
                
                # 4. 결과 출력 및 다운로드
                st.divider()
                st.subheader("✨ 역재생 완료!")
                st.video(output_path)
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="💾 역재생 영상 저장하기",
                        data=file,
                        file_name="reversed_video.mp4",
                        mime="video/mp4"
                    )
                
                # 사용 후 메모리 해제 및 임시 파일 삭제
                clip.close()
                reversed_clip.close()
                
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")
            finally:
                if os.path.exists(video_path):
                    os.remove(video_path)
