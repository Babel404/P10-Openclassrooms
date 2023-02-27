++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# PROJET 10 : Créez une API sécurisée RESTful en utilisant Django REST

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

## Contexte

Création d'une API REST permettant aux utilisateurs de créer divers projets.
Ces projets peuvent avoir plusieurs collaborateurs et des problèmes liés aux projets peuvent être signalés et commentés.  

## Installation


### 1 - Mise en place de l'environnement virtuel "env"

    1 - Accès au répertoire du projet :
            
            cd /P10_COUPARD_Bastien

    2 - Création de l'environnement virtuel :
            
            python -m venv env


### 2 - Ouverture de l'environnement virtuel et ajout des packages

            source env/Scripts/activate
            
            (env) $ pip install -r requirements.txt
            

### 3 - Modification du fichier softdesk/settings.py

    1 - Modifier la variable 'SECRET_KEY' afin d'ajouter une clé de sécurité
        "django-insecure-( + 50 caractères aléatoires avec majuscule,
        minuscule, chiffres et caractères spéciaux )"


## Utilisation du programme


### 1 - Lancement

    1 - activation de l'environnement virtuel dans le répertoire de base:

        source env/Scripts/activate

    2 - accès au répertoire softdesk:

        cd softdesk/

    3 - Lancement du serveur Django

        python manage.py runserver


### 2 - Utilisation de l'API

    Afin de tester cette API, 4 utilisateurs fictifs sont enregistrés avec quelques projets,
    problèmes et commentaires dans la base de donnée "db.sqlite3" mise à disposition dans le repository : 

        - admin
        - pierre
        - paul
        - jacques

        le mot de passe pour les utilisateurs : 123Soleil!

    Un accès à la page admin est possible :

        Exemple sur une installation locale : http://127.0.0.1:8000/admin

        utilisateur : admin    
        password : 123Soleil!

    Cela permet un accès complet (lecture et écriture) aux tables de la base de données.

    Commande pour la création d'un administrateur :

        python manage.py createsuperuser

    Pour avoir une base de donnée initiale:

        1 - Arrêter le serveur Django en effectuant la combinaison :
                
                 control + c 

        2 - Supprimer le fichier "db.sqlite3"

        3 - effectuer la migration vers la nouvelle base

                python manage.py makemigrations => Cela crée un fichier dans softdesk/projects/migrations 

                python manage.py migrate => Création des tables dans le fichier "db.sqlite" (crée directement)
              
###  3 - Utilisation des requêtes

    Plusieurs méthodes existe pour effectuer des requêtes, exemple :

        - Avec le logiciel POSTMAN (Utilisé pour la documentation de cet API)

                Installation sur Linux UBUNTU :

                sudo snap install postman

        - Avec le logiciel en ligne de commande cURL :

            Installation sur Linux UBUNTU :

                sudo snap install curl

            Exemple de la requête 'GET projects'

                curl --location --request GET 'http://127.0.0.1:8000/projects' \
                --header 'Authorization: Bearer "TOKEN 'access' "'

