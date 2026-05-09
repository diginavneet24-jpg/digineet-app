import streamlit as st
import asyncio, os, feedparser, subprocess

st.set_page_config(page_title="DigiNeet AI Video", page_icon="🎬")
st.title("🎬 DigiNeet AI Video Creator")

# News Fetch
feed = feedparser.parse("https://news.google.com/rss/headlines/section/topic/NATION?ceid=IN:hi&hl=hi&gl=IN")

if st.button("🚀 Create & Download News Video"):
    if not feed.entries:
        st.error("News nahi mil rahi!")
    else:
        with st.spinner("AI Video process ho raha hai..."):
            try:
                # 1. News Text Clean
                news_text = feed.entries[0].title.split("-")[0].strip().replace("'", "").replace('"', "")
                st.info(f"Khabar: {news_text}")

                # 2. Audio Generation
                audio_file = "news_audio.mp3"
                tts = Communicate(f"Namaste, DigiNeet News. Aaj ki mukhya khabar. {news_text}", "hi-IN-MadhurNeural")
                asyncio.run(tts.save(audio_file))

                # 3. Fast Video Rendering
                video_file = "digineet_video.mp4"
                if os.path.exists(video_file): os.remove(video_file)

                # Command with 'ultrafast' preset to avoid download failure
                cmd = f'ffmpeg -y -f lavfi -i color=c=0x000520:s=720x1280:d=10 -i {audio_file} -vf "drawbox=y=ih-120:color=red@0.8:width=iw:height=120:t=fill, drawtext=text=\'DIGINEET NEWS\':fontcolor=yellow:fontsize=50:x=(w-text_w)/2:y=150, drawtext=text=\'{news_text[:60]}\':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=ih-80" -c:v libx264 -preset ultrafast -pix_fmt yuv420p -c:a aac -shortest {video_file}'
                
                subprocess.run(cmd, shell=True, capture_output=True)

                # 4. Direct Download
                if os.path.exists(video_file):
                    with open(video_file, "rb") as file:
                        btn = st.download_button(
                            label="📥 CLICK HERE TO SAVE VIDEO",
                            data=file,
                            file_name="DigiNeet_News.mp4",
                            mime="video/mp4"
                        )
                    st.success("Bhai, ab download button pe click karo!")
                else:
                    st.error("Server Busy hai, 1 minute baad fir try karein.")
            except Exception as e:
                st.error(f"Technical Error: {e}")

st.divider()
st.subheader("📰 Today's Headlines")
for entry in feed.entries[:3]:
    st.write(f"🔥 {entry.title.split('-')[0]}")
