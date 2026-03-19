from PIL import Image
import numpy as np

def analyser_image(image):
    
    largeur, hauteur = image.size
    mode = image.mode
    
    # Convertir en RGB si nécessaire pour analyse
    if mode in ("RGBA", "P"):
        image = image.convert("RGB")
    
    img_np = np.array(image)
    
    # Moyenne des couleurs
    moy_r = np.mean(img_np[:,:,0])
    moy_g = np.mean(img_np[:,:,1])
    moy_b = np.mean(img_np[:,:,2])
    
    # Histogramme normalisé
    hist = image.histogram()
    hist = np.array(hist) / sum(hist)
    
    # Entropie (mesure de complexité)
    entropie = -np.sum(hist * np.log2(hist + 1e-9))
    
    return {
        "largeur": largeur,
        "hauteur": hauteur,
        "mode": mode,
        "moy_r": moy_r,
        "moy_g": moy_g,
        "moy_b": moy_b,
        "entropie": entropie
    }