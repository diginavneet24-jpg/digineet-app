import streamlit as st
import asyncio, requests, os
from edge_tts import Communicate

st.set_page_config(page_title="DigiNeet AI News", page_icon="📺")
st.title("📺 DigiNeet AI News")

# Professional Key (Maine ek alternative way bhi add kiya hai)
api_key = "0c4472faa2424275a880d2d83e17eb5f"

async def make_video():
    # 1. News Fetch safely
    try:
        res = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}")
        data = res.json()
        
        if data.get('status') != 'ok' or not data.get('articles'):
            return "error_news", "News nahi mil paa rahi hai. API Key check karein."
            
        title = data['articles'][0]['title'].replace("'", "")
    except Exception as e:
        return "error_news", str(e)
    
    # 2. Audio
    try:
        tts = Communicate(f"Namaste. Aaj ki badi khabar. {title}", "hi-IN-MadhurNeural")
        await tts.save("test.mp3")
    except:
        return "error_voice", "Voice generate nahi hui."
    
    # 3. Simple Video Command
    os.system("ffmpeg -y -f lavfi -i color=c=0x000520:s=1280x720:d=10 -i test.mp3 -vf \"drawtext=text='DIGINEET NEWS':fontcolor=yellow:fontsize=50:x=(w-text_w)/2:y=100\" -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest out.mp4")
    
    return "success", "out.mp4"

if st.button("Direct Video Generate"):
    with st.spinner("News fetch karke video banayi ja rahi hai..."):
        status, result = asyncio.run(make_video())
        
        if status == "success":
            if os.path.exists(result):
                st.success("Video Taiyar Hai!")
                with open(result, "rb") as f:
                    st.download_button("📥 Download Karein", f, "news.mp4")
                st.video(result)
            else:
                st.error("Video file nahi bani. 'packages.txt' mein ffmpeg check karein.")
        else:
            st.error(f"Gadbad: {result}")
