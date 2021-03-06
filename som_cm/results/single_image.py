# -*- coding: utf-8 -*-
## @package som_cm.results.som_single_image
#
#  Demo for single image.
#  @author      tody
#  @date        2015/08/31

import os
import numpy as np
import matplotlib.pyplot as plt
from som_cm.core.color_pixels import ColorPixels
from mpl_toolkits.mplot3d import Axes3D


from som_cm.io_util.image import loadRGB
from som_cm.results.resu import batchResults, resultFile
from som_cm.core.hist_3d import Hist3D
from som_cm.core.som import SOMParam, SOM, SOMPlot

## Setup SOM in 1D and 2D for the target image.
def setupSOM(image, random_seed=100, num_samples=2000):
    np.random.seed(random_seed)

    hist3D = Hist3D(image, num_bins=16)
    # 为了灰度化而生成流形，所以不需要采用hist3D.colorCoordinates()
    # samples = hist3D.colorCoordinates()

    samples = hist3D._pixels
    print len(hist3D._pixels)

    # 删除白色像素点
    # bl=samples==[255,255,255]
    # bl=np.any(bl,axis=1)
    # ind=np.nonzero(bl)[0]
    # samples = np.delete(samples,ind,axis=0)
    # print len(samples)
    #
    # bl=samples==[254,255,255]
    # bl=np.any(bl,axis=1)
    # ind=np.nonzero(bl)[0]
    # samples = np.delete(samples,ind,axis=0)


    #1000
    print len(samples)

    param1D = SOMParam(h=64, dimension=1)
    som1D = SOM(samples, param1D)

    param2D = SOMParam(h=16, dimension=2)
    som2D = SOM(samples, param2D)
    return som1D, som2D


## Demo for the single image file.
def singleImageResult(image_file):
    print image_file
    image_name = os.path.basename(image_file)
    image_name = os.path.splitext(image_name)[0]

    image = loadRGB(image_file)
    import time
    start = time.time()

    som1D, som2D = setupSOM(image)

    fig = plt.figure(figsize=(12, 10))
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.9, wspace=0.1, hspace=0.2)

    print time.time() - start
    font_size = 15
    fig.suptitle("SOM-Color Manifolds for Single Image", fontsize=font_size)

    plt.subplot(331)
    h, w = image.shape[:2]
    plt.title("Original Image: %s x %s" % (w, h), fontsize=font_size)
    plt.imshow(image)
    plt.axis('off')

    print "  - Train 1D"
    som1D.trainAll()

    print "  - Train 2D"
    som2D.trainAll()

    som1D_plot = SOMPlot(som1D)
    som2D_plot = SOMPlot(som2D)
    plt.subplot(332)
    plt.title("SOM 1D", fontsize=font_size)
    # 如果改变updateImage函数的返回值，那么可以用以下语句，代替以下第二行语句。
    # plt.imshow(som1D_plot.updateImage())
    som1D_plot.updateImage()
    plt.axis('off')

    plt.subplot(333)
    plt.title("SOM 2D", fontsize=font_size)
    som2D_plot.updateImage()
    plt.axis('off')


    color_pixels = ColorPixels(image)
    pixels = color_pixels.pixels(color_space="rgb")
    ax = fig.add_subplot(334, projection='3d')
    plt.title("cloudPoint", fontsize=font_size)
    som1D_plot.plotCloud(ax, pixels)

    hist3D = Hist3D(image, num_bins=16)
    color_samples = hist3D.colorCoordinates()
    ax = fig.add_subplot(337, projection='3d')
    plt.title("cloudPoint", fontsize=font_size)
    som1D_plot.plotCloud(ax, color_samples)


    ax1D = fig.add_subplot(335, projection='3d')
    plt.title("1D in 3D", fontsize=font_size)
    som1D_plot.plot3D(ax1D)

    ax2D = fig.add_subplot(336, projection='3d')
    plt.title("2D in 3D", fontsize=font_size)
    som2D_plot.plot3D(ax2D)

    plt.subplot(338)
    plt.title("Gray", fontsize=font_size)

    # 如果改变updateImage函数的返回值，那么可以用以下语句，代替以下第二行语句。
    a,b = som2D_plot.showGrayImage2(image)

    plt.imshow(a, cmap='gray', vmin = 0, vmax = 1)
    plt.axis('off')
    plt.imsave('''./''' + image_name + '''.png''', a, cmap='gray',vmin = 0, vmax = 1)
    plt.imsave('''./''' + image_name + '''!.png''', b, cmap='gray',vmin = 0, vmax = 1)


    plt.subplot(339)
    plt.title("Gray", fontsize=font_size)
    plt.imshow(b, cmap='gray', vmin = 0, vmax = 1)
    plt.axis('off')

    result_file = resultFile("%s_single" % image_name)
    plt.savefig(result_file)
    #showMaximize()


## Demo for the given data names, ids.
def singleImageResults(data_names, data_ids):
    batchResults(data_names, data_ids, singleImageResult, "SOM (single image)")

if __name__ == '__main__':
    data_names = ["apple"]
    data_ids = range(9)

    singleImageResults(data_names, data_ids)