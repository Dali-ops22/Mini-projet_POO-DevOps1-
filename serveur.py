# serveur.py
import socket
import threading
import json


class ServeurTaches:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        

        # Création du socket serveur
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f"Serveur lancé sur {self.host}:{self.port}")

    
    # 1) Attente des connexions
   
    def start(self):
        print("En attente de connexions...")
        while True:
            client_socket, client_addr = self.server_socket.accept()
            print(f"Client connecté : {client_addr}")

            # Thread = gérer plusieurs clients en même temps
            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.start()


    # 2) Gestion d’un client
  
    def handle_client(self, client_socket):
        with client_socket:
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break

                    message = data.decode().strip()
                    print(f"Reçu : {message}")

                    # Traitement du message
                    response = self.process_message(message)

                    # Réponse au client
                    client_socket.send((response + "\n").encode())

                except:
                    break

   
    # 3) Traitement des commandes
   
    def process_message(self, msg):

        # ----- Mode JSON -----
        if msg.startswith("{"):
            try:
                data = json.loads(msg)
                action = data.get("action")

                if action == "add":
                    t = self.gestionnaire.ajouter_tache(
                        data.get("titre"), 
                        data.get("description")
                    )
                    return json.dumps({"status": "ok", "id": t.id})

                elif action == "list":
                    return json.dumps(self.gestionnaire.lister_taches())

                elif action == "del":
                    ok = self.gestionnaire.supprimer_tache(data.get("id"))
                    return json.dumps({"status": "ok" if ok else "not_found"})

            except json.JSONDecodeError:
                return "ERREUR: JSON invalide"

        # ----- Mode Texte -----
        parts = msg.split(";")

        command = parts[0].upper()

        if command == "ADD" and len(parts) >= 3:
            t = self.gestionnaire.ajouter_tache(parts[1], parts[2])
            return f"TACHE AJOUTEE ID={t.id}"

        elif command == "LIST":
            return json.dumps(self.gestionnaire.lister_taches())

        elif command == "DEL" and len(parts) >= 2:
            ok = self.gestionnaire.supprimer_tache(parts[1])
            return "SUPPRIMEE" if ok else "ID INTROUVABLE"

        return "COMMANDE INVALIDE"
