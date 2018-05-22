import caffe
import surgery, score

import numpy as np
import os
import sys
from PIL import Image

try:
    import setproctitle
    setproctitle.setproctitle(os.path.basename(os.getcwd()))
except:
    pass


weights = '../cityscapes_iter_25000.caffemodel'

caffe.set_mode_gpu()

solver = caffe.SGDSolver('solver.prototxt')
solver.net.copy_from(weights)

# surgeries
interp_layers = [k for k in solver.net.params.keys() if 'up' in k]
surgery.interp(solver.net, interp_layers)

# scoring
val = np.loadtxt('eval_list/val.txt', dtype=str)

for _ in range(50):
    solver.step(4000)
    score.seg_tests(solver, False, val, layer='score')