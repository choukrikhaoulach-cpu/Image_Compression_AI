import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import mean_squared_error as mse

class EvaluationAgent:
    def evaluate(self, original_path, compressed_path):
        try:
            # Charger images
            original = cv2.imread(original_path)
            compressed = cv2.imread(compressed_path)

            if original is None or compressed is None:
                raise ValueError("Impossible de charger les images")

            # Redimensionner si tailles différentes
            if original.shape != compressed.shape:
                compressed = cv2.resize(compressed, (original.shape[1], original.shape[0]))

            # Convertir en grayscale pour certaines métriques
            original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            compressed_gray = cv2.cvtColor(compressed, cv2.COLOR_BGR2GRAY)

            # Calcul des métriques
            psnr_value = psnr(original_gray, compressed_gray)
            ssim_value = ssim(original_gray, compressed_gray)
            mse_value = mse(original_gray, compressed_gray)

            # Taille fichiers
            original_size = os.path.getsize(original_path)
            compressed_size = os.path.getsize(compressed_path)
            compression_ratio = (1 - (compressed_size / original_size)) * 100

            # Vérification qualité
            quality_status = "acceptable"
            if ssim_value < 0.85 or psnr_value < 30:
                quality_status = "low_quality"

            return {
                "status": "success",
                "metrics": {
                    "PSNR": round(psnr_value, 2),
                    "SSIM": round(ssim_value, 4),
                    "MSE": round(mse_value, 2),
                    "original_size_kb": round(original_size / 1024, 2),
                    "compressed_size_kb": round(compressed_size / 1024, 2),
                    "compression_ratio_percent": round(compression_ratio, 2)
                },
                "quality_status": quality_status
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}