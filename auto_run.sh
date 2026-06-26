#!/bin/bash

while true
do
    echo "🔄 Starting Multi-IP TV Scanner..."
    python scanner.py
    
    echo "🚀 Pushing all playlists to GitHub..."
    # দুটো ফাইলকেই অ্যাড করা হচ্ছে 
    git add timetv_channels.m3u livetv_channels.m3u texas_tv_real.m3u
    
    git commit -m "🔄 Termux Auto-update: $(date)"
    git push origin main
    
    echo "😴 Done! Sleeping for 12 hours..."
    sleep 43200
done
