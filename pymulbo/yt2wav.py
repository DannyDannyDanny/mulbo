from __future__ import unicode_literals
import youtube_dl
import os

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '256',
    }],
}

link = input()
if len(link) > 30:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
