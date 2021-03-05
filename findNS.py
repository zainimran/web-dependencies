 # To run, python dns.py inputfile filetowriteIn start_index number_of_entries 

import os
import sys
import subprocess
import time
import tldextract


def main():

    filename = sys.argv[1]
    output = sys.argv[2]

    start = int(sys.argv[3])
    entries = int (sys.argv[4])
    f = open(filename, 'r')
    of = open(output,"w")
    count = 0
    for line in f:
        result = "" 
        try:
            print(count)
            if count >= start + entries:
                break
            if count >= start:
                line = line.strip('\n').split(' ')[2]
                line = extract_domain(line)
                output = subprocess.check_output(['dig', line])
                output = str(output,"utf-8")
                if("NXDOMAIN" in output):
                    of.write(f'{line},NXDOMAIN\n')
                elif("SERVFAIL" in output):
                    # print (f"{line},SERVFAIL")
                    output = subprocess.check_output(['dig', "@8.8.8.8",line])
                    output = str(output,"utf-8")
                    if("NXDOMAIN" in output):
                        of.write((f"{line},NXDOMAIN\n"))
                    if("SERVFAIL" in output):
                        of.write(f"{line},SERVFAIL\n")
                else:
                    # only keeping the list of authoritative nameservers
                    output = subprocess.check_output(['dig', "ns", "@8.8.8.8", line, "+short"])
                    output = str(output,"utf-8")
                    output_array = output.split('\n')[:-1]

                    # classifying if a nameserver is private or third-party w.r.t. a domain
                    for d in output_array:
                        d = d.rstrip('.')
                        result = classify(d, line)
                        of.write(line + "\t" + d + "\t" + result + "\n")
                        
                    if("ANSWER: 0" in output):
                        domain = extract_domain(line)
                        output = subprocess.check_output(['dig', "ns","@8.8.8.8",domain])
                        output = str(output,"utf-8")

            count += 1
        except subprocess.CalledProcessError as e:
            pass

def extract_domain(website):
    tld = tldextract.extract(website)
    domain = tld.domain + "." + tld.suffix
    return domain

def classify(nameserver, website):
    domain = extract_domain(website)
    if (website == domain):
        return 'private'
    return 'third-party'

if __name__ == "__main__":
    main()
