import cv2
import numpy as np
from PIL import Image


class ConvertXBM:
    def __init__(self,img, size_w, size_h,pWidth=10, saveType=1):
        self.img = img
        self.size_w = size_w
        self.size_h = size_h
        self.pWidth = pWidth
        self.saveType = saveType

    def resiveByte(self, mybyte):
        res = 0
        for x in range(8):
            res <<= 1
            res |= (mybyte & 1)
            mybyte >>= 1
        return res

    def img2XBM(self,img, size_w, size_h, inv=0, pWidth=20, saveType=1):
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (size_w, size_h), interpolation=cv2.INTER_AREA)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        ret3,binary = cv2.threshold(gray,0,1,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        #ret, binary = cv2.threshold(blur, 127, 1, cv2.THRESH_BINARY)

        #binary = cv2.GaussianBlur(binary, (3, 3), 0)
        # kernel = np.ones((1, 1), np.uint8)
        # binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        img_width = binary.shape[1]
        img_height = binary.shape[0]
        current_bit = 0
        current_byte = 0
        xbm_list = []
        for j in range(img_height):
            add_bit = lambda x: 8 if (x % 8) == 0 else (x % 8)
            for i in range(img_width + (8 - add_bit(img_width))):
                if i < img_width:
                    current_byte += (binary[j][i] ^ inv)
                else:
                    current_byte += 0 ^ inv
                if current_bit < 7:
                    current_byte <<= 1
                current_bit += 1
                if current_bit == 8:
                    if saveType:
                        todo_byte = self.resiveByte(current_byte)
                    else:
                        todo_byte = current_byte

                    xbm_list.append("{0:#04X}".format(todo_byte))
                    current_bit = 0
                    current_byte = 0
        bufsize = len(xbm_list)
        res = '{'
        for index in range(len(xbm_list)):
            if (index % pWidth == 0):
                res += '\n'
            res += xbm_list[index]
            if (index < len(xbm_list) - 1):
                res += ','
        res += '}'
        return bufsize,res

    def gif2XBM(self,frame_start,frame_end,inv = 0):
        res = '{'
        for i in range(frame_start-1,frame_end):
            self.img.seek(i)
            new = Image.new("RGBA", self.img.size)
            new.paste(self.img)
            splitImg = cv2.cvtColor(np.asarray(new), cv2.COLOR_RGB2BGR)
            bufsize , tempres = self.img2XBM(splitImg, self.size_w, self.size_h, inv=inv)
            res += tempres
            if i < self.img.n_frames - 1:
                res += ',\n'
        res += '}'
        return frame_end-frame_start+1,bufsize,res

# # img = cv2.imread("C:/Users/Daybreak/Downloads/Compressed/heart/bubu.bmp")
# # img = cv2.imread("D:/timg.gif")
# # print(img)
# # cv2.imshow('img', img)
# # cv2.waitKey(0)
# img = Image.open("C:/Users/Daybreak/Downloads/ezgif.com-resize.gif")
# print(img.n_frames)
#
# print(gif2XBM(img,128,64))
# # print(img2XBM(img,128,64))
# # print(resiveByte(0x3e))
