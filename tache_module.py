
class Tache:
    def __init__(self, id, titre, description, statut="TODO", auteur="inconnu"):
        self.id = id
        self.titre = titre
        self.description = description
        self.statut = statut      # "TODO" / "DOING" / "DONE"
        self.auteur = auteur

    def __str__(self):
        return f"[{self.id}] {self.titre} - {self.statut} (par {self.auteur})"
class GestionnaireTaches:
    def __init__(self):
        self.taches = {}
        self.prochain_id = 1


    # Ajouter une tâche

    def ajouter_tache(self, titre, description, auteur):
        tache = Tache(
            id=self.prochain_id,
            titre=titre,
            description=description,
            statut="TODO",
            auteur=auteur
        )
        self.taches[self.prochain_id] = tache
        self.prochain_id += 1
        return tache

   
    # Supprimer une tâche
 
    def supprimer_tache(self, id_tache):
        if id_tache in self.taches:
            del self.taches[id_tache]
            return True
        return False

    
    # Lister les tâches
  
    def lister_taches(self):
        return list(self.taches.values())

    # Changer le statut

    def changer_statut(self, id_tache, nouveau_statut):
        if id_tache in self.taches:
            self.taches[id_tache].statut = nouveau_statut
            return True
        return False

