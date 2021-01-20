import time, os, os.path, datetime
from logs_base import logger

ver = open(os.getcwd() + "\\version", "r") #on génère la variable pour logs
version = ver.read()
ver.close()
log_out = "Minecraft ModPack Manager v" + str(version) + "\n\n[======================]\n\n"

print("Welcome to MC ModPack Manager, this part is only for user vars definition/verification")
end = input("\nPress enter to continue")
isitgood = 0 #Var pour boucles

#on vérifie l'existence du fichier vars.dat (et on le crée s'il n'existe pas)
datpath = os.getcwd() + "\\user_vars.dat"

if not os.path.isfile(datpath):
    file = open(datpath, "w")
    file.write("")
    file.close()

#Récupère les variables d'environement d'install et d'username
vars = open(datpath, "r")
DatRead = vars.readlines()
vars.close()
DatRead += [""] + [""] + [""] #Cette ligne sert juste à forcer au minimum 3 vars pour éviter un plantage

#Supprime les caractères "\n" des éléments (ils sont inutilisables avec)
for i in range(len(DatRead)):
    DatRead[i] = DatRead[i].replace("\n", "")


#On prépare le dictionnaire de variables d'environement et vérifie le contenu du fichier en cas d'éléments manquants
DatDic = {}
DatDicKeys = ["Username", "MCinstall", "MCMPMinstall"]
Write = 0 #var utile pour savoir si on écrit ou non

#Phase de vérif
if DatRead[0] == "": #On définit le nom d'utilisateur si non défini
    DatRead[0] = input("User name not defined !\n")
    Write = 1
    logger("user_vars.dat modified at " + os.getcwd() + "\\user_vars.dat (line 1)")

if (DatRead[1] == "") or (not os.path.exists(DatRead[1] + "\\versions")): #On définit le path d'installation de minecraft (si non ou mal défini)
    print("MC install directory not defined !")
    Write = 1
    while isitgood != 1: #On demande si le dossier est celui par défaut
        isit = input("Is minecraft installed in the defaut folder ? (C:/Users/<username>/appdata/roaming/.minecraft)\n(y/n)\n")
        if isit == "y":
            DatRead[1] = "C:\\Users\\"+ os.getenv("USERNAME")+ "\\AppData\\Roaming\\.minecraft"
        else:
            DatRead[1] = input("Please give the complete minecraft folder installation path:\n(ex: C:\\a_folder\\another_folder\\.minecraft)\n")
        if os.path.exists(DatRead[1] + "\\versions"): #On teste si le dossier existe ou non
            isitgood = 1
        else:
            isitgood = 0
            print("Bad definition !")
            time.sleep(2)
    logger("user_vars.dat modified at " + os.getcwd() + "\\user_vars.dat (line 2)")


if (DatRead[2] == "") or (not os.path.exists(DatRead[2])): #On définit le path d'installation du logiciel (si non ou mal défini)
    DatRead[2] = os.getcwd()
    Write = 1
    logger("user_vars.dat modified at " + os.getcwd() + "\\user_vars.dat (line 3)")


#On écrit si des éléments manquent (sinon, pas besoin)
if Write == 1:
    VarsWrite = DatRead[0] + "\n" + DatRead[1] + "\n" + DatRead[2] + "\n"
    vars = open(datpath, "w")
    vars.write(VarsWrite)
    vars.close()

logger(0, 1)

end = input("\nPress enter to exit program")

os.system('python ' + DatRead[2] + '\\environment_gen.py')