# %%
import cv2
import configparser
import os
import re


class pic2video:
    def __init__(self):
        self.cfg = self.read_cfg()
        self.pics = []


    def read_cfg(self):
        return dict(configparser.ConfigParser().read('config.ini', encoding='uft-8'))


    def read_pics(self, path, type_pattern = re.compile('*\.{\'jpg\', \'jpeg\', \'png\'}')):
        pics = []
        files = os.listdir(path)
        for file in files:
            if os.path.isdir(file):
                child_dir_pics = self.read_pics(file, type_pattern)
                pics += child_dir_pics
            else:
                if re.match(type_pattern, file):
                    pics.append(cv2.imread(file))

        return pics


    def get_pics(self):
        # folder path
        path = self.cfg['path']
        return self.read_pics(path)

        
    def generate_video(self):
        video = []
        pics = self.get_pics()

        if self.cfg['save_path'] != None:
            self.save(video)

        return


    def save(self, video):
        
        return


# %%
if __name__ == "__main__":
    p2v = pic2video()
    p2v.generate_video()


# %%
import re
a = re.compile('*123')
if re.match(a, 'vew123'):
    print(123)
else:
    print(789)
# %%
