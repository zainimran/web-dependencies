 # To run, `cd backend && pipenv shell; python findNS.py <input_file> <start_index> <number_of_entries>`

import os
import sys
import subprocess
import time
import tldextract
import re
import json
import random

def initialization():
    input_path = sys.argv[1]

    timestr = time.strftime('%m%d-%H%M')
 
    output_path = './outputs/{0}'.format(timestr)
    graph_path = '../frontend/src/graphData.json'
    graph_path_dup = '../frontend/src/data/{0}.json'.format(timestr)

    file_handlers = {
        'input_file': open(input_path, 'r'),
        'output_file': open(output_path, 'w'),
        'graph_file': open(graph_path, 'w'),
        'graph_file_dup': open(graph_path_dup, 'w')
    }

    return file_handlers

def extract_url_from_hispar_list(line):
    return line.strip('\n').split(' ')[2]

def extract_domain(url, full_domain=False):
    tld = tldextract.extract(url)
    domain = tld.domain + '.' + tld.suffix
    if full_domain:
        domain = tld.subdomain + '.' + domain
    return domain

def get_string_of_ns(domain):
    string_of_ns = subprocess.check_output(['dig', 'ns', '@8.8.8.8', domain, '+short'])
    string_of_ns = str(string_of_ns, 'utf-8')

    if string_of_ns == '':
        domain = extract_domain(domain)
        string_of_ns = subprocess.check_output(['dig', 'ns', '@8.8.8.8', domain, '+short'])
        string_of_ns = str(string_of_ns,"utf-8")

    return string_of_ns

def run_dig_for_domain(domain, output_file):
    output = subprocess.check_output(['dig', domain, '+short'])
    output = str(output, 'utf-8')
    if 'NXDOMAIN' in output:
        output_file.write(f'{domain} -> NXDOMAIN\n')
        return
    elif 'SERVFAIL' in output:
        output = subprocess.check_output(['dig', '@8.8.8.8', domain, '+short'])
        output = str(output, 'utf-8')
        if 'NXDOMAIN' in output:
            output_file.write(f'{domain} -> NXDOMAIN\n')
            return
        elif 'SERVFAIL' in output:
            output_file.write(f'{domain} -> SERVFAIL\n')
            return
    
    string_of_ns = get_string_of_ns(domain)
    
    if string_of_ns != '':
        list_of_ns = string_of_ns.split('\n')[:-1]
        return list_of_ns

def get_ns_provider_domain_root_from_soa(ns_domain):
    output = subprocess.check_output(['dig', 'soa', '@8.8.8.8', ns_domain, '+short'])
    output = str(output,"utf-8")
    if len(output) > 0:
        ns_provider_contact = output.split(' ')[1]
        ns_provider_root_domain = tldextract.extract(ns_provider_contact).domain
        return ns_provider_root_domain

def classify_ns(ns, domain):
    is_private = False

    ns_domain = extract_domain(ns)
    ns_domain_root = tldextract.extract(ns).domain

    domain_root = tldextract.extract(domain).domain

    if ns_domain == domain:
        is_private = True
    elif ns_domain_root == domain_root:
        is_private = True
    else: 
        ns_domain_root = get_ns_provider_domain_root_from_soa(ns_domain)
        if ns_domain_root == domain_root:
            is_private = True
    
    classification = 'Public'
    if is_private:
        classification = 'Private'
    
    return classification, ns_domain_root, domain

def main():

    file_handlers = initialization()
    
    starting_line = int(sys.argv[2])
    lines_to_read = int (sys.argv[3])
    line_number = 1

    input_file, output_file, graph_file, graph_file_dup = [
        file_handlers[k] for k in (
            'input_file', 
            'output_file', 
            'graph_file', 
            'graph_file_dup'
            )
        ]

    edges = []
    nodes = []

    for line in input_file:
        try:
            if line_number >= starting_line + lines_to_read:
                break
            elif line_number >= starting_line:
                print(line_number)
                try:
                    url = extract_url_from_hispar_list(line)
                except:
                    print("Wrong file format")
                    continue

                domain = extract_domain(url, full_domain=True)
                list_of_ns = run_dig_for_domain(domain, output_file)
                if list_of_ns is not None:
                    for ns in list_of_ns:    
                        classification, ns_domain_root, domain = classify_ns(ns, domain)

                        nodes.extend([ns_domain_root, domain])
                        edges.append((ns_domain_root, domain))
                        
                        output_file.write(domain + "\t" + ns.rstrip('.') + "\t" + classification + "\n")
            
            line_number += 1

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
                "color":'#00f',
                "x": random.random(),
                "y": random.random()
            }

            # if node represents a NS provider, then we set its color to #dce622
            if n.find('.') == -1 :
                nodes[i]['color'] = '#dce622'
            
            n_map[n] = n_id
            id_increment += 1

    if edges:
        edges = list(set(edges))
        id_increment = 1
        for i, e in enumerate(edges):
            edges[i] = {
                "id": id_increment,
                "source": n_map[e[0]],
                "target": n_map[e[1]],
                "label": 'DNS',
            }
            id_increment += 1

    graph_object = {
        'nodes': nodes,
        'edges': edges 
    }
    graph_file.write(json.dumps(graph_object, indent=4))
    graph_file_dup.write(json.dumps(graph_object, indent=4))

if __name__ == "__main__":
    main()
