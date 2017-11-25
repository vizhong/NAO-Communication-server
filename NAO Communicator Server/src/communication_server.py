'''
Created on 07.09.2012

@author: hannes
'''
import os, sys, argparse
import logging
from time import sleep

from settings.Settings import Settings
from network.serverManager import ServerManager
from commands.Command import NAOCommand



def parseSettings():
	"""
	Function to parse settings from command line arguments
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument( "-rip", "--robotip", help="Robot ip (default: 127.0.0.1)", type=str, default="127.0.0.1" )
	parser.add_argument( "-rp", "--robotport", help="Robot port", type=int, default=9559 )
	parser.add_argument( "-sip", "--serverip", help="Server ip (default: 127.0.0.1)", type=str, default="127.0.0.1" )
	parser.add_argument( "-sp", "--serverport", help="Server port (default: 5050)", type=int, default=5050 )
	parser.add_argument( "-st", "--servicetype", help="Network service type (default _naocom._tcp)", type=str, default="_naocom._tcp" )
	parser.add_argument("-log", "--loglevel", help="Log level (default: INFO)", type=str, default="INFO")

	args = parser.parse_args()
	Settings.naoHostName = args.robotip
	Settings.naoPort = args.robotport
	Settings.serverDefaultIP = args.serverip
	Settings.serverDefaultPort = args.serverport
	Settings.serverServiceType = args.servicetype

	numeric_level = getattr(logging, args.loglevel.upper(), None)
	if not isinstance(numeric_level, int):
			raise ValueError('Invalid log level: %s' % args.loglevel)
	else:
		logging.basicConfig(level=numeric_level)

	return True

if __name__ == '__main__':

	# set current working path
	path = os.path.dirname(sys.argv[0])
	if not path:
		path = str(os.getcwd())
		sys.argv[0] = path + "/" + str(sys.argv[0])

		print "set working path from " + str(os.getcwd()) + " to " + str(path)
		os.chdir(path)

	# parse settings
	parseSettings();

	# create commands list
	NAOCommand.addCmds()
	servermanager = ServerManager()

	# Endlosschleife
	while(True):
		servermanager.manage()
		sleep(2)

	print "ERROR: Program terminated"

