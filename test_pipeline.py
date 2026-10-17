import os
import json
import numpy as np
from PIL import Image
from agents.orchestrator import Orchestrator
from agents.analyse import analyser_image

from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

# Dossiers
DATASET_PATH = "dataset"
RESULTS_PATH = "results"
COMPRESSED_PATH = os.path.join(RESULTS_PATH, "compressed")
REPORTS_PATH = os.path.join(RESULTS_PATH, "reports")

os.makedirs(COMPRESSED_PATH, exist_ok=True)
os.makedirs(REPORTS_PATH, exist_ok=True)

orch = Orchestrator()

global_stats = []

print("🚀 Début pipeline dataset...\n")

for filename in os.listdir(DATASET_PATH):

    try:
        print(f"Traitement : {filename}")

        path = os.path.join(DATASET_PATH, filename)

        image = Image.open(path).convert("RGB")

        # -----------------------
        # ANALYSE
        # -----------------------
        features = analyser_image(image)

        # -----------------------
        # DECISION IA
        # -----------------------
        decision = orch.llm.decide(features)

        # -----------------------
        # COMPRESSION
        # -----------------------
        base = filename.split(".")[0]
        compressed_path = os.path.join(COMPRESSED_PATH, f"{base}.jpg")

        image.save(compressed_path, "JPEG", quality=decision.get("quality", 80))

        # -----------------------
        # METRICS
        # -----------------------
        orig = np.array(image)
        comp = np.array(Image.open(compressed_path).convert("RGB"))

        if orig.shape != comp.shape:
            comp = np.array(Image.fromarray(comp).resize((orig.shape[1], orig.shape[0])))

        psnr_val = psnr(orig, comp)
        ssim_val = ssim(orig, comp, channel_axis=-1)

        original_size = os.path.getsize(path)
        compressed_size = os.path.getsize(compressed_path)

        compression_ratio = (1 - (compressed_size / original_size)) * 100

        # -----------------------
        # REPORT INDIVIDUEL
        # -----------------------
        report = {
            "image": filename,
            "decision": decision,
            "metrics": {
                "PSNR": round(psnr_val, 2),
                "SSIM": round(ssim_val, 4),
                "original_size_kb": round(original_size / 1024, 2),
                "compressed_size_kb": round(compressed_size / 1024, 2),
                "compression_ratio_percent": round(compression_ratio, 2)
            }
        }

        with open(os.path.join(REPORTS_PATH, f"{base}.json"), "w") as f:
            json.dump(report, f, indent=4)

        global_stats.append(report["metrics"])

    except Exception as e:
        print(f"❌ Erreur avec {filename} : {e}")

# -----------------------
# GLOBAL REPORT
# -----------------------

if global_stats:

    avg_psnr = np.mean([x["PSNR"] for x in global_stats])
    avg_ssim = np.mean([x["SSIM"] for x in global_stats])
    avg_compression = np.mean([x["compression_ratio_percent"] for x in global_stats])

    global_report = {
        "total_images": len(global_stats),
        "average_psnr": round(avg_psnr, 2),
        "average_ssim": round(avg_ssim, 4),
        "average_compression": round(avg_compression, 2)
    }

    with open(os.path.join(RESULTS_PATH, "global_report.json"), "w") as f:
        json.dump(global_report, f, indent=4)

print("\n🔥 Pipeline terminé !")