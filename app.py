import streamlit as st
import asyncio, requests, os
from edge_tts import Communicate

st.set_page_config(page_title="DigiNeet AI Pro", page_icon="📺")
st.title("📺 DigiNeet Pro News Creator")

news_count = st.sidebar.slider("Kitni News?", 1, 5, 3)
api_key = "0c4472faa2424275a880d2d83e17eb5f"

async def process_video(count):
    # 1. Fetch News
    res = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}").json()
    articles = res['articles'][:count]
    
    st.info(f"⚡ {count} Headlines mil gayi hain...")
    
    # 2. Voiceover & Script
    full_script = "Namaste, DigiNeet News mein aapka swagat hai. Aaj ki mukhya khabrein. "
    headlines_text = ""
    for i, art in enumerate(articles):
        clean_title = art['title'].split("-")[0].strip().replace("'", "")
        full_script += f"Khabar number {i+1}: {clean_title}. "
        headlines_text += f" [{i+1}] {clean_title} • "

    tts = Communicate(full_script, "hi-IN-MadhurNeural")
    await tts.save("final_audio.mp3")
    
    # 3. FIX: Browser-Compatible Rendering
    # Humne yahan '-pix_fmt yuv420p' add kiya hai taaki Chrome/Android par chale
    cmd = (
        f"ffmpeg -y -f lavfi -i \"color=c=0x000520:s=720x1280:d=60\" -i final_audio.mp3 "
        f"-vf \"drawbox=y=ih-120:color=red@0.8:width=iw:height=120:t=fill, "
        f"drawtext=text='DIGINEET NEWS':fontcolor=yellow:fontsize=70:x=(w-text_w)/2:y=150:shadowcolor=black:shadowx=2:shadowy=2, "
        f"drawtext=text='{headlines_text}':fontcolor=white:fontsize=35:x=w-mod(200*t\,w+tw):y=ih-80\" "
        f"-c:v libx264 -pix_fmt yuv420p -c:a aac -shortest final_video.mp4"
    )
    
    os.system(cmd)
    return "final_video.mp4"

if st.button("🚀 Generate Professional Video"):
    with st.spinner("AI Graphics aur Audio merge kar raha hai..."):
        try:
            if os.path.exists("final_video.mp4"): os.remove("final_video.mp4") # Purani file delete
            video_path = asyncio.run(process_video(news_count))
            
            # Video display
            with open(video_path, "rb") as f:
                st.video(f.read())
            
            st.success("Bhai, ab check karo! Video play honi chahiye.")
            with open(video_path, "rb") as f:
                st.download_button("📥 Download News Video", f, "DigiNeet_News.mp4")
        except Exception as e:
            st.error(f"Error: {e}")
