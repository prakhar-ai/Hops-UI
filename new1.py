from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import os
dirname = os.path.dirname(__file__)

resp = urlopen('https://drive.google.com/uc?export=download&id=1dWUye322dBFsER-O_2yni3z9vBjhcIHh')
zipfile = ZipFile(BytesIO(resp.read()))
    #print(zipfile.namelist())
studyid = '1'
outpath = '1'
print(outpath)
    # for name in zipfile.namelist():    
        # zipfile.extract(name, outpath)
media =os.path.join(dirname, 'media')
zipfile.extractall(os.path.join(media, '123'))