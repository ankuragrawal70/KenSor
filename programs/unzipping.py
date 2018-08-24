import os
import zipfile,os.path
def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)

"""def unzip(source_filename,dirname):
    zfile = zipfile.ZipFile(source_filename)
    for name in zfile.namelist():
      (dirname, filename) = os.path.split(name)
      print "Decompressing " + filename + " on " + dirname
      if not os.path.exists(dirname):
        os.makedirs(dirname)
      zfile.extract(name, dirname)"""

"""def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)"""

    

dest="D://Thesis//data//2015_data//"
for filename in os.listdir("D://Thesis//data_gdelt//2015_data//"):
    print filename
    x="D://Thesis//data_gdelt//2015_data//"+filename
    unzip(x,dest)
    #fh = open(x,'rb')
    #z = zipfile.ZipFile(fh)

    #z.extract(dest)
    #for name in z.namelist():
        #outfile = open(name, 'wb')
        #outfile.write(dest+z.read(name))
        #outfile.close()
    #    z.extract(name,dest)
    #fh.close()
