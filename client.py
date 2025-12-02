import socket
import json

class ClientTaches:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   
    # Connexion au serveur
  
    def connecter(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("✅ Connecté au serveur.")
        except Exception as e:
            print("❌ Impossible de se connecter :", e)
            exit()


    # Envoi et réception de messages

    def envoyer(self, message):
        try:
            self.client_socket.send((message + "\n").encode())
            data = self.client_socket.recv(4096).decode()
            return data.strip()
        except:
            print("❌ Erreur de communication avec le serveur.")
            return None


    # Menu principal

    def menu(self):
        while True:
            print("\n===== MENU =====")
            print("1. Ajouter une tâche")
            print("2. Lister les tâches")
            print("3. Supprimer une tâche")
            print("4. Changer le statut d’une tâche")
            print("5. Quitter")

            choix = input("Votre choix : ")

            if choix == "1":
                self.ajouter_tache()

            elif choix == "2":
                self.lister_taches()

            elif choix == "3":
                self.supprimer_tache()

            elif choix == "4":
                self.changer_statut()

            elif choix == "5":
                print("👋 Au revoir !")
                self.client_socket.close()
                break

            else:
                print("❌ Choix invalide.")


    # 1) Ajouter une tâche
  
    def ajouter_tache(self):
        titre = input("Titre : ")
        description = input("Description : ")

        message = f"ADD;{titre};{description}"
        rep = self.envoyer(message)
        print("➡️ Réponse serveur :", rep)

 
    # 2) Lister les tâches

    def lister_taches(self):
        rep = self.envoyer("LIST")

        try:
            taches = json.loads(rep)
            print("\n===== LISTE DES TÂCHES =====")
            if not taches:
                print("(aucune tâche)")
                return

            for t in taches:
                print(f"ID: {t['id']} | {t['titre']} | {t['description']} | STATUT: {t['statut']}")
        except:
            print("❌ Erreur : réponse serveur invalide.")


    # 3) Supprimer une tâche

    def supprimer_tache(self):
        id_tache = input("ID de la tâche à supprimer : ")
        rep = self.envoyer(f"DEL;{id_tache}")
        print("➡️ Réponse serveur :", rep)

    
    # 4) Changer le statut

    def changer_statut(self):
        id_tache = input("ID de la tâche : ")
        new_statut = input("Nouveau statut (TODO / DOING / DONE) : ").upper()

        msg = json.dumps({
            "action": "change_status",
            "id": id_tache,
            "statut": new_statut
        })

        rep = self.envoyer(msg)
        print("➡️ Réponse serveur :", rep)



