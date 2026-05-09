import streamlit as st
import asyncio, requests, os
from edge_tts import Communicate

st.set_page_config(page_title="DigiNeet AI News", page_icon="📺")
st.title("📺 DigiNeet AI News Generator")

# Settings
news_count = st.sidebar.slider("Kitni News chahiye?", 1, 5, 3)
api_key = "0c4472faa2424275a880d2d83e17eb5f"

async def process_video(count):
    # 1. News Fetch karna
    res = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}").json()
    articles = res['articles'][:count]
    
    st.info(f"⚡ {count} Badi Khabrein Mil Gayi Hain...")
    
    # 2. Voiceover taiyar karna
    full_script = "Namaste, DigiNeet News mein aapka swagat hai. Aaj ki badi khabrein kuch is prakar hain. "
    for i, art in enumerate(articles):
        full_script += f"Khabar number {i+1}: {art['title']}. "
    
    tts = Communicate(full_script, "hi-IN-MadhurNeural")
    await tts.save("final_audio.mp3")
    
    # 3. Video Render karna (No image needed)
    # Yeh command ek blue background banayega aur upar news likhega
    os.system("ffmpeg -y -f lavfi -i color=c=0x1a1a2e:s=720x1280:d=30 -i final_audio.mp3 -vf \"drawtext=text='DIGINEET NEWS':fontcolor=yellow:fontsize=60:x=(w-text_w)/2:y=100, drawtext=text='TOP HEADLINES TODAY':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=200\" -c:v libx264 -c:a copy -shortest final_video.mp4")
    
    return "final_video.mp4"

if st.button("🎬 Create Video Now"):
    with st.spinner("AI Video bana raha hai... 1 minute wait karein"):
        try:
            video_path = asyncio.run(process_video(news_count))
            st.video(video_path)
            with open(video_path, "rb") as f:
                st.download_button("📥 Download Video", f, "DigiNeet_News.mp4")
        except Exception as e:
            st.error(f"Error: {e}")
