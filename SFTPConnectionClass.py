"""
Uses paramiko to implement Server:
    simplified upload/download via SFTP

Usage:
    server = sftp.Server("user", "pass", "example.com")
    # upload a file
    server.upload("/local/path", "/remote/path")
    # download a file
    server.download("remote/path", "/local/path")
    server.close()

    (with statement support)
    with sftp.Server("user", "pass", "example.com") as server:
        server.upload("/local/path", "/remote/path")
"""

import pysftp


class SFTPConnectionClass(object):
    """
    Wraps paramiko for super-simple SFTP uploading and downloading.
    """

    def __init__(self, username, hostname, password=None, private_key=None, port=None):
        if port is None:
            port = '22'

 ## Variables used for hostkeys setup
        cnopts = pysftp.CnOpts()
        hostkeys = None

 ## Backup hostkeys
        if cnopts.hostkeys.lookup(hostname) == None:
            print("New host - will accept any host key")
            # Backup loaded .ssh/known_hosts file
            hostkeys = cnopts.hostkeys
            # And do not verify host key of the new host
            cnopts.hostkeys = None

 # Define username/password login vs private key login params
        if password is not None:
            conn_params= {'host': hostname, 'username': username, 'password': password,'cnopts': cnopts}
        elif private_key is not None:
            conn_params = {'host': hostname, 'username': username, 'private_key': private_key,'cnopts': cnopts}

        # Connect to SFTP
        self.sftp = pysftp.Connection(**conn_params)

        # Add Host Key if it does not exist
        if hostkeys != None:
            print("Connected to new host, caching its hostkey")
            hostkeys.add(hostname, self.sftp.remote_server_key.get_name(), self.sftp.remote_server_key)
            hostkeys.save(pysftp.helpers.known_hosts())

    def uploadfile(self, localf, remotef,confirm):
        #self.sftp.cd(path.dirname(remote))
        return(self.sftp.put(localpath=localf, remotepath=remotef,confirm=confirm))

    def uploadallfiles(self, localf, remotef ):
        #self.sftp.cd(path.dirname(remote))
        return(self.sftp.put_d(localf, remotef))

    def downloadfile(self, remotef, localf):
        #self.sftp.cd(path.dirname(remote))
        return(self.sftp.get(remotef, localf))

    def downloadallfiles(self, remotef, localf):
        #self.sftp.cd(path.dirname(remote))
        return(self.sftp.get_d(remotef, localf))

    def listdir(self, remotef):
        #self.sftp.cd(path.dirname(remote))
        return(self.sftp.listdir(remotef))

    def removefile(self, remotef):
        self.sftp.remove(remotef)

    def close(self):
        """
        Close the connection if it's active
        """
        self.sftp.close()

    # with-statement support
    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.sftp.close()
        self.close()


