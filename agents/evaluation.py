import os
import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import mean_squared_error as mse

class EvaluationAgent:

    def evaluate(self, original_path, compressed_path):

        try:
            original = cv2.imread(original_path)
            compressed = cv2.imread(compressed_path)

            if original is None or compressed is None:
                raise ValueError("Erreur chargement image")

            if original.shape != compressed.shape:
                compressed = cv2.resize(compressed, (original.shape[1], original.shape[0]))

            original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            compressed_gray = cv2.cvtColor(compressed, cv2.COLOR_BGR2GRAY)

            return {
                "status": "success",
                "PSNR": round(psnr(original_gray, compressed_gray), 2),
                "SSIM": round(ssim(original_gray, compressed_gray), 4),
                "original_size_kb": round(os.path.getsize(original_path)/1024, 2),
                "compressed_size_kb": round(os.path.getsize(compressed_path)/1024, 2)
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}