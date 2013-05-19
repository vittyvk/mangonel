import sys

try:
    from katello.client import server
    from katello.client.server import BasicAuthentication
    
except ImportError, e:
    print "Please install Katello CLI package."
    sys.exit(-1)


class Server(object):

    def __init__(self, host, project='/katello/', username='admin', password='admin'):
        """
        Initiates a session to the provided host, using credentials.
        """

        s = server.KatelloServer(host=host, path_prefix=project)
        s.set_auth_method(BasicAuthentication(username, password))
        server.set_active_server(s)
