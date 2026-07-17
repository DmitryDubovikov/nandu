#!/usr/bin/env bash
# Download Ñandú / OMA problem PDFs from Google Drive via gdown.
# Each file is independent: on failure we log and continue.
set -u
source venv/bin/activate

declare -a NAMES IDS DESTS

add() { NAMES+=("$1"); IDS+=("$2"); DESTS+=("$3"); }

# === Historico (Nivel 1, all stages) ===
add Escolares_N1       0B-7eAD5s2YQSQ09DNlpvNUNvOE0 nandu_problemas/historico/Escolares_N1.pdf
add Interescolares_N1  0B-7eAD5s2YQSVUdrc0RYT0tzdXc nandu_problemas/historico/Interescolares_N1.pdf
add Zonales_N1         0B-7eAD5s2YQSaWFOb1h6WjZSS2s nandu_problemas/historico/Zonales_N1.pdf
add Provinciales_N1    0B-7eAD5s2YQSSHN4em1XSk56NkU nandu_problemas/historico/Provinciales_N1.pdf
add Regionales_N1      0B-7eAD5s2YQSTTdLSk5TSjh5Tlk nandu_problemas/historico/Regionales_N1.pdf
add Nacionales_N1      0B-7eAD5s2YQSTWhFZ2sxMk9kZ2s nandu_problemas/historico/Nacionales_N1.pdf

# === 2025 ===
add 2025_Colegial_N1      1CDfpzlFnxhWXlPNiSG4HKFeAPprLm2XR nandu_problemas/2025/2025_Colegial_N1.pdf
add 2025_Intercolegial_N1 13jJEBjUPrW5ag-ik2PZLzJvPG7KWljGu nandu_problemas/2025/2025_Intercolegial_N1.pdf
add 2025_Zonal_N1         1FU3EYWJbMijEKDrJhiIMiq-5vDJCvYwg nandu_problemas/2025/2025_Zonal_N1.pdf
add 2025_Provincial_N1    1hn21tXDZmpsb3XO70BvxbM-Gcj0WYD2v nandu_problemas/2025/2025_Provincial_N1.pdf
add 2025_Regional_N1      1EVEsMZwXsYs1_7SP0NYOZ2jQkqcmjSKU nandu_problemas/2025/2025_Regional_N1.pdf
add 2025_Nacional_N1      1e0Yz6_Yt7VDD_NeD084ZGqC0PCx-svXD nandu_problemas/2025/2025_Nacional_N1.pdf

n=${#NAMES[@]}
for ((i=0; i<n; i++)); do
  name="${NAMES[$i]}"; id="${IDS[$i]}"; dest="${DESTS[$i]}"
  echo "=========================================================="
  echo ">>> [$((i+1))/$n] $name  (id=$id)"
  rm -f "$dest"
  gdown "https://drive.google.com/uc?id=${id}" -O "$dest" 2>&1
  rc=$?
  if [[ $rc -ne 0 || ! -s "$dest" ]]; then
    echo "!!! gdown uc form failed (rc=$rc), trying --fuzzy..."
    gdown --fuzzy "https://drive.google.com/file/d/${id}/view" -O "$dest" 2>&1
    rc=$?
  fi
  if [[ $rc -ne 0 || ! -s "$dest" ]]; then
    echo "XXX FAILED: $name"
  fi
done
echo "=========================================================="
echo "DONE"
