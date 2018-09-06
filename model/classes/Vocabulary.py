__author__ = 'Tony Beltramelli - www.tonybeltramelli.com'

import sys
import numpy as np

START_TOKEN = "<START>"
END_TOKEN = "<END>"
PLACEHOLDER = " "
SEPARATOR = '->'


class Vocabulary:
    def __init__(self):
        # 每个token所在的位置，表示成数组的方式，也即向量的方式
        self.binary_vocabulary = {}
        # 每个token所在的位置，key是token，value是索引
        self.vocabulary = {}
        # 每个token所在的位置，对应是什么token，key是索引，value是token
        self.token_lookup = {}
        self.size = 0

        self.append(START_TOKEN)
        self.append(END_TOKEN)
        self.append(PLACEHOLDER)

    def append(self, token):
        if token not in self.vocabulary:
            self.vocabulary[token] = self.size
            self.token_lookup[self.size] = token
            print("token:%s, size:%d" % (token, self.size))
            self.size += 1


    def create_binary_representation(self):
        if sys.version_info >= (3,):
            items = self.vocabulary.items()
        else:
            items = self.vocabulary.iteritems()
        for key, value in items:
            # 返回来一个给定形状和类型的用0填充的数组
            binary = np.zeros(self.size)
            binary[value] = 1
            self.binary_vocabulary[key] = binary
        print('self.vocabulary:%r' % self.vocabulary)
        print('self.token_lookup:%r' % self.token_lookup)
        print('self.binary_vocabulary:%r' % self.binary_vocabulary)

    def get_serialized_binary_representation(self):
        if len(self.binary_vocabulary) == 0:
            self.create_binary_representation()

        string = ""
        if sys.version_info >= (3,):
            items = self.binary_vocabulary.items()
        else:
            items = self.binary_vocabulary.iteritems()
        for key, value in items:
            array_as_string = np.array2string(value, separator=',', max_line_width=self.size * self.size)
            string += "{}{}{}\n".format(key, SEPARATOR, array_as_string[1:len(array_as_string) - 1])
        return string

    def save(self, path):
        output_file_name = "{}/words.vocab".format(path)
        output_file = open(output_file_name, 'w')
        output_file.write(self.get_serialized_binary_representation())
        output_file.close()

    def retrieve(self, path):
        input_file = open("{}/words.vocab".format(path), 'r')
        buffer = ""
        for line in input_file:
            try:
                separator_position = len(buffer) + line.index(SEPARATOR)
                buffer += line
                key = buffer[:separator_position]
                value = buffer[separator_position + len(SEPARATOR):]
                value = np.fromstring(value, sep=',')

                self.binary_vocabulary[key] = value
                self.vocabulary[key] = np.where(value == 1)[0][0]
                self.token_lookup[np.where(value == 1)[0][0]] = key

                buffer = ""
            except ValueError:
                buffer += line
        input_file.close()
        self.size = len(self.vocabulary)
