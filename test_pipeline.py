import os
from agents.orchestrator import Orchestrator
from PIL import Image

orch = Orchestrator()

dataset_path = "dataset"
results = []

for category in os.listdir(dataset_path):
    folder = os.path.join(dataset_path, category)

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        try:
            image = Image.open(path)

            result = orch.run(
                image=image,
                original_path=path,
                compressed_path_func=lambda d: path  # temporaire
            )

            results.append(result)

        except:
            print("Erreur :", file)

print("Tests terminés :", len(results))