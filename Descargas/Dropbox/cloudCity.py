# -*- coding: UTF-8 -*-
import sys,os
import Tkinter
import tkFileDialog
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import dropbox
from dropbox import client, rest, session
'''
gauth = GoogleAuth()
gauth.LocalWebserverAuth() 

drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'
file1.SetContentString('Hello World!') # Set content of the file from given string
file1.Upload()

file1 = drive.CreateFile()
file1.SetContentFile('einstein.jpg')
file1.Upload()
espacio=0
Auto-iterate through all files that matches this query
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    espacio+=float(file1['fileSize'])

print "Espacio ocupado: "+str(espacio/1073741824)+" Bytes de 15 GB"'''

app_key = 'dyudz69cn64qqnp'
app_secret = 'os1sw97dv6w5hkk'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

authorize_url = flow.start()
client = dropbox.client.DropboxClient('CEHAMSGRPBAAAAAAAAAACCi3p6xWFCY5ayssALMM5r7UvoPzdT1_ygQ-LQSH3emB')


root = Tkinter.Tk()
root.withdraw()

filename = tkFileDialog.askopenfilename(parent=root,title='Elige el archivo') #abre una ventanita para elegir el archivo con el ratón
print filename


print "Seleccione la nube"
print "1. Google Drive"
print "2. Dropbox"
choice = raw_input(" >>  ")

if choice == '1':
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() 
    drive = GoogleDrive(gauth)
    file1 = drive.CreateFile()
    file1.SetContentFile(filename)
    print "---Subiendo archivo..."
    file1.Upload()
    espacio=0
    
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    
    print "---Archivo subido"
    '''
    for file1 in file_list:
        espacio+=float(file1['fileSize'])
    print "Espacio ocupado: "+str(espacio/1073741824)+" Bytes de 15 GB"'''

if choice == '2':
    f = open('working-draft.txt', 'rb')
    response = client.put_file('/magnum-opus.txt', f)
    print 'uploaded: ', response
    diccionario= client.account_info()
    valores = diccionario.values()
    #espacio total en mb
    print valores[10]['quota']/1048576
    #espacio usado en mb
    print valores[10]['normal']/1048576
