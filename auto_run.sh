#!/bin/bash

while true
do
    echo "🔄 Running IPTV Scanner..."
    python scanner.py
    
    echo "🚀 Pushing changes to GitHub..."
    git add livetv_channels.m3u
    git commit -m "🔄 Phone Auto-update: $(date)"
    git push origin main
    
    echo "😴 Sleeping for 12 hours..."
    sleep 43200
done