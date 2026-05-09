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
