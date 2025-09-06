
import streamlit as st
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from pathlib import Path
import tempfile

st.set_page_config(page_title="PRIMUS Ad Forge", layout="centered")
st.title("🎬 PRIMUS Ad Forge — Real Ad Generator")

input_file = st.file_uploader("Upload your video", type=["mp4", "mov"])
hook = st.text_input("Hook Text", "This cleared my skin in 7 days")
cta = st.text_input("Call to Action", "Tap to try it now")
brand = st.text_input("Watermark (optional)", "")

platform = st.selectbox("Select Platform", ["tiktok", "instagram", "facebook"])
start_btn = st.button("Generate Video")

platform_sizes = {
    "tiktok": (1080, 1920),
    "instagram": (1080, 1920),
    "facebook": (1080, 1080),
}

def process_video(uploaded, hook_text, cta_text, brand_text, platform):
    temp_dir = tempfile.mkdtemp()
    input_path = Path(temp_dir) / "input.mp4"
    with open(input_path, "wb") as f:
        f.write(uploaded.read())

    clip = VideoFileClip(str(input_path)).subclip(0, min(10, uploaded.size))  # max 10 sec
    clip = clip.resize(height=platform_sizes[platform][1])

    W, H = clip.size
    txt_clips = []

    if hook_text:
        txt_clips.append(TextClip(hook_text, fontsize=60, color='white', bg_color='black', size=(W, None))
                         .set_position(("center", 50)).set_duration(clip.duration))

    if cta_text:
        txt_clips.append(TextClip(cta_text, fontsize=50, color='white', bg_color='black', size=(W, None))
                         .set_position(("center", H - 120)).set_duration(clip.duration))

    if brand_text:
        txt_clips.append(TextClip(brand_text, fontsize=40, color='gray', bg_color=None)
                         .set_position(("right", "bottom")).set_duration(clip.duration))

    final = CompositeVideoClip([clip] + txt_clips)
    output_path = Path(temp_dir) / f"output_{platform}.mp4"
    final.write_videofile(str(output_path), codec='libx264', audio_codec='aac')

    return output_path

if start_btn and input_file:
    with st.spinner("Processing..."):
        out = process_video(input_file, hook, cta, brand, platform)
        st.video(str(out))
        with open(out, "rb") as f:
            st.download_button("Download Video", f, file_name=out.name)
