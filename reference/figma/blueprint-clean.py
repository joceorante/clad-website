import sys, numpy as np
from PIL import Image, ImageFilter
src, out_dir = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGBA")
bg = Image.new("RGBA", im.size, (255,255,255,255)); bg.alpha_composite(im)
g = np.array(bg.convert("L")).astype(float)
dark = g < 140
# thick-stroke detector: pixels whose 3x3 neighbourhood is entirely dark (map linework is ~1px)
H, W = dark.shape
thick = np.zeros_like(dark)
for dy in (-1,0,1):
    for dx in (-1,0,1):
        pass
pad = np.pad(dark, 1)
win = np.ones_like(dark)
for dy in range(3):
    for dx in range(3):
        win &= pad[dy:dy+H, dx:dx+W]
thick = win.copy(); thick[425:, :] = False  # keep the scale bar
print("thick px", int(thick.sum()))
ys, xs = np.nonzero(thick)
print("thick bbox", xs.min(), ys.min(), xs.max(), ys.max())
# dilate thick by 3px to cover the full markup stroke, then erase from the map
m = Image.fromarray((thick*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))
mask = np.array(m) > 0
clean = g.copy(); clean[mask] = 255
Image.fromarray(clean.astype(np.uint8)).save(f"{out_dir}/map-clean.png")
Image.fromarray((mask*255).astype(np.uint8)).save(f"{out_dir}/markup-mask.png")
# bitmap for potrace: map lines black on white, threshold
Image.fromarray(((clean < 170)*0 + (clean >= 170)*255).astype(np.uint8)).convert("1").save(f"{out_dir}/map.pbm")
# column/row histograms of thick pixels to locate markup pieces
from collections import Counter
print("thick x hist (by 20px):", sorted(Counter((xs//20*20).tolist()).items()))
print("thick y hist (by 20px):", sorted(Counter((ys//20*20).tolist()).items()))
