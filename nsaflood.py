#!/usr/bin/env python
#
# Copyright 2014 Joel Cool-Panama <mr.jkuhl@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import random
import subprocess
import socket
import argparse
import linecache

import time

defaultTTL=8;
defaultKeyfileSize=256;
defaultConnectAttempts=5;

def selectPeer(unreachableHosts=[]):

	peersCount = subprocess.Popen(["wc", "-l", "/etc/nsaflood/peertab"], stdout=subprocess.PIPE).communicate()[0];
	peersCount = peersCount.split(" ")[0];

	maxPeerFindAttempts = 50;
	peerFindAttempts = 0;

	while True:
		selectedHost = linecache.getline('/etc/nsaflood/peertab', random.randrange(1, int(peersCount) + 1)).splitlines()[0];

		for host in unreachableHosts:

			if selectedHost == host:

				selectedHost = None;

		if selectedHost != None:

			break;

		peerFindAttempts += 1;

		if peerFindAttempts == maxPeerFindAttempts:

			return 1;

	return selectedHost;

def createGarbagefile(garbagefileSize=0):

	garbagefileName = subprocess.Popen(["mktemp", "--tmpdir", "nsaflood-garbagefile.XXXX"], stdout=subprocess.PIPE).communicate()[0];
	garbagefileName = garbagefileName.splitlines()[0];

	garbagefile = open(garbagefileName, 'w');
	garbagefile.write(os.urandom(garbagefileSize));
	garbagefile.close();

	return garbagefileName;

def createGarbagekey(garbagekeySize=0):

	garbagekeyName = subprocess.Popen(["mktemp", "--tmpdir", "nsaflood-garbagekey.XXXX"], stdout=subprocess.PIPE).communicate()[0];
	garbagekeyName = garbagekeyName.splitlines()[0];

	garbagekey = open(garbagekeyName, 'w');
	#change out to openssl rand 128
	garbagekey.write(os.urandom(garbagekeySize));
	garbagekey.close();

	return garbagekeyName;

def createTTLFile(garbagefileTTL=""):

	ttlFileName = subprocess.Popen(["mktemp", "--tmpdir", "nsaflood-ttlFile.XXXX"], stdout=subprocess.PIPE).communicate()[0];
	ttlFileName = ttlFileName.splitlines()[0];

	ttlFile = open(ttlFileName, 'w');
	ttlFile.write(str(garbagefileTTL));
	ttlFile.close();

	return ttlFileName

def encryptGarbagefile(garbagefile, garbagekey):

	newGarbagefile = createGarbagefile();

	subprocess.call(["openssl", "enc", "-aes-256-cbc", "-salt", "-in", garbagefile, "-out", newGarbagefile, "-pass", "file:" + garbagekey]);

	os.remove(garbagefile);

	return newGarbagefile;

def decryptGarbagefile(garbagefile, garbagekey):

	newGarbagefile = createGarbagefile();

	subprocess.call(["openssl", "enc", "-d", "-aes-256-cbc", "-in", garbagefile, "-out", newGarbagefile, "-pass", "file:" + garbagekey]);

	os.remove(garbagefile);

	return newGarbagefile;

def encryptTTLFile(ttlFile, garbagekey):

	newTTLFile = createTTLFile();

	subprocess.call(["openssl", "enc", "-aes-256-cbc", "-salt", "-in", ttlFile, "-out", newTTLFile, "-pass", "file:" + garbagekey]);

	os.remove(ttlFile);

	return newTTLFile;

def decryptTTLFile(ttlFile, garbagekey):

	newTTLFile = createTTLFile();

	subprocess.call(["openssl", "enc", "-d", "-aes-256-cbc", "-in", ttlFile, "-out", newTTLFile, "-pass", "file:" + garbagekey]);

	os.remove(ttlFile);

	return newTTLFile;

def encryptGarbagekey(garbagekey, publickey):

	newGarbagekey = createGarbagekey();

	subprocess.call(["openssl", "rsautl", "-encrypt", "-inkey", publickey, "-pubin", "-in", garbagekey, "-out", newGarbagekey]);

	os.remove(garbagekey);

	return newGarbagekey;

def decryptGarbagekey(garbagekey, privatekey):

	newGarbagekey = createGarbagekey();

	subprocess.call(["openssl", "rsautl", "-decrypt", "-inkey", privatekey, "-in", garbagekey, "-out", newGarbagekey]);

	os.remove(garbagekey);

	return newGarbagekey;


def readFileChunks(file, fileChunkSize=1024):

	filePointer = open(file, "r");

	while True:

		data = filePointer.read(fileChunkSize);

		if not data:

			break;

		yield data;

def startServer():

	server = socket.socket();

	host = socket.gethostname();
	port = 17666;

	server.bind((host, port));
	server.listen(5);

	while True:

		connection, address = server.accept();

		garbagefile = createGarbagefile();
		garbagekey = createGarbagekey();
		ttlFile = createTTLFile();

		garbagefilePointer = open(garbagefile, "a");
		garbagekeyPointer = open(garbagekey, "a");
		ttlFilePointer = open(ttlFile, "a");

		transferState = 0;

		while True:

			#get some rate limiting in here
			data = connection.recv(4096);

			if data == "\r\n\n":

				transferState += 1;

				if transferState == 1:

					ttlFilePointer.close();

					print "nsaflood server: ttlFile transfer finished.";

				elif transferState == 2:

					garbagefilePointer.close();

					print "nsaflood server: Garbagefile transfer finished."

				elif transferState == 3:

					print "nsaflood server: Garbagekey transfer finished."
					print "nsaflood server: Connection from " + str(address) + " finished";

					garbagekeyPointer.close();
					garbagekey = decryptGarbagekey(garbagekey, "/etc/nsaflood/privatekey");

					connection.close();

					break;

				continue

			if transferState == 0:

				#garbagefileTTL = int(data);
				ttlFilePointer.write(data);

			elif transferState == 1:

				garbagefilePointer.write(data);

			elif transferState == 2:

				garbagekeyPointer.write(data);

		ttlFile = decryptTTLFile(ttlFile, garbagekey);

		ttlFilePointer = open(ttlFile, "r");

		garbagefileTTL = ttlFilePointer.read(1);

		ttlFilePointer.close();

		garbagefile = decryptGarbagefile(garbagefile, garbagekey);

		os.remove(ttlFile);
		os.remove(garbagekey);

		subprocess.call(["nsaflood.py", "--garbage-file", garbagefile, "--ttl", str(garbagefileTTL)]);

def main():

	parser = argparse.ArgumentParser();

	parser.add_argument("-S", "--start-server", help="Start the listening server", action="store_true");
	parser.add_argument("-H", "--host", help="The destination host");
	parser.add_argument("-s", "--file-size", help="Size of the file to be generated in MiB");
	parser.add_argument("-b", "--bandwidth", help="Upload speed limit in Kib");
	parser.add_argument("-g", "--garbage-file", help="The file to be sent to the recipient.");
	parser.add_argument("-t", "--ttl", help="The time-to-live of the garbagefile");
	parser.add_argument("--version", help="Display version and copyright information", action="store_true");

	args = parser.parse_args();

	if args.start_server:
		startServer();
		return 0;

	if args.version:
		print "poop";
		return 0;

	if args.host:
		host = args.host;

		print "nsaflood: Host provided, host is " + host;

	else:
		print "nsaflood: Host not provided. Selecting host at random from peertab.";

		host = selectPeer();

		print "nsaflood: Host " + host + " selected.";

	if args.file_size:

		garbagefileSize = int(args.file_size) * 1024 * 1024;

	else:

		garbagefileSize = 1024 * 1024;

	if args.bandwidth:

		uploadBandwidth = args.bandwidth;

	else:

		uploadBandwidth = 2048;

	if args.garbage_file:

		garbagefile = args.garbage_file;

		print "nsaflood: Garbagefile provided, garbagefile is " + garbagefile;

	else:

		print "nsaflood: Garbagefile not provided. Creating new garbagefile filled with random data.";

		garbagefile = createGarbagefile(garbagefileSize);

		print "nsaflood: Garbagefile " + garbagefile + " created.";

	if args.ttl != None:

		print "nsaflood: TTL provided, decrementing by 1."

		garbagefileTTL = int(args.ttl) - 1;

		print "nsaflood: TTL decremented to " + str(garbagefileTTL);

	if args.ttl != None and int(args.ttl) == 0:

		print "nsaflood: The TTL of garbagefile " + garbagefile + "is 0.";
		print "nsaflood: The garbgefile and garbagekey will be deleted.";

		return 0;

	elif args.ttl == None:

		garbagefileTTL = defaultTTL;

		print "nsaflood: TTL not provided, set to " + str(defaultTTL) + ".";

	server = socket.socket();
	port = 17666;

	connectAttempts = 0;
	unreachableHosts = [];

	while True:

		try:

			server.connect((host, port));

			connectAttempts = None;
			unreachableHosts = None;
			break;

		except socket.error:

			connectAttempts += 1;

			if connectAttempts == defaultConnectAttempts:

				print "nsaflood: failed to connect to a host " + str(defaultConnectAttempts) + " times.";
				print "nsaflood: Now exiting.";

				os.remove(garbagefile);

				return 1;

			print "nsaflood: The connection to host " + host + " timed out. nsaflood will retry with a new host";

			unreachableHosts.append(host);
			host = selectPeer(unreachableHosts);

			if host.isdigit():

				print "nsaflood: selectPeer() has attempted to find a new, random peer, but failed.";
				print "nsaflood: Now exiting."

				os.remove(garbagefile);

				return 1;

			print "nsaflood: Host " + host + " selected.";

	publickey = "/etc/nsaflood/pubkeys/" + host;
	garbagekey = createGarbagekey(defaultKeyfileSize);
	ttlFile = createTTLFile(garbagefileTTL);

	ttlFile = encryptTTLFile(ttlFile, garbagekey);
	garbagefile = encryptGarbagefile(garbagefile, garbagekey);
	garbagekey = encryptGarbagekey(garbagekey, publickey);

	#get some rate limiting in here
	#encrypt ttl
	#server.send(str(garbagefileTTL));
	for data in readFileChunks(ttlFile, 4096):

		server.send(data);

	time.sleep(1);

	server.send("\r\n\n");

	time.sleep(1);

	for data in readFileChunks(garbagefile, 4096):

		server.send(data);

	time.sleep(1);

	server.send("\r\n\n");

	time.sleep(1);

	for data in readFileChunks(garbagekey, 4096):

		server.send(data);

	time.sleep(1);

	server.send("\r\n\n");

	print "Finished file transfer.";

	server.close();

	os.remove(ttlFile);
	os.remove(garbagefile);
	os.remove(garbagekey);

if __name__ == "__main__":

	main()

