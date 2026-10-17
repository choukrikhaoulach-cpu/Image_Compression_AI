import streamlit as st
from PIL import Image
import os
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as compare_psnr
from skimage.metrics import structural_similarity as compare_ssim

from agents.orchestrator import Orchestrator
from agents.analyse import analyser_image  # ✅ IMPORTANT

st.title("🧠 Compression d’images intelligente (IA Multi-Agents)")

uploaded_file = st.file_uploader("📤 Upload une image")

if uploaded_file is not None:

    orch = Orchestrator()

    image = Image.open(uploaded_file)

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    os.makedirs("web_results", exist_ok=True)

    original_path = os.path.join("web_results", "original_" + uploaded_file.name)
    image.save(original_path)

    # -----------------------
    # REDIMENSIONNEMENT
    # -----------------------
    max_width = 1280
    if image.width > max_width:
        ratio = max_width / image.width
        new_height = int(image.height * ratio)
        image = image.resize((max_width, new_height))
        st.info("📉 Image redimensionnée pour meilleure compression")

    # -----------------------
    # MULTI-COMPRESSION
    # -----------------------
    def compress_image(img, decision=None):
        filename = uploaded_file.name.split(".")[0]
        paths = []

        path1 = os.path.join("web_results", f"{filename}_q85.jpg")
        img.save(path1, "JPEG", quality=85)
        paths.append(path1)

        path2 = os.path.join("web_results", f"{filename}_q40.jpg")
        img.save(path2, "JPEG", quality=40, optimize=True)
        paths.append(path2)

        path3 = os.path.join("web_results", f"{filename}.webp")
        img.save(path3, "WEBP", quality=60)
        paths.append(path3)

        path4 = os.path.join("web_results", f"{filename}.png")
        img.save(path4, "PNG")
        paths.append(path4)

        best_path = min(paths, key=lambda p: os.path.getsize(p))
        return best_path

    # -----------------------
    # PIPELINE AVEC PROGRESS
    # -----------------------
    progress = st.progress(0)
    status = st.empty()

    # 1. ANALYSE
    status.text("🔍 Analyse de l'image...")
    progress.progress(10)
    features = analyser_image(image)

    # 2. DECISION IA
    status.text("🤖 Prise de décision IA...")
    progress.progress(40)
    decision = orch.llm.decide(features)

    # 3. COMPRESSION
    status.text("🗜️ Compression en cours...")
    progress.progress(70)
    final_path = compress_image(image, decision)

    # 4. FIN
    progress.progress(100)
    status.text("✅ Terminé !")

    # -----------------------
    # CALCUL METRICS
    # -----------------------
    def calc_metrics(orig_path, comp_path):
        orig_img = Image.open(orig_path).convert("RGB")
        comp_img = Image.open(comp_path).convert("RGB")

        if orig_img.size != comp_img.size:
            comp_img = comp_img.resize(orig_img.size)

        orig_np = np.array(orig_img)
        comp_np = np.array(comp_img)

        psnr = compare_psnr(orig_np, comp_np)
        ssim = compare_ssim(orig_np, comp_np, channel_axis=-1)
        mse = np.mean((orig_np - comp_np) ** 2)

        return {
            "PSNR": round(psnr, 2),
            "SSIM": round(ssim, 4),
            "MSE": round(mse, 2),
            "original_size_kb": round(os.path.getsize(orig_path) / 1024, 2),
            "compressed_size_kb": round(os.path.getsize(comp_path) / 1024, 2),
            "status": "success"
        }

    metrics = calc_metrics(original_path, final_path)

    # -----------------------
    # AFFICHAGE
    # -----------------------
    st.subheader("📊 Analyse de l’image")
    st.json(features)

    st.subheader("🤖 Décision IA")
    st.json(decision)

    st.subheader("📉 Résultats")

    st.image(
        [original_path, final_path],
        caption=["Originale", "Optimisée"]
    )

    if metrics["status"] == "success":
        st.write(f"📏 PSNR : {metrics['PSNR']} dB")
        st.write(f"📊 SSIM : {metrics['SSIM']}")
        st.write(f"📉 MSE : {metrics['MSE']}")
        st.write(f"📦 Taille originale : {metrics['original_size_kb']} KB")
        st.write(f"📦 Taille compressée : {metrics['compressed_size_kb']} KB")

    # -----------------------
    # DOWNLOAD
    # -----------------------
    if os.path.exists(final_path):
        with open(final_path, "rb") as file:
            st.download_button(
                label="⬇️ Télécharger l’image optimisée",
                data=file,
                file_name=os.path.basename(final_path),
                mime="image/jpeg"
            )