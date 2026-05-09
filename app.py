import streamlit as st
import asyncio, requests, os, io
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
        # Clean text for FFmpeg
        clean_title = art['title'].split("-")[0].strip().replace("'", "").replace(":", "")
        full_script += f"Khabar number {i+1}: {clean_title}. "
        headlines_text += f" [{i+1}] {clean_title} • "

    tts = Communicate(full_script, "hi-IN-MadhurNeural")
    await tts.save("final_audio.mp3")
    
    # 3. Rendering with absolute path to avoid file errors
    output_file = "digineet_output.mp4"
    if os.path.exists(output_file):
        os.remove(output_file)
        
    cmd = (
        f"ffmpeg -y -f lavfi -i \"color=c=0x000520:s=720x1280:d=60\" -i final_audio.mp3 "
        f"-vf \"drawbox=y=ih-120:color=red@0.8:width=iw:height=120:t=fill, "
        f"drawtext=text='DIGINEET NEWS':fontcolor=yellow:fontsize=70:x=(w-text_w)/2:y=150:shadowcolor=black:shadowx=2:shadowy=2, "
        f"drawtext=text='{headlines_text}':fontcolor=white:fontsize=35:x=w-mod(200*t\,w+tw):y=ih-80\" "
        f"-c:v libx264 -pix_fmt yuv420p -preset superfast -c:a aac -shortest {output_file}"
    )
    
    os.system(cmd)
    return output_file

if st.button("🚀 Generate & Download Video"):
    with st.spinner("AI Graphics aur Audio merge kar raha hai..."):
        try:
            video_path = asyncio.run(process_video(news_count))
            
            if os.path.exists(video_path):
                with open(video_path, "rb") as f:
                    video_bytes = f.read()
                    
                st.success("✅ Video Taiyar Hai!")
                
                # Naya Download Button (Direct bytes se)
                st.download_button(
                    label="📥 Click Here to Download",
                    data=video_bytes,
                    file_name="DigiNeet_News.mp4",
                    mime="video/mp4"
                )
                
                # Display attempt
                st.video(video_bytes)
            else:
                st.error("Video file generate nahi ho payi. FFmpeg mein error hai.")
                
        except Exception as e:
            st.error(f"Kuch gadbad ho gayi: {e}")
