#-*- coding:utf-8 –*-
# %%
import configparser
import os
import re
import math
import cv2
import numpy as np
# cv2 don't support Chinese, so use PIL read and process pics
import PIL.Image as Image


class pic2video:
    def __init__(self):
        self.config = None
        self.cfg = None
        self.read_cfg()
        self.pics = []


    def read_cfg(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read('config.ini', encoding='utf-8')
        self.config = self.cfg['config']


    def read_pics(self, path, img_pattern = re.compile('.*\.{\'jpg\', \'jpeg\', \'png\'}')):
        pics = []
        files = os.listdir(path)
        for file in files:
            if os.path.isdir(file):
                child_dir_pics = self.read_pics(os.path.join(path, file), img_pattern)
                pics += child_dir_pics
            else:
                if re.match(img_pattern, file):
                    pics.append(Image.open(os.path.join(path, file)).resize((640, 480)))

        return pics


    def get_pics(self):
        # folder path
        path = self.config['path']
        return self.read_pics(path)

        
    def generate_video(self, type = 1):
        fps = int(self.config['fps'])
        pic_len = int(self.config['pic_len'])
        pic_wid = int(self.config['pic_wid'])
        video = None
        if self.config['save_path'] != '':
            video = cv2.VideoWriter(self.config['save_path'], -1, fps, (pic_len, pic_wid))
        else:
            video = cv2.VideoWriter('temp.mp4', -1, fps, (pic_len, pic_wid))
        pics = self.get_pics()
        if type == 1:
            for i in range(len(pics)):
                video.write(cv2.cvtColor(np.array(pics[i]), cv2.COLOR_RGB2BGR))
                # puzzle a big img with front pics
                rows = cols = math.ceil(math.sqrt(i + 1))
                big_img = Image.new('RGB', (rows * pic_len, cols * pic_wid))
                for r in range(rows):
                    for c in range(cols):
                        if r * cols + c >= len(pics):
                            break
                        big_img.paste((r * pic_len, c * pic_wid))

                big_img = cv2.cvtColor(np.array(big_img.resize((pic_len, pic_wid)), cv2.COLOR_RGB2BGR))
                video.write(big_img)

        video.release()
        return


# %%
if __name__ == "__main__":
    p2v = pic2video()
    p2v.generate_video()

