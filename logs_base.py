import time, os, os.path, datetime

log_out = ""

def logger(x = "no log output defined here", y = 0):
    global log_out
    if not os.path.exists(os.getcwd() + "\\logs"):
        os.mkdir(os.getcwd() + "\\logs")
    if log_out == "":
        ver = open(os.getcwd() + "\\version", "r")
        version = ver.read()
        ver.close()
        log_out = "Minecraft ModPack Manager v" + str(version) + "\n\n[======================]\n\n"
    if y != 0:
        log_out += "\n[======================]\n\nLog end" #On écrit les logs dans le fichier
        log = open(os.getcwd() + "\\lastest.log", "w")
        date = datetime.datetime.now()
        log_name = str(os.getcwd() + "\\logs\\log_" + str(date.day) + "-" + str(date.month) + "-" + str(date.year) + "-" + str(date.hour) + "_" + str(date.minute) + "_" + str(date.second) + ".log")
        log1 = open(log_name, "w")
        log.write(log_out)
        log1.write(log_out)
        log.close()
        log1.close()
        print("\nLog file saved as [" + os.getcwd() + "\\lastest.log]" + "\nSaved as [" + log_name + "] too")
    else:
        date = datetime.datetime.now()
        if x != "no log output defined here":
            log_out += str(date.hour) + ":" + str(date.minute) + ":" + str(date.second) + " - " + x + "\n"
        else:
            print(str(date.hour) + ":" + str(date.minute) + ":" + str(date.second) + " - " + x)


#Exemple d'insertion pour un programme random

#logger("test je teste tout par ici")
#logger("test je teste tout par fqebfqici")
#logger("test je teste tout par icfqv")
#logger("test je teste tout par icd")
#logger(0, 1)

#Fin exemple pour un programme random