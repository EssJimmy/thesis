import os
from configparser import ConfigParser

DIR = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
parser = ConfigParser()
parser.read(os.path.join(DIR, "robot.conf"))
ip = parser.get('xArm', 'ip')
print(ip)