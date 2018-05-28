import os

data_path = os.path.join('..', '..', 'data')
for split in ['train', 'val']:
  print(split)
  img_train_path = os.path.join(data_path, 'leftImg8bit', split)

  for dp, dn, filenames in os.walk(img_train_path):
    for f in filenames: 
      if f.endswith('.png'):
        print os.path.join('/home/deeplearning/studdocs/doronin_m/SemanticSegmentation/data/leftImg8bit/train', 
                           os.path.basename(dp), f)

  img_train_list = [os.path.join('/home/deeplearning/studdocs/doronin_m/SemanticSegmentation/data/leftImg8bit', split, os.path.basename(dp), f)
                    for dp, dn, filenames in os.walk(img_train_path)
                    for f in filenames if f.endswith('.png')]
  img_train_list.sort()

  label_train_path = os.path.join(data_path, 'gtFine', split)

  for dp, dn, filenames in os.walk(label_train_path):
    for f in filenames: 
      if f.endswith('labelIds.png'):
        os.path.join(dp, f)


  label_train_list = [os.path.join('/home/deeplearning/studdocs/doronin_m/SemanticSegmentation/data/gtFine', split, os.path.basename(dp), f)
                    for dp, dn, filenames in os.walk(label_train_path)
                    for f in filenames if f.endswith('labelIds.png')]
  label_train_list.sort()

  f = open(os.path.join('eval_list', split + '.txt'), 'w')
  for i in range(0, len(img_train_list)):
    f.write(img_train_list[i] + ' ' + label_train_list[i] + '\n')





