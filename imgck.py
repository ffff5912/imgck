# coding: utf-8

import imghdr
import subprocess

class Imgck(object):

    def __init__(self, blob=None):
        self.destroy()
        self._blob = blob
        self._identify()

    def get_blob(self):
        return self._blob

    def width(self):
        return self._size['width']
                
    def height(self):
        return self._size['height']

    def exif(self, key):
        return self._exif.get(key, None)

    def optimize(self):
        if imghdr.what(None,self._blob) == 'jpeg':
            cmd = 'convert - -sampling-factor 4:2:0 -strip -'
        else:
            cmd = 'convert - -strip -'
        
        outputs = self._execute(cmd)

        return Imgck(outputs)

    def resize(self, width, height, quality=0):
        option = ''
        if (quality):
            option += ' -quality %(quality)d' % {'quality': quality}

        cmd = 'convert - -resize %(width)dx%(height)d %(option)s -' % {'width': width, 'height': height, 'option': option}
        outputs = self._execute(cmd)

        return Imgck(outputs)

    def strip(self):
        cmd = 'convert - -strip -'
        outputs = self._execute(cmd)

        return Imgck(outputs)

    def destroy(self):
        self._blob = None
        self._size = {'width':0, 'height':0}
        self._exif = {}

    def _identify(self):
        cmd = 'identify -format "width:%w\nheight:%h\n%[exif:*]" -'
        outputs = self._execute(cmd)
        output = outputs.decode('utf-8')

        for profiles in output.split('\n'):
            profile = profiles.strip().split(':', maxsplit=1)
            if self._has_profile(profile) == False:
                continue
            
            if profile[0] in self._size:
                self._size[profile[0]] = int(profile[1])
                continue

            exif_pair = profile[1].split('=', maxsplit=1)
            self._exif[exif_pair[0]] = exif_pair[1]
    
    def _has_profile(self, profile):
        return len(profile) >= 2

    def _execute(self, cmd): 
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True
        )

        outputs, errors = proc.communicate(self._blob)

        return outputs