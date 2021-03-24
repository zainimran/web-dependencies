 # To run, `python findNS.py <input_file> <start_index> <number_of_entries>`

import os
import sys
import subprocess
import time
import tldextract
import re
import json


def extract_site(website):
    tld = tldextract.extract(website)
    site = tld.domain + "." + tld.suffix
    return site

def main():

    filename = sys.argv[1]
    start = int(sys.argv[2])
    entries = int (sys.argv[3])

    timestr = time.strftime("%Y%m%d-%H%M%S")
    output_path = './outputs/output-{0}.json'.format(timestr)

    f = open(filename, 'r')
    of = open(output_path,"w")

    edges = []
    nodes = []
    
    count = 1
    for line in f:
        try:
            if count >= start + entries:
                break
            if count >= start:
                print(count)
                line = line.strip('\n').split(' ')[2]
                line = extract_site(line)
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

                    if("ANSWER: 0" in output):
                        output = subprocess.check_output(['dig', "ns", "@8.8.8.8", line, "+short"])
                        output = str(output,"utf-8")
                    
                    output_array = output.split('\n')[:-1]

                    # classifying if a nameserver is private or third-party w.r.t. a domain
                    for d in output_array:
                        result = ''
                        dns_site = extract_site(d)
                        output = subprocess.check_output(['dig', "soa", "@8.8.8.8", dns_site, "+short"])
                        output = str(output,"utf-8")
                        contact_addrs = output.split(' ')[1]

                        provider_domain = tldextract.extract(contact_addrs).domain
                        
                        website_domain = tldextract.extract(line).domain
                        if (website_domain == provider_domain):
                            result = 'private'
                        else:
                            result = 'third-party'
                            nodes.extend([provider_domain, line])
                            edges.append((provider_domain, line))

                        of.write(line + "\t" + d + "\t" + result + "\n")
                
            count += 1
        except subprocess.CalledProcessError as e:
            pass
    
    n_map = {}
    if nodes:
        nodes = list(set(nodes))
        id_increment = 1
        for i, n in enumerate(nodes):
            n_id = 'n'+ str(id_increment)
            nodes[i] = {
                "id": n_id,
                "label": str(n),
                "color":'#00f'
            }

            # if not provider, then node color is yellow
            if n.find('.') != -1 :
                nodes[i]['color'] = '#dce622'
            n_map[n] = n_id
            id_increment += 1

    if edges:
        edges = list(set(edges))
        id_increment = 1
        for i, e in enumerate(edges):
            edges[i] = {
                "id": 'e'+ str(id_increment),
                "source": n_map[e[0]],
                "target": n_map[e[1]],
                "label": 'DNS',
            }
            id_increment += 1

    jf_path = '../frontend/src/graphData.json'
    jf_path_copy = '../frontend/src/graph-data/graphData-{0}.json'.format(timestr)
    jf = open(jf_path, "w")
    jf_copy = open(jf_path_copy, 'w')
    g_object = {
        'nodes': nodes,
        'edges': edges 
    }
    jf.write(json.dumps(g_object, indent=4))
    jf_copy.write(json.dumps(g_object, indent=4))


if __name__ == "__main__":
    main()
