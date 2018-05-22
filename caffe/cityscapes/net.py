import caffe
import os
from caffe import layers as L, params as P
from caffe.coord_map import crop

def conv_relu(bottom, nout=16, ks=3, stride=1, pad=1, group=1):
    conv = L.Convolution(bottom, kernel_size=ks, stride=stride, group=group,
        num_output=nout, pad=pad, weight_filler=dict(type='xavier'), bias_filler=dict(type='constant'))
    return conv, L.ReLU(conv, in_place=True)

def max_pool(bottom, ks=2, stride=2):
    return L.Pooling(bottom, pool=P.Pooling.MAX, kernel_size=ks, stride=stride)

def fcn(split):
    n = caffe.NetSpec()
    pydata_params = dict(split=split, seed=1337)
    pydata_params['source'] = os.path.join('eval_list')
    pydata_params['root_folder'] = os.path.join('..', '..', 'data')
    pydata_params['batch_size'] = 2
    # pydata_params['scale'] = (0.0078125,0.0078125,0.0078125)
    # pydata_params['mean_value'] = (104.007/255, 116.669/255, 122.679/255)
    pydata_params['new_height'] = 512
    pydata_params['new_width'] = 512
    if split == 'train':
        pydata_params['mirror'] = True
        pydata_params['suffle'] = True

    pylayer_train = 'CityscapesDataLayer'
    n.data, n.label = L.Python(module='cityscapes_data_layer2', layer=pylayer_train,
            ntop=2, param_str=str(pydata_params))

    # the base net
    n.conv1, n.relu1 = conv_relu(n.data, ks=11, nout=96, stride=4, pad=100)
    n.pool1 = max_pool(n.relu1, 3, stride=2)
    n.norm1 = L.LRN(n.pool1, local_size=5, alpha=1e-4, beta=0.75)
    n.conv2, n.relu2 = conv_relu(n.norm1, ks=5, nout=256, pad=2, group=2)
    n.pool2 = max_pool(n.relu2, 3, stride=2)
    n.norm2 = L.LRN(n.pool2, local_size=5, alpha=1e-4, beta=0.75)
    n.conv3, n.relu3 = conv_relu(n.norm2, ks=3, nout=384, pad=1)
    n.conv4, n.relu4 = conv_relu(n.relu3, ks=3, nout=384, pad=1, group=2)
    n.conv5, n.relu5 = conv_relu(n.relu4, ks=3, nout=256, pad=1, group=2)
    n.pool5 = max_pool(n.relu5, 3, stride=2)

    # fully conv
    n.fc6, n.relu6 = conv_relu(n.pool5, ks=6, nout=4096)
    n.drop6 = L.Dropout(n.relu6, dropout_ratio=0.5, in_place=True)
    n.fc7, n.relu7 = conv_relu(n.drop6, ks=1, nout=4096)
    n.drop7 = L.Dropout(n.relu7, dropout_ratio=0.5, in_place=True)

    n.score_fr = L.Convolution(n.drop7, num_output=30, kernel_size=1, pad=0,
        weight_filler=dict(type='xavier'), bias_filler=dict(type='constant'),
        param=[dict(lr_mult=1, decay_mult=1), dict(lr_mult=2, decay_mult=0)])
    n.upscore = L.Deconvolution(n.score_fr,
        convolution_param=dict(num_output=30, kernel_size=63, stride=32,
            bias_term=False, weight_filler=dict(type='xavier'), bias_filler=dict(type='constant')),
        param=[dict(lr_mult=0)])
    n.score = crop(n.upscore, n.data)
    n.loss = L.SoftmaxWithLoss(n.score, n.label,
            loss_param=dict(normalize=True, ignore_label=255))

    n.accuracy = L.Accuracy(n.score, n.label)
    return n.to_proto()

def make_net():
    with open('train.prototxt', 'w') as f:
        f.write(str(fcn('train')))
    with open('val.prototxt', 'w') as f:
        f.write(str(fcn('val')))

if __name__ == '__main__':
    make_net()
