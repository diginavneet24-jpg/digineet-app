import streamlit as st
import feedparser

st.title("📺 DigiNeet News Live")

# News Fetch
feed = feedparser.parse("https://news.google.com/rss/headlines/section/topic/NATION?ceid=IN:hi&hl=hi&gl=IN")

if st.button("Aaj Ki Badi Khabrein Dekhein"):
    for entry in feed.entries[:5]:
        st.subheader(f"🔥 {entry.title.split('-')[0]}")
        st.write(f"🔗 [Poori Khabar Padhein]({entry.link})")
        st.divider()
import streamlit as st
import asyncio, os, feedparser
from edge_tts import Communicate

st.set_page_config(page_title="DigiNeet AI Video", page_icon="🎬")
st.title("🎬 DigiNeet AI Video Creator")

# News Fetch
feed = feedparser.parse("https://news.google.com/rss/headlines/section/topic/NATION?ceid=IN:hi&hl=hi&gl=IN")

if st.button("🚀 Create & Download News Video"):
    if not feed.entries:
        st.error("News nahi mil rahi!")
    else:
        with st.spinner("AI Video ban raha hai, thoda intezar karein..."):
            try:
                # 1. Sirf Top News lena
                news_text = feed.entries[0].title.split("-")[0].strip()
                st.info(f"Khabar: {news_text}")

                # 2. Audio Banana
                audio_file = "news_audio.mp3"
                tts = Communicate(f"Namaste, DigiNeet News mein swagat hai. Aaj ki mukhya khabar. {news_text}", "hi-IN-MadhurNeural")
                asyncio.run(tts.save(audio_file))

                # 3. Video Rendering (Simple & Fast)
                video_file = "digineet_video.mp4"
                # FFmpeg command jo background blue rakhega aur niche text scroll karega
                cmd = f'ffmpeg -y -f lavfi -i color=c=0x000520:s=720x1280:d=10 -i {audio_file} -vf "drawbox=y=ih-120:color=red@0.8:width=iw:height=120:t=fill, drawtext=text=\'DIGINEET NEWS\':fontcolor=yellow:fontsize=50:x=(w-text_w)/2:y=150, drawtext=text=\'{news_text}\':fontcolor=white:fontsize=30:x=w-mod(150*t\,w+tw):y=ih-80" -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest {video_file}'
                
                os.system(cmd)

                # 4. Final Result
                if os.path.exists(video_file):
                    st.success("✅ Video taiyar hai!")
                    with open(video_file, "rb") as f:
                        st.download_button("📥 Click to Download Video", f, file_name="News_Video.mp4")
                else:
                    st.error("Video file generate nahi hui. Reboot karein.")
            except Exception as e:
                st.error(f"Error: {e}")

# Niche headlines display (Aapki purani working cheez)
st.divider()
st.subheader("📰 Today's Headlines")
for entry in feed.entries[:3]:
    st.write(f"🔥 {entry.title.split('-')[0]}")
