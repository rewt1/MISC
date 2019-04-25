import re
import sys
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--errorlog", help="specify path to error_log file",required=True)
parser.add_argument('-p', help='include payload in result', required=False,action='store_true')
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    exit()

file = args.errorlog

remodsec = '.*ModSecurity:.+\[id.+?\"(?P<id>.+?)\"].+\[msg.+?\"(?P<msg>.+?)\"].+?Matched Data:.+found\s+within\s+(?P<element>.+?)\:\s+(?P<payload>.+?)\"].*?hostname\s"(?P<hostname>.+?)".*?uri\s"(?P<uri>.+?)"'

try:
    with open(file,"r") as f:
        f.read()
except Exception as e:
    print("The specified file is not accessible. " + str(e))
    exit()

def modsec_parse(line,regex):
    try:
        r = re.match(regex,line).groupdict()
        return r
    except:
        return False


with open(file) as rawlog:
    for line in rawlog:
        try:
            dic = modsec_parse(line,remodsec)
            if dic == False:
                continue
            for attr in ["id", "msg", "element", "payload", "hostname", "uri"]:
                if not attr in dic:
                    dic[obj] = "--------"
            if args.p:
                print("{0:<10}{1:<50}{2:<30}{3:<60}{4:<20}{5:20}".format(dic["id"],dic["msg"],dic["element"],dic["payload"],dic["hostname"],dic["uri"]))
            else:
                print("{0:<10}{1:<90}{2:<30}{3:<20}{4:20}".format(dic["id"],dic["msg"],dic["element"],dic["hostname"],dic["uri"]))
        except Exception as e:
            print("ERROR: " + str(e))
            pass
