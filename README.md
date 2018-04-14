# imgck

Directly execute the convert command etc. in the environment where ImageMagick is installed

This works in 1 file simple substance without depending on the library

## How to use

place imgck.py at the same position as the source code

```python
# coding: utf-8

import os
import imgck

base_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base_dir, 'sample.jpg'), 'rb') as f:
    img = f.read()

i = imgck.Imgck(img)

print(i.width())
print(i.height())
print(i.exif('DateTimeOriginal'))

r = i.resize(300, 300)

with open('test-convert.jpg', 'wb') as o:
    o.write(r.get_blob())
```
