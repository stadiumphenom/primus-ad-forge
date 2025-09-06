
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="PRIMUS Ad Forge", layout="centered")

st.title("🎬 PRIMUS Ad Forge — Ad Simulation")

input_path = st.text_input("Input file path (e.g. ./sample.mp4)")
hook = st.text_area("Hook (e.g. This cleared my skin in 7 days)")
cta = st.text_area("Call to Action (e.g. Tap to try it now)")
brand = st.text_input("Brand watermark (optional)")

platforms = []
cols = st.columns(3)
with cols[0]:
    if st.toggle("tiktok", value=True):
        platforms.append("tiktok")
with cols[1]:
    if st.toggle("instagram"):
        platforms.append("instagram")
with cols[2]:
    if st.toggle("facebook"):
        platforms.append("facebook")

if st.button("Simulate Ad Creation"):
    if not input_path or not hook or not cta:
        st.warning("Please fill in all required fields.")
    else:
        st.success("✅ Simulation started")
        for p in platforms:
            st.markdown(f"**Simulating for {p.upper()}...**")
            st.text(f"  Hook: {hook}")
            st.text(f"  CTA: {cta}")
            st.text(f"  Brand: {brand or '[none]'}")
            st.text(f"  Output: {Path(input_path).stem}_{p}.mp4")
            st.markdown("---")
