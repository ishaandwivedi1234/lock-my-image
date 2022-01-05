from functools import partial
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from pathlib import Path
import os



def index(request):
   intro =""" Hey ! do you want to send any confidential image to someone, but fear that it may be intercepted ? Then you are on
   right place. Just upload your image and set a private key and download the encrypted image which is ready to sale without fear. And anyone with private key can see your image through this website  """
   context ={'intro':intro,'lock':False,'unlock':False}
   return render(request,'index.html',context)

def lock(request):

   imgfile = request.FILES['imgfile']
   
   masterKey = request.POST.get("masterKey")
   
   
   # print(imgfile)
   # print(masterKey)
   
   masterBytes = bytes(masterKey,'utf-8')
   masterSum = 0
   
   for b in masterBytes:
      masterSum  = masterSum + b
  
   print("master sum",masterSum)
   # print(type(imgfile))
  
   f = imgfile.read()
   imgbytes = bytearray(f)

  
   for i in range(0,len(imgbytes)):
      imgbytes[i] = (imgbytes[i] ^ masterSum) % 256

   BASE_DIR = Path(__file__).resolve().parent.parent
   STATIC_DIR = os.path.join(BASE_DIR, 'static')
   imgPath = os.path.join(STATIC_DIR, 'encrypted.jpg')
   
   with open(imgPath, "wb") as binary_file:
         binary_file.write(imgbytes)
   
   
   intro =""" 
   You can now share this image to anyone without fear, just don't forget to tell them your master key to unlock it. Click on download button to download the locked image now
    """
   context={'lock':True,'unlock':False,'intro':intro}
   
   return render(request,'index.html',context)

def unlock(request):

   imgfile = request.FILES['imgfile']
   masterKey = request.POST.get("masterKey")

   print(imgfile)
   print(masterKey)
   
   masterBytes = bytes(masterKey,'utf-8')
   masterSum = 0
   
   for b in masterBytes:
      masterSum  = masterSum + b
   
   print("master sum",masterSum)
   
   # print(type(imgfile))


   f = imgfile.read()
   
   imgbytes = bytearray(f)

   for i in range(0,len(imgbytes)):
      imgbytes[i] = (imgbytes[i] ^ masterSum) % 256
      
   BASE_DIR = Path(__file__).resolve().parent.parent
   STATIC_DIR = os.path.join(BASE_DIR, 'static')
   
   imgPath = os.path.join(STATIC_DIR, 'decrypted.jpg')
   
   with open(imgPath, "wb") as binary_file:
         binary_file.write(imgbytes)

   
   intro =""" 
   You would be able to open the image if master key entered by you is correct. Other wise you may try again
    """
   context={'lock':False,'unlock':True,'intro':intro}

   return render(request,'index.html',context)

   


