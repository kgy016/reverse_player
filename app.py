import streamlit as st
import tempfile
import os

# MoviePy 버전 호환성 처리
try:
    from moviepy.editor import VideoFileClip
    import moviepy.video.fx.all as vfx
except ImportError:
    from moviepy import VideoFileClip
    import moviepy.video.fx as vfx

# 1. 페이지 설정
st.set_page_config(page_title="거꾸로 영상 제작소", page_icon="⏪")

st.title("⏪ 초간단 영상 역재생기")
st.info("짧은 영상(10~20초)을 올리면 시간을 뒤집어 드립니다!")

# 2. 파일 업로드
uploaded_file = st.file_uploader("역재생할 영상을 업로드하세요", type=["mp4", "mov", "avi"])

if uploaded_file:
    # 임시 파일 생성 및 닫기 (MoviePy가 읽을 수 있도록 경로 확보)
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    video_path = tfile.name
    tfile.close()

    st.video(video_path)
    
    if st.button("⏪ 시간 뒤집기 시작!", use_container_width=True):
        with st.spinner("영상을 요리하는 중... 잠시만 기다려주세요."):
            try:
                # 3. 영상 처리
                clip = VideoFileClip(video_path)
                
                # 역재생 적용 (버전에 따라 다른 방식 대응)
                try:
                    reversed_clip = clip.fx(vfx.time_mirror)
                except:
                    reversed_clip = clip.reversed()
                
                output_path = "reversed_result.mp4"
                
                # 인코딩 시작
                reversed_clip.write_videofile(output_path, codec="libx264", audio=True)
                
                # 4. 결과 출력
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
                
                clip.close()
                reversed_clip.close()
                
            except Exception as e:
                st.error(f"⚠️ 영상 처리 중 오류가 발생했습니다: {e}")
                st.info("영상이 너무 길거나 고화질이면 서버가 힘들어할 수 있어요.")
            finally:
                if os.path.exists(video_path):
                    os.remove(video_path)
