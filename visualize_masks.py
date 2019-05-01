# takes different masks generated by different versions/runs of deepcell and compares them

import numpy as np
import os
import skimage.io as io
import copy

base_dir = '/Users/noahgreenwald/Documents/Grad_School/Lab/Segmentation_Project/Contours/First_Run/'
image_dir = base_dir + 'cnn_data/Deepcell_docker/output/190428_epoch_test/'
# image_dir = base_dir + '/cnn_data/Deepcell_gcloud/Point1_12_18_23_3X/'
plot_dir = base_dir + '/Figs/'

files = os.listdir(image_dir)
files = [file for file in files if 'npy' in file]
files = [file for file in files if 'sample' not in file]
data = np.zeros((len(files), 4, 1024, 1024, 4), dtype='float32')

# axes on data: training run, image, x_dim, y_dim, output_mask
for i in range(len(files)):
    data[i, :, :, :, :] = np.load(os.path.join(image_dir, files[i]))

# save images back to folder for viewing
names = files
names = [x.replace('Point1_12_18_3X_', '').replace('_metrics.npy', '') for x in names]
for i in range(len(files)):
    io.imsave(os.path.join(image_dir, names[i] + '_nucleus.tiff'), data[i, 3, :, :, 2])
    io.imsave(os.path.join(image_dir, names[i] + '_border.tiff'), data[i, 3, :, :, 1])


# watershed version
files = os.listdir(image_dir)
files = [file for file in files if 'npy' in file]
files = [file for file in files if 'sample' in file]
data = np.zeros((len(files), 4, 1024, 1024, 4), dtype='float32')

# axes on data: training run, image, x_dim, y_dim, output_mask
for i in range(len(files)):
    data[i, :, :, :, :] = np.load(os.path.join(image_dir, files[i]))

argmax_images = []
for i in range(data.shape[0]):
    argmax_images.append(np.argmax(data[i], axis=-1))
argmax_images = np.array(argmax_images)
argmax_images = np.expand_dims(argmax_images, axis=-1)

# save images back to folder for viewing
names = files
names = [x.replace('Point1_12_18_23_', '').replace('_metrics.npy', '') for x in names]
for i in range(len(files)):
    io.imsave(os.path.join(image_dir, names[i] + '_nucleus.tiff'), data[i, 3, :, :, 2])

io.imshow(data[8, 3, :, :, 1])
io.imsave(plot_dir + 'test_image.tiff', x)

temp = copy.copy(data[5, 3, :, :, 1])
io.imshow(temp)
temp[temp < 0.4] = 0
io.imshow(temp)

# io.imsave(plot_dir + "interior_border_border_20_minus_5.tiff", data[6, 3, :, :, 1] - data[8, 3, :, :, 1])
io.imshow(data[6, 3, :, :, 1] - data[8, 3, :, :, 1])

io.imshow(data[4, 3, :, :, 1] - data[5, 3, :, :, 1])





# figure out watershed
test_images = np.load(image_dir + files[2])
argmax_images = []
for i in range(test_images.shape[0]):
    argmax_images.append(np.argmax(test_images[i], axis=-1))
argmax_images = np.array(argmax_images)
argmax_images = np.expand_dims(argmax_images, axis=-1)

print('watershed argmax shape:', argmax_images.shape)

#threshold = 0.9

#fg_thresh = test_images_fgbg[..., 1] > threshold

#fg_thresh = np.expand_dims(fg_thresh, axis=-1)
argmax_images_post_fgbg = argmax_images

from skimage.measure import label
from skimage.morphology import watershed
from skimage.feature import peak_local_max

watershed_images = []
for i in range(argmax_images_post_fgbg.shape[0]):
    image = argmax_images_post_fgbg[i, ..., 0] > 0
    distance = argmax_images_post_fgbg[i, ..., 0]

    local_maxi = peak_local_max(test_images[i, ..., -1],
                                min_distance=5,
                                exclude_border=False,
                                indices=False,
                                labels=image)

    markers = label(local_maxi)
    segments = watershed(-distance, markers, mask=image)
    watershed_images.append(segments)

watershed_images = np.array(watershed_images)
watershed_images = np.expand_dims(watershed_images, axis=-1)

