# client.py
import socket


class ClientTaches:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port
        self.sock = None

    def connecter(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print("Connecté au serveur.")

    def envoyer(self, message):
        self.sock.sendall(message.encode())

    def recevoir(self):
        data = self.sock.recv(4096).decode()
        return data

    def fermer(self):
        if self.sock:
            self.sock.close()
            print("Connexion fermée.")





def menu_client():
    client = ClientTaches()

    try:
        client.connecter()

        while True:
            print("\n=== MENU CLIENT ===")
            print("1. Ajouter une tâche")
            print("2. Lister les tâches")
            print("3. Supprimer une tâche")
            print("4. Changer le statut")
            print("0. Quitter")

            choix = input("Votre choix : ")

           
            if choix == "1":
                titre = input("Titre : ")
                description = input("Description : ")
                auteur = input("Auteur : ")
                message = f"ADD|{titre}|{description}|{auteur}"
                client.envoyer(message)
                print(client.recevoir())

            
            elif choix == "2":
                client.envoyer("LIST")
                print("--- LISTE DES TÂCHES ---")
                print(client.recevoir())

           
            elif choix == "3":
                id_tache = input("ID à supprimer : ")
                client.envoyer(f"DELETE|{id_tache}")
                print(client.recevoir())

            elif choix == "4":
                id_tache = input("ID : ")
                statut = input("Nouveau statut (TODO/DOING/DONE) : ")
                client.envoyer(f"STATUS|{id_tache}|{statut}")
                print(client.recevoir())

            
            elif choix == "0":
                client.envoyer("QUIT")
                client.fermer()
                break

            else:
                print("Choix invalide.")

    except Exception as e:
        print("Erreur :", e)
        client.fermer()
