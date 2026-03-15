 #!/usr/bin/env python3
"""
Portfolio image optimizer — run this once from your nathanlane-portfolio folder.
Converts large PNGs to WebP and GIF to MP4.

Requirements:
  pip install Pillow        (for WebP conversion)
  brew install ffmpeg       (for GIF → MP4)

Run with:
  cd ~/Desktop/nathanlane-portfolio   (or wherever your folder is)
  python3 convert-images.py
"""

import os, sys, subprocess, shutil

IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'images')

PNG_FILES = [
    'neon-ticketmaster.png',
    'sg-storytelling.png',
    'sg-bts.png',
    'tiktok-analytics-1.png',
    'tiktok-analytics-2.png',
    'sg-overview.png',
    'canva-icon.png',
    'sg-title.png',
    'ig-analytics-views.png',
    'ig-analytics-interactions.png',
]

GIF_FILE = 'neon-night-ad.gif'
MP4_FILE = 'neon-night-ad.mp4'


def convert_pngs():
    try:
        from PIL import Image
    except ImportError:
        print("❌  Pillow not found. Run:  pip install Pillow")
        return

    for filename in PNG_FILES:
        src = os.path.join(IMAGES_DIR, filename)
        dst = os.path.join(IMAGES_DIR, filename.replace('.png', '.webp'))
        if not os.path.exists(src):
            print(f"⚠️   Not found, skipping: {filename}")
            continue
        if os.path.exists(dst):
            print(f"✅  Already converted: {filename}")
            continue
        img = Image.open(src)
        img.save(dst, 'WEBP', quality=88, method=6)
        before = os.path.getsize(src)
        after = os.path.getsize(dst)
        pct = round((1 - after / before) * 100)
        print(f"✅  {filename} → .webp  ({round(before/1024)}KB → {round(after/1024)}KB, -{pct}% smaller)")


def convert_gif():
    src = os.path.join(IMAGES_DIR, GIF_FILE)
    dst = os.path.join(IMAGES_DIR, MP4_FILE)

    if not os.path.exists(src):
        print(f"⚠️   {GIF_FILE} not found, skipping.")
        return
    if os.path.exists(dst):
        print(f"✅  {MP4_FILE} already exists.")
        return

    if not shutil.which('ffmpeg'):
        print("❌  ffmpeg not found. Run:  brew install ffmpeg")
        print(f"    Then re-run this script, or convert {GIF_FILE} manually at ezgif.com/gif-to-mp4")
        return

    cmd = [
        'ffmpeg', '-i', src,
        '-movflags', 'faststart',
        '-pix_fmt', 'yuv420p',
        '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
        '-crf', '22',
        dst, '-y'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        before = os.path.getsize(src)
        after = os.path.getsize(dst)
        pct = round((1 - after / before) * 100)
        print(f"✅  {GIF_FILE} → .mp4  ({round(before/1024/1024, 1)}MB → {round(after/1024)}KB, -{pct}% smaller)")
    else:
        print(f"❌  ffmpeg failed: {result.stderr[-300:]}")


if __name__ == '__main__':
    print("\n🔧  Portfolio image optimizer\n")
    print("Converting PNGs → WebP...")
    convert_pngs()
    print("\nConverting GIF → MP4...")
    convert_gif()
    print("\nDone! Refresh your browser with Cmd+Shift+R.\n")
