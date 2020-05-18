# coding:utf-8
from base64 import b64decode, b64encode, b85decode, b85encode
from gzip import compress, decompress
def encrypt(source):
    try:
        one = source.encode('utf-8', 'ignore')
        two = compress(one)
        three = b64encode(two)
        four = compress(three)
        five = b85encode(four)
        six = compress(five)
        seven = b64encode(six).decode('utf-8', 'ignore')
        return seven
    except Exception as e:
        return '加密失败:' + str(e)


def decrypt(source):
    try:
        one = b64decode(source.encode('utf-8', 'ignore'))
        two = decompress(one)
        three = b85decode(two)
        four = decompress(three)
        five = b64decode(four)
        six = decompress(five)
        seven = six.decode('utf-8', 'ignore')
        return seven
    except Exception as e:
        return '解密失败:' + str(e)

