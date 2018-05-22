import h5py, os
import caffe
import numpy as np
import sys
from PIL import Image

IMG_ROOT=os.path.join('..', '..', 'data')

SIZE = 224 # fixed size to all images
with open( os.path.join('eval_list', str(sys.argv[1]) + '.txt'), 'r' ) as T :
    lines = T.readlines()

X = np.zeros( (len(lines), 3, SIZE , SIZE ), dtype=np.float32 ) 
Y = np.zeros( (len(lines), 1, SIZE , SIZE ), dtype=np.uint8 )
for i,l in enumerate(lines):
    sp = l.split(' ')
    img = caffe.io.load_image( os.path.join(IMG_ROOT, sp[0]) )
    img = caffe.io.resize( img, (SIZE , SIZE , 3) ) # resize to fixed size
    label = Image.open( os.path.join(IMG_ROOT, sp[1].split()[0]))
    label = np.array(label, dtype=np.uint8)
    label = caffe.io.resize( label, (SIZE , SIZE , 1) )

    # you may apply other input transformations here...
    # Note that the transformation should take img from size-by-size-by-3 and transpose it to 3-by-size-by-size
    # for example
    transposed_img = img.transpose((2,0,1))[::-1,:,:] # RGB->BGR
    transposed_label = label.transpose((2,0,1))[::-1,:,:] # RGB->BGR
    X[i] = transposed_img
    Y[i] = transposed_label
    if i % 10 == 0:
        print i

with h5py.File(str(sys.argv[1]) + '.h5','w') as H:
    H.create_dataset( 'X', data=X ) # note the name X given to the dataset!
    H.create_dataset( 'Y', data=Y ) # note the name Y given to the dataset!
with open(sys.argv[1] + '_h5_list.txt','w') as L:
    L.write( '/tmp/cityscapes/' + str(sys.argv[1]) + '.h5' ) # list all h5 files you are going to use