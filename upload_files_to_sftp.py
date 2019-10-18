from SFTPConnectionClass import SFTPConnectionClass
import glob
import os
from os import path
from custom_utilities import create_dict_from_file
import sys

"""
    This method is designed to put files to an sftp.
    This method needs env_file name as an argument.
    It is designed for username/password based authentication and private key based authentication
    The authentication is done with username/password. It accepts filepattern as a param.
    If the filepattern is not set then it uploads all files under the local_dir to remote_dir.
    File pattern can be File name or a pattern with * as the wildcard"""

env_file = sys.argv[1] #Env variables file. Key value pairs. One per line. Ex: hostname=sftp.test.com. Elements accepted are hostname,username,password,private_key,remote_dir,local_dir,filepattern



# Setup the env vars dictionary from the env vars file
env_vars = create_dict_from_file(os.path.join(env_file), '=')
if type(env_vars) is dict:
    print("Dictionary from file Step completed")
else:
    print("Unable to create a dictionary from file %s" %(env_file))
    sys.exit("Unable to create a dictionary from file %s" %(env_file))
##


if "password" in env_vars:
    con =  SFTPConnectionClass(username=env_vars['username'], hostname=env_vars['hostname'],password=env_vars['password'])
elif "private_key" in env_vars:
    con = SFTPConnectionClass(username=env_vars['username'], hostname=env_vars['hostname'],private_key=env_vars['private_key'])
else:
    print("Authentication failed. Need to provide username/password or username/private_key details.")
    exit("Authentication failed. Need to provide username/password or username/private_key details.")

if "filepattern" not in env_vars:
    filepattern = "*"
else:
    filepattern=env_vars['filepattern']


for file in glob.glob(path.join(env_vars['local_dir'], filepattern)):
    print("Uploading file %s" %(file))
    base = path.basename(file)
    if "confirm" in env_vars:
        v_confirm=True if env_vars['confirm'].upper() == 'TRUE' else False 
    else:
        v_confirm=True
    print(con.uploadfile(localf=file, remotef=env_vars['remote_dir'] + '/' + base,confirm=v_confirm))
