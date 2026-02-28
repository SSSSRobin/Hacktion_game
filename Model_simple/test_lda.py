import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Model_simple.csp_lda import CSPLDA, load_edf
import numpy as np

# communication UDP
import socket
import numpy as np
from Model_simple.csp_lda import CSPLDA, load_edf

print("Current dir:", os.getcwd())
print("Files:", os.listdir())
# Charger le modele
model = CSPLDA.load("Model_simple/model_0010.pkl")
X_new, y_new, _, sf = load_edf("0010.edf")

"""
# Predire sur de nouvelles donnees
predictions = model.predict(X_new)   # ['left_hand', 'right_hand', ...]
accuracy    = model.score(X_new, y_new)
print("accuracy", accuracy)
"""

###### Test sur 1 sample ######

# Prendre le premier trial comme exemple
"""
duration = 1
idx = int(duration * sf)
sample_3s = X_new[0,:,:idx]          # shape (7, 250) — 7 canaux x 3s @ 256Hz

# Ajouter la dimension batch (1, 7, 250)
proba = model.predict_proba(sample_3s[np.newaxis])   # shape (1, 2)
prediction = model.predict(sample_3s[np.newaxis])

label = prediction[0]
confidence = proba[0].max() * 100
print("Predict sur 1 trial",prediction[0])    
print(f"Prediction: {label}  ({confidence:.1f}%)")
"""


IP = "127.0.0.1"
PORT = 5005

# Mapping label -> valeur UDP
LABEL_MAP = {"left_hand": -1, "right_hand": 1}

def main():
    model = CSPLDA.load("model_0010.pkl")
    duration = 1          # secondes
    sf       = 256        # Hz
    idx      = int(duration * sf)   # = 256 points
    X_new = np.random.randn(1, 7, idx)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[BCI] Envoi UDP vers {IP}:{PORT}")

    try:
        for i, sample in enumerate(X_new):
            prediction = model.predict(sample[np.newaxis])[0]
            proba = model.predict_proba(sample[np.newaxis])[0].max()

            valeur = LABEL_MAP[prediction]
            msg = str(valeur).encode("utf-8")
            sock.sendto(msg, (IP, PORT))

            print(f"[BCI] Trial {i+1}: {prediction} -> {valeur}  ({proba*100:.1f}%)")

    except KeyboardInterrupt:
        print("\n[BCI] arrêté.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()




