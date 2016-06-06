from Tkinter import *

from tkinter import ttk

import tkFileDialog

import sys,os

from pydrive.auth import GoogleAuth

from pydrive.drive import GoogleDrive

import dropbox

from dropbox import client, rest, session

import onedrivesdk

from onedrivesdk.helpers import GetAuthCodeServer



#conectando con Dropbox---------------------------------

app_key = 'dyudz69cn64qqnp'

app_secret = 'os1sw97dv6w5hkk'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

authorize_url = flow.start()

clientDrop = dropbox.client.DropboxClient('CEHAMSGRPBAAAAAAAAAACCi3p6xWFCY5ayssALMM5r7UvoPzdT1_ygQ-LQSH3emB')

diccionarioDrop= clientDrop.account_info()

espDrop=diccionarioDrop.values()[10]['quota']-diccionarioDrop.values()[10]['normal']

#conectando con GoogleDrive-------------------------------

gauth = GoogleAuth()

# Try to load saved client credentials

gauth.LoadCredentialsFile("auth/mycreds.txt")

if gauth.credentials is None:

    # Authenticate if they're not there

    gauth.LocalWebserverAuth()

elif gauth.access_token_expired:

    # Refresh them if expired

    gauth.Refresh()

else:

    # Initialize the saved creds

    gauth.Authorize()

# Save the current credentials to a file

gauth.SaveCredentialsFile("auth/mycreds.txt")


drive = GoogleDrive(gauth)

espGoo=0
    
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    

for file2 in file_list:

		espGoo+=int(file2.metadata['quotaBytesUsed'])

#conectando con OneDrive-------------------------------
redirect_uri = "http://localhost:8080/"
client_secret = "tLwyKkPS74siASB9DnEKt0C"

client = onedrivesdk.get_default_client(client_id='4490f18b-5c69-4aa4-8694-b84f6e8d9a15',
                                        scopes=['wl.signin',
                                                'wl.offline_access',
                                                'onedrive.readwrite'])

auth_url = client.auth_provider.get_auth_url(redirect_uri)

#this will block until we have the code
code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

client.auth_provider.authenticate(code, redirect_uri, client_secret)

items = client.item(id="root").children.get()

item=onedrivesdk.Item()

espOne=0

for item in items:

		espOne+=int(item.size)
#--------------------------------------------------------------------

