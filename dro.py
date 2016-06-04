import dropbox
from dropbox import client, rest, session

client = dropbox.client.DropboxClient('CEHAMSGRPBAAAAAAAAAACCi3p6xWFCY5ayssALMM5r7UvoPzdT1_ygQ-LQSH3emB')
diccionario= client.account_info()
valores = diccionario.values()
#espacio total en mb
print valores[10]['quota']/1048576
#espacio usado en mb
print valores[10]['normal']/1048576
