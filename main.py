from aparat_downloader import *

if __name__ == '__main__':

    link = "https://www.aparat.com/v/5Mm64"
    
    vide_instance = AparatDownloader(link)
    
    if len(vide_instance.available_qualities) > 0:
        download_path = vide_instance.download(vide_instance.available_qualities[0])
        best_download_path = vide_instance.download_best_quality()
        
    del vide_instance