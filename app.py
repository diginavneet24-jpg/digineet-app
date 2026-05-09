import streamlit as st
import asyncio, requests, os
from edge_tts import Communicate

st.set_page_config(page_title="DigiNeet AI Fix", page_icon="📺")
st.title("📺 DigiNeet AI News")

api_key = "0c4472faa2424275a880d2d83e17eb5f"

async def make_video():
    # 1. News Fetch
    res = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}").json()
    title = res['articles'][0]['title'].replace("'", "")
    
    # 2. Audio
    tts = Communicate(f"Namaste. Aaj ki badi khabar. {title}", "hi-IN-MadhurNeural")
    await tts.save("test.mp3")
    
    # 3. Simple Video Command
    os.system("ffmpeg -y -f lavfi -i color=c=blue:s=1280x720:d=10 -i test.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest out.mp4")
    return "out.mp4"

if st.button("Direct Video Generate"):
    with st.spinner("Processing..."):
        try:
            path = asyncio.run(make_video())
            if os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button("📥 Yahan Click Karein Download ke liye", f, "news.mp4")
                st.video(path)
            else:
                st.error("Server par video nahi ban payi. 'packages.txt' check karein.")
        except Exception as e:
            st.error(f"Error: {e}")