class Application(Frame):

	def __init__(self,master):

		Frame.__init__(self,master)

		self.grid()

		self.create_widgets()

	

	def create_widgets(self):

		self.b1=Button(self,text="Subir Archivo",command= self.fun) 

		self.b1.grid(row=3,column=2,columnspan=2,sticky=W) 

		self.b2=Button(self,text="Descargar Archivo",command= self.descargarDrop, width=20) 

		self.b2.grid(row=10,column=1) 

		self.b3=Button(self,text="Descargar Archivo",command= self.descargarDrive, width=20) 

		self.b3.grid(row=10,column=2) 

		self.b4=Button(self,text="Descargar Archivo",command= self.descargarOdrive, width=20) 

		self.b4.grid(row=10,column=3) 

		

		#labels------------------------------------------------

		self.lbl1= Label(self, text="")

		self.lbl1.grid(row= 3, column= 3, sticky= W)

		self.lblEspDrop= Label(self, text="Espacio en Dropbox: "+str(espDrop)+" bytes")

		self.lblEspDrop.grid(row= 0, column=0, columnspan =2, sticky= W)

		self.lblEspGoo= Label(self, text="Espacio en Google Drive: "+str(15*1024*1024*1024-espGoo)+" bytes")

		self.lblEspGoo.grid(row= 1, column=0, columnspan =2, sticky= W)

		self.lblEspOne= Label(self, text="Espacio en One Drive: "+str(5*1024*1024*1024-espOne)+" bytes")

		self.lblEspOne.grid(row= 2, column=0, columnspan =2, sticky= W)

		self.lblArchivosDrop= Label(self, text="Archivos en Dropbox:")

		self.lblArchivosDrop.grid(row= 8, column=1, columnspan =2, sticky= W)

		self.lblArchivosGdri= Label(self, text="Archivos en Google Drive:")

		self.lblArchivosGdri.grid(row= 8, column=2, columnspan =2, sticky= W)

		self.lblArchivosOdri= Label(self, text="Archivos en One Drive:")

		self.lblArchivosOdri.grid(row= 8, column=3, columnspan =2, sticky= W)





		#Radio Buttons------------------------------------

		self.nube = StringVar()

		Radiobutton(self,

					text = "Dropbox",

					variable= self.nube,

					value = "dropbox.",

					).grid(row=5,column=2,sticky=W)

		Radiobutton(self,

					text = "Google Drive",

					variable= self.nube,

					value = "Gdrive.",

					).grid(row=6,column=2,sticky=W)

		Radiobutton(self,

					text = "OneDrive",

					variable= self.nube,

					value = "Odrive.",

					).grid(row=7,column=2,sticky=W)



		#ListBox Dropbox--------------------------------------

		self.lbDrop = Listbox(self, height=20, width= 30)

		self.lbDrop.grid(column=1, row=9, sticky=(N,W))

		s = ttk.Scrollbar(self, orient=VERTICAL, command=self.lbDrop.yview)

		s.grid(column=1, row=9, sticky=(N,S,E))

		self.lbDrop['yscrollcommand'] = s.set

		self.cargarArchivosDrop()



		#ListBox Google Drive--------------------------------------

		self.lbGdri = Listbox(self, height=20, width= 30)

		self.lbGdri.grid(column=2, row=9, sticky=(N,W))

		s2 = ttk.Scrollbar(self, orient=VERTICAL, command=self.lbGdri.yview)

		s2.grid(column=2, row=9, sticky=(N,S,E))

		self.lbGdri['yscrollcommand'] = s2.set

		self.cargarArchivosDrive()

		

		#ListBox One Drive--------------------------------------

		self.lbOdri = Listbox(self, height=20, width= 30)

		self.lbOdri.grid(column=3, row=9, sticky=(N,W))

		s3 = ttk.Scrollbar(self, orient=VERTICAL, command=self.lbOdri.yview)

		s3.grid(column=3, row=9, sticky=(N,S,E))

		self.lbOdri['yscrollcommand'] = s3.set

		self.cargarArchivosOne()

		

	#Cargar Archivos a listBox----------------------

	def cargarArchivosDrop(self):

		self.lbDrop.delete(0, END)

		metadata = clientDrop.metadata('/bespin')

		files = [content['path'].split('/')[-1] for content in metadata['contents']]

		for k in range(len(files)):

			self.lbDrop.insert('end',str(files[k]))



	def cargarArchivosDrive(self):

		self.lbGdri.delete(0, END)

		file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

		for file1 in file_list:

			self.lbGdri.insert('end',file1['title'])

	def cargarArchivosOne(self):


		self.lbOdri.delete(0, END)


		items = client.item(id="root").children.get()

		item=onedrivesdk.Item()

        	for item in items:

			self.lbOdri.insert('end',item.name)

			#print item.size

			
        

	#Avisos en el Label-------------------------------------

	def fun(self):

		if self.nube.get()=="dropbox.":

			self.lbl1["text"]="Dropbox"

			self.buscar()

		elif self.nube.get()=="Gdrive.":

			self.lbl1["text"]="Google Drive"

			self.buscar()

		elif self.nube.get()=="Odrive.":

			self.lbl1["text"]="OneDrive"

			self.buscar()

		elif self.nube.get()=="cualquiera.":

			self.lbl1["text"]="Cualquiera"

			self.buscar()

		else:

			self.lbl1["text"]="Debes elegir una nube"

	

	#Elegir archivo y redireccionar a funcion de subida de la nube elegida--------

	def buscar(self):

		#Abre el desplegable para buscar el archivo a subir

		filepath = tkFileDialog.askopenfilename(parent=root,title='Elige el archivo') 

		filename = os.path.split(filepath)[-1]

		filesize = os.path.getsize(filepath)

		if self.nube.get()=="cualquiera.":

			self.subir	(name=filename, path=filepath, size=filesize)

		if self.nube.get()=="dropbox.":

			self.subirDrop(name=filename, path=filepath,size=filesize)

		if self.nube.get()=="Gdrive.":

			self.subirDrive(name=filename, path=filepath,size=filesize)

		if self.nube.get()=="Odrive.":

			self.subirOdrive(name=filename, path=filepath,size=filesize)

		

	#Subir a Dropbox-------------------------------------

	def subirDrop(self,name,path,size):

		espacio=diccionarioDrop.values()[10]['quota']-diccionarioDrop.values()[10]['normal']

		if size>espacio:

			self.lbl1["text"]="No hay suficiente espacio en tu Dropbox"

		else:

			f = open(path, 'rb')

    			response = clientDrop.put_file('/Bespin/'+name, f)

			self.lbl1["text"]= name+" subido con exito"

			self.refresh()

	
	#Subir a Drive-------------------------------------

	def subirDrive(self,name,path,size):

		espacio=0

		file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

		for file2 in file_list:

			espacio+=int(file2.metadata['quotaBytesUsed'])

		if size>espacio:

			self.lbl1["text"]="No hay suficiente espacio en tu Drive"

		else:

			file1 = drive.CreateFile({'title': name})

    			file1.SetContentFile(path)

			file1.Upload()

			self.lbl1["text"]= name+" subido con exito"

			self.refresh()

	
	#Subir a OneDrive-------------------------------------

	def subirOdrive(self,name,path,size):

		espacio=5242880-espOne

		if size>espacio:

			self.lbl1["text"]="No hay suficiente espacio en tu OneDrive"

		else:

			returned_item = client.item(drive="me", id="root").children[name].upload(path)

			self.lbl1["text"]= name+" subido con exito"

			self.refresh()

	


	#Descargar de Dropbox-------------------------------------

	def descargarDrop(self):

		file= self.lbDrop.curselection()

		value = str(self.lbDrop.get(file[0]))

		f, metadata = clientDrop.get_file_and_metadata('/bespin/'+value)

		out = open(value, 'wb')

		out.write(f.read())

		out.close()

		os.rename(os.getcwd()+"/"+value, os.getcwd()+"/Descargas/Dropbox/"+value)

		self.lbl1["text"]= value+" descargado con exito"

	
	#Descargar de Drive-------------------------------------

	def descargarDrive(self):

		file= self.lbGdri.curselection()

		value = str(self.lbGdri.get(file[0]))

		file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

		for file6 in file_list:

			if file6['title'] == value:

			    file6.GetContentFile(os.getcwd()+"/Descargas/Drive/"+value)
        

		self.lbl1["text"]= value+" descargado con exito"

    	
	#Descargar de OneDrive-------------------------------------

	def descargarOdrive(self):

		file= self.lbOdri.curselection()

		value = str(self.lbOdri.get(file[0]))

		print os.getcwd()+"/"+value

		client.item(drive="me", id="root").children[value].download(os.getcwd()+"/Descargas/OneDrive/"+value)

		self.lbl1["text"]= value+" descargado con exito"

	#Actualizamos los datos de espacio en las nubes

	def refresh(self):

		#Dropbox--------------------------------------------------

		diccionarioDrop= clientDrop.account_info()

		espDrop=diccionarioDrop.values()[10]['quota']-diccionarioDrop.values()[10]['normal']

		self.lblEspDrop["text"]="Espacio en Dropbox: "+str(espDrop)+" bytes"

		self.cargarArchivosDrop()



		#Google Drive--------------------------------------------------

		espGoo=0
    
		file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    

		for file2 in file_list:

				espGoo+=int(file2.metadata['quotaBytesUsed'])

		self.lblEspGoo["text"]="Espacio en Google Drive: "+str(15*1024*1024*1024-espGoo)+" bytes"

		self.cargarArchivosDrive()

		#OneDrive--------------------------------------------------
		item=onedrivesdk.Item()

		espOne=0

		for item in items:

				espOne+=int(item.size)

		self.lblEspOne["text"]="Espacio en OneDrive: "+str(15*1024*1024*1024-espOne)+" bytes"
		
		self.cargarArchivosOne()


		

root=Tk()

#root.config(bg="white") # Le da color al fondo

root.title("Bespin The Cloud City")

root.geometry("800x600")

app=Application(root)

root.mainloop()



