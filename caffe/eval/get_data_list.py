import os

data_path = os.path.join('..', '..', 'data')
for split in ['train', 'val']:
  img_train_path = os.path.join(data_path, 'leftImg8bit', split)

  img_train_list = [os.path.relpath(os.path.join(dp, f), start=data_path)
                    for dp, dn, filenames in os.walk(img_train_path)
                    for f in filenames if f.endswith('.png')]
  img_train_list.sort()

  label_train_path = os.path.join(data_path, 'gtFine', split)

  label_train_list = [os.path.relpath(os.path.join(dp, f), start=data_path)
                    for dp, dn, filenames in os.walk(label_train_path)
                    for f in filenames if f.endswith('labelTrainIds.png')]
  label_train_list.sort()

  f = open(os.path.join('eval_list', split + '.txt'), 'w')
  for i in range(0, len(img_train_list)):
    f.write(img_train_list[i] + ' ' + label_train_list[i] + '\n')






