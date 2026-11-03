"""zoomd.py FRAME_DIR OUT.png N1 N2 ...: 2x zooms (top screen) of the given shots, 4 per row. N = the number
printed on the contact sheet / clipcheck output (opens f_{N+1:03d}.png)."""
import os
import sys
from PIL import Image
d, out, fr = sys.argv[1], sys.argv[2], [int(a) for a in sys.argv[3:]]
ims=[Image.open(os.path.join(d, 'f_%03d.png' % (f + 1))).crop((0,0,256,192)).resize((320,240),Image.NEAREST) for f in fr]
cols=4; rows=(len(ims)+3)//4
s=Image.new('RGB',(322*cols,242*rows)); [s.paste(im,((i%cols)*322,(i//cols)*242)) for i,im in enumerate(ims)]; s.save(out)
