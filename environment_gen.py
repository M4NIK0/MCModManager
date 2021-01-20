import time, os, os.path, shutil, datetime
from logs_base import logger


ver = open(os.getcwd() + "\\version", "r") #on génère la variable pour logs
version = ver.read()
ver.close()

log_out = "Minecraft ModPack Manager v" + str(version) + "\n\n[======================]\n\n"

usrpath = os.getcwd() + "\\user_vars.dat" #On récupère les vars utilisateur, on traîte les données et on construit le dictionnaire en question
usrvars = open(usrpath, "r")
usrvrfile = usrvars.readlines()

for i in range(len(usrvrfile)):
    usrvrfile[i] = usrvrfile[i].replace("\n", "")

User_Vars = {}
User_Vars_Keys = ["Username", "MC_path", "MCMPM_path"]
for i in range(3):
    User_Vars[User_Vars_Keys[i]] = usrvrfile[i]

if not os.path.exists(User_Vars["MCMPM_path"] + "\\packs"): #On crée un dossier pour contenir les packs, configs et paramètres du jeu
    os.mkdir(User_Vars["MCMPM_path"] + "\\packs")
    os.mkdir(User_Vars["MCMPM_path"] + "\\packs\\options")
    os.mkdir(User_Vars["MCMPM_path"] + "\\packs\\pack")
    os.mkdir(User_Vars["MCMPM_path"] + "\\packs\\config")
    config_file = open(User_Vars["MCMPM_path"] + "\\packs" + "\\configs.dat", "w")
    config_file.write("")
    config_file.close()
    logger("packs folder added at " + User_Vars["MCMPM_path"] + "\\packs (associated content added too)")
    
    

if not os.path.exists(User_Vars["MCMPM_path"] + "\\backups"): #On crée un dossier de backups des packs et des configs
    os.mkdir(User_Vars["MCMPM_path"] + "\\backups")
    os.mkdir(User_Vars["MCMPM_path"] + "\\backups\\game")
    os.mkdir(User_Vars["MCMPM_path"] + "\\backups\\options")
    os.mkdir(User_Vars["MCMPM_path"] + "\\backups\\pack")
    os.mkdir(User_Vars["MCMPM_path"] + "\\backups\\config")
    config_file = open(User_Vars["MCMPM_path"] + "\\backups" + "\\configs.dat", "w")
    config_file.write("")
    config_file.close()
    logger("backups folder added at " + User_Vars["MCMPM_path"] + "\\backups (associated content added too)")

if not os.path.exists(User_Vars["MC_path"] + "\\MCMPM_configs"):
    os.mkdir(User_Vars["MC_path"] + "\\MCMPM_configs")
    logger("packs folder added at " + User_Vars["MCMPM_path"] + "\\packs (associated content added too)")

if not os.path.exists(User_Vars["MC_path"] + "\\mods"):
    os.mkdir(User_Vars["MC_path"] + "\\mods")
    logger("packs folder added at " + User_Vars["MCMPM_path"] + "\\packs (associated content added too)")

if not os.path.exists(User_Vars["MCMPM_path"] + "\\logs"):
    os.mkdir(User_Vars["MCMPM_path"] + "\\logs")
    logger("packs folder added at " + User_Vars["MCMPM_path"] + "\\logs (associated content added too)")

logger(0, 1)

end = input("\nPress enter to exit program\n")