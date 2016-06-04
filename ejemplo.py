# -*- coding: UTF-8 -*-

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth() 

drive = GoogleDrive(gauth)
'''
file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'
file1.SetContentString('Hello World!') # Set content of the file from given string
file1.Upload()'''

file1 = drive.CreateFile()
file1.SetContentFile('einstein.jpg')
file1.Upload()
espacio=0
# Auto-iterate through all files that matches this query
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    espacio+=float(file1['fileSize'])

print "Espacio ocupado: "+str(espacio/1073741824)+" Bytes de 15 GB"
