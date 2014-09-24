#!c:/Python27/python.exe
import zipfile
import os
import subprocess

ZIP_FILE = "Apache24-win64.zip"

# Get base_dir
currentDir = os.path.dirname(os.path.realpath(__file__))

BASE_DIR = currentDir[0:currentDir.find('grooveproject')].replace('\\', '/')

zfile = zipfile.ZipFile(ZIP_FILE)
for name in zfile.namelist():
    (dirname, filename) = os.path.split(name)
    print "Decompressing " + filename + " on " + dirname
    if not os.path.exists(dirname):
      os.makedirs(dirname)
    zfile.extract(name, 'C:\\.')

config_file = open("C:\\Apache24\\conf\\httpd.conf", 'r')
config_txt = config_file.read()
config_file.close()

new_txt = ""
for line in config_txt.split('\n'):
    if 'BASE_DIR' in line:
        new_txt += line.replace('{BASE_DIR}', BASE_DIR) + "\n"
    else:
        new_txt += line + "\n"

print BASE_DIR
config_file = open("C:\\Apache24\\conf\\httpd.conf", 'w')
config_file.write(new_txt)
config_file.close()

subprocess.call(['C:\\Apache24\\bin\httpd.exe', '-k', 'install'])