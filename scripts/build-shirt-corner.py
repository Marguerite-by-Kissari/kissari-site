"""M08: extend only the supplied shirt's rounded cut, preserving all upper pixels.
Original is untouched; the missing right-bottom fabric uses reflected source pixels.
"""
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
src=root/'static/images/Femme cheveux.png'
out=root/'static/images/Femme cheveux-angle-droit.png'
im=Image.open(src).convert('RGBA')
original=im.copy()
for y in range(900,im.height):
    sample_y=min(y,im.height-2)
    opaque=[x for x in range(im.width) if original.getpixel((x,sample_y))[3]==255]
    edge=max(opaque)
    for x in range(edge+1,im.width):
        reflected=max(min(2*edge-x-4,edge-4),100)
        pixel=original.getpixel((reflected,sample_y))
        assert pixel[3]==255
        im.putpixel((x,y),pixel)
im.save(out)
print(out)