###  4 - Liste des requêtes   

    La documentation détaillé est disponible sur : https://documenter.getpostman.com/view/11631622/2s93CRKBcr

    - POST signup : http://127.0.0.1:8000/signup/ 

        Inscription d'un utilisateur à l'API. 
        Champs à utiliser : username, password, password2, first_name, last_name, email

    - POST : http://127.0.0.1:8000/login/

        Connexion d'un utilisateur à l'API. 
        Champs à utiliser : username, password
        Retour : Clé TOKEN 'access' (A utiliser pour les requêtes avec authentification, valable 1 heure)
                 Clé TOKEN 'refresh' (A utiliser pour les requêtes refresh et logout)
                 
    - POST : http://127.0.0.1:8000/login/refresh/

        Récupération d'une autre paire de clé TOKEN sans se reconnecter
        Champs à utiliser : refresh
        Retour : Clé TOKEN 'access' (A utiliser pour les requêtes avec authentification, valable 1 heure)
                 Clé TOKEN 'refresh' (A utiliser pour les requêtes refresh et logout)

    - PUT : http://127.0.0.1:8000/change_password/

        Authentification requis
        Permet le changement du password
        Champs à utiliser : old_password, password, password2

    - GET : http://127.0.0.1:8000/users/

        Authentification requis
        Permet d'accéder à la liste des utilisateurs de l'API

    - POST : http://127.0.0.1:8000/logout/

        Authentification requis
        Permet de blacklister la clé TOKEN refresh pour interdire son utilisation
        Champs à utiliser : refresh

    - GET : http://127.0.0.1:8000/projects/

        Authentification requis
        Accès à la liste des projets auxquels l'utilisateur est lié.

    - POST : http://127.0.0.1:8000/projects/

        Authentification requis
        Création d'un projet
        Champs à utiliser : title, description, project_type

    - GET : http://127.0.0.1:8000/projects/{id_du_projet}

        Authentification requis, utilisateur contributeur du projet
        Accès aux détails d'un projet
    
    - PUT : http://127.0.0.1:8000/projects/{id_du_projet}

        Authentification requis, utilisateur auteur du projet
        Modification du projet
        Champs à utiliser : title, description, project_type

    - DELETE : http://127.0.0.1:8000/projects/{id_du_projet}

        Authentification requis, utilisateur auteur du projet
        Suppression du projet

    - GET : http://127.0.0.1:8000/projects/{id_du_projet}/users/
        
        Authentification requis, utilisateur contributeur du projet
        Accès à la liste des contributeurs du projet

    - POST : http://127.0.0.1:8000/projects/{id_du_projet}/users/

        Authentification requis, utilisateur auteur du projet
        Ajout d'un contributeur au projet
        Champs à utiliser : user_id, role

    - DELETE : http://127.0.0.1:8000/projects/{id_du_projet}/users/{id_du_contributeur}

        Authentification requis, utilisateur auteur du projet
        Suppression d'un contributeur au projet
     
    - GET : http://127.0.0.1:8000/projects/{id_du_projet}/issues/

        Authentification requis, utilisateur contributeur du projet
        Accès à la liste des problèmes du projet

    - POST : http://127.0.0.1:8000/projects/{id_du_projet}/issues/

        Authentification requis, utilisateur contributeur du projet
        Ajout d'un problème au projet
        Champs à utiliser : title, description, tag, priority, status, assignee_user_id

    - PUT : http://127.0.0.1:8000/projects/{id_du_projet}/issues/{id_du_problème}

        Authentification requis, utilisateur auteur du problème posté
        Ajout d'un problème au projet
        Champs à utiliser : title, description, tag, priority, status, assignee_user_id
    
    - DELETE : http://127.0.0.1:8000/projects/{id_du_projet}/issues/{id_du_problème}

        Authentification requis, utilisateur auteur du problème posté
        Suppression d'un problème au projet

    - GET : http://127.0.0.1:8000/projects/{id_du_projet}/issues/{id_du_problème}/comments/

        Authentification requis, utilisateur contributeur du projet
        Accès à la liste des commentaires du problème

    - POST : http://127.0.0.1:8000/projects/{id_du_projet}/issues/{id_du_problème}/comments/

        Authentification requis, utilisateur contributeur du projet
        Ajout d'un commentaire au problème
        Champs à utiliser : description

    - GET : http://127.0.0.1:8000/projects/{id_du_projet}/issues/{id_du_problème}/comments/{id_du_commentaire}

        Authentification requis, utilisateur contributeur du projet
        Accès au details du commentaire au problème

    - PUT : http://127.0.0.1:8000/projects/{id_du_projet}/issues/{id_du_problème}/comments/{id_du_commentaire}

        Authentification requis, utilisateur auteur du commentaire
        Modification d'un commentaire au problème
        Champs à utiliser : description

    - DELETE : http://127.0.0.1:8000/projects/{id_du_projet}/issues/{id_du_problème}/comments/{id_du_commentaire}

        Authentification requis, utilisateur auteur du commentaire
        Suppression d'un commentaire au problème
