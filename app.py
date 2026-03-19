import streamlit as st
from PIL import Image
import os
from agents.analyse import analyser_image
from agents.decision import prendre_decision
import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity

st.title("Compression d'images")

uploaded_file = st.file_uploader("Choisir une image")

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    # -----------------------
    # Analyse
    # -----------------------
    analyse = analyser_image(image)
    st.write("Analyse automatique :", analyse)

    decision = prendre_decision(analyse)
    st.write("Décision automatique :", decision)

    format_choice = decision["format"]
    quality = decision["quality"]

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    os.makedirs("compressed", exist_ok=True)

    # -----------------------
    # Sauvegarde originale
    # -----------------------
    original_path = os.path.join("compressed", "original_" + uploaded_file.name)
    image.save(original_path)

    # -----------------------
    # Resize intelligent (pour compression seulement)
    # -----------------------
    image_for_compression = image.copy()

    max_width = 1920
    if image_for_compression.width > max_width:
        ratio = max_width / image_for_compression.width
        new_height = int(image_for_compression.height * ratio)
        image_for_compression = image_for_compression.resize((max_width, new_height))
        st.info("Image redimensionnée automatiquement pour optimisation web.")

    # -----------------------
    # Sauvegarde compressée
    # -----------------------
    compressed_filename = f"compressed_{uploaded_file.name.split('.')[0]}.{format_choice.lower()}"
    compressed_path = os.path.join("compressed", compressed_filename)

    if format_choice == "JPEG":
        image_for_compression.save(compressed_path, "JPEG", quality=quality)

    elif format_choice == "PNG":
        image_for_compression.save(compressed_path, "PNG")

    elif format_choice == "WebP":
        image_for_compression.save(compressed_path, "WebP", quality=quality)

    # -----------------------
    # Calcul tailles
    # -----------------------
    taille_originale = len(uploaded_file.getvalue()) / 1024
    taille_compressee = os.path.getsize(compressed_path) / 1024

    # -----------------------
    # PSNR & SSIM
    # -----------------------
    original_np = np.array(Image.open(original_path))
    compressed_np = np.array(Image.open(compressed_path))

    if original_np.shape == compressed_np.shape:
        psnr_value = peak_signal_noise_ratio(original_np, compressed_np, data_range=255)
        ssim_value = structural_similarity(original_np, compressed_np, channel_axis=-1)
    else:
        psnr_value = None
        ssim_value = None

    # -----------------------
    # Décision intelligente
    # -----------------------
    if taille_compressee >= taille_originale:
        st.warning("⚠️ La compression augmente la taille. Image originale conservée.")
        final_path = original_path
    else:
        final_path = compressed_path

    taux = (1 - taille_compressee / taille_originale) * 100

    # -----------------------
    # Affichage
    # -----------------------
    st.subheader("Résultats")

    st.image(
        [original_path, final_path],
        caption=["Originale", "Résultat final"]
    )

    st.write(f"Taille originale : {taille_originale:.2f} KB")
    st.write(f"Taille compressée : {taille_compressee:.2f} KB")
    st.write(f"Taux de compression : {taux:.2f} %")

    if psnr_value is not None:
        st.write(f"PSNR : {psnr_value:.2f} dB")
        st.write(f"SSIM : {ssim_value:.4f}")
    else:
        st.write("PSNR / SSIM non calculables (dimensions différentes)")

    # -----------------------
    # Bouton téléchargement
    # -----------------------
    with open(final_path, "rb") as file:
        st.download_button(
            label="Télécharger l'image optimisée",
            data=file,
            file_name=os.path.basename(final_path),
            mime="image/jpeg"
        )