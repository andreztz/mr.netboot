#!/usr/bin/env python

from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor

reactor.listenTCP(80, Site(File("/data")), interface='0.0.0.0')
reactor.run()
