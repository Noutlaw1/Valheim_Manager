class Config(object):
        #Add an array of IPs here that so they are allowed access.
        ALLOWED_IPS = ['']
        #Path to wherever the Valheim docker container is stored, if you want to run a backup script there.
        VALHEIM_DIR = ""
        #Valheim backup script name.
        BACKUP_SCRIPT = ""
