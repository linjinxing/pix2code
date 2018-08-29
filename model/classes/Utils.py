__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'

import numpy as np


class Utils:
    @staticmethod
    def sparsify(label_vector, output_size):
        sparse_vector = []

        for label in label_vector:
            sparse_label = np.zeros(output_size)
            sparse_label[label] = 1

            sparse_vector.append(sparse_label)

        return np.array(sparse_vector)

    @staticmethod
    def get_preprocessed_img(img_path, image_size):
        """ 因为opencv读入的图片矩阵数值是0到255，有时我们需要对其进行归一化为0~1  """
        import cv2
        img = cv2.imread(img_path)
        # Utils.show(img)
        # print(img.size)
        img = cv2.resize(img, (image_size, image_size))
        # print(img.size)
        Utils.show(img)
        img = img.astype('float32') # 注意需要先转化数据类型为float
        img /= 255 # 归一化为0~1
        return img

    @staticmethod
    def show(image):
        import cv2
        cv2.namedWindow("view", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("view", image)
        cv2.waitKey(0)
        cv2.destroyWindow("view")
