import ftplib
import json
import os
import sys
from datetime import datetime

def upload_config():
    # Lade die Konfiguration aus der GitHub Action
    config_str = os.environ.get('CONFIG_JSON')
    if not config_str:
        print("Keine Konfiguration gefunden")
        sys.exit(1)
    
    config = json.loads(config_str)
    
    # FTP Credentials aus Environment Variables
    FTP_HOST = os.environ.get('FTP_HOST')
    FTP_USER = os.environ.get('FTP_USER')
    FTP_PASS = os.environ.get('FTP_PASS')
    
    # Location is hardcoded to 'spiez'
    LOCATION = 'spiez'
    
    if not all([FTP_HOST, FTP_USER, FTP_PASS]):
        print("FTP Credentials nicht vollständig")
        sys.exit(1)
    
    # Speichere config temporär
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        
    print("Hochzuladende Konfiguration:")
    with open('config.json') as f:
        print(f.read())
    
    # Verbinde zum FTP Server
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        
        # Create location directory if it doesn't exist
        try:
            ftp.mkd(LOCATION)
        except:
            pass  # Directory might already exist
            
        # Change to location directory
        ftp.cwd(LOCATION)
        
        # Öffne die Datei und lade sie hoch
        with open('config.json', 'rb') as f:
            ftp.storbinary('STOR config.json', f)
        
        print("Konfiguration erfolgreich hochgeladen!")
        
        # Cleanup
        ftp.quit()
        os.remove('config.json')
        
    except Exception as e:
        print(f"Fehler beim FTP Upload: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    upload_config()
