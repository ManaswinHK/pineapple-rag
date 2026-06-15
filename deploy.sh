#!/bin/bash

echo "===================================================="
echo "  Agritech RAG Dashboard - Automated Deployment"
echo "===================================================="
echo ""

if command -v nvidia-smi &> /dev/null; then
    echo "[OK] NVIDIA GPU detected! 🚀"
    echo "Routing AI workloads to the GPU for maximum speed..."
    docker-compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
else
    echo "[INFO] No NVIDIA GPU detected."
    echo "Defaulting to CPU mode. This is slightly slower but perfectly fine..."
    docker-compose -f docker-compose.yml up -d
fi

echo ""
echo "===================================================="
echo "✅ Deployment initiated!"
echo "The dashboard will be available at: http://127.0.0.1:8080/"
echo "(Note: It may take a few minutes on the first run to download the AI models)"
echo "===================================================="
