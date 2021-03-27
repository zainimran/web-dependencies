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
    graph_path = '../outputs/graphs/{0}'.format(timestr)
    graph_path_dup = '../static-frontend/data/graphData.json'

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
    subdomains_to_ignore = ['www', '']
    if full_domain and tld.subdomain not in subdomains_to_ignore:
        domain = tld.subdomain + '.' + domain
    return domain

def get_string_of_ns(domain):
    string_of_ns = subprocess.check_output(['dig', 'ns', '@8.8.8.8', domain, '+short'])
    string_of_ns = str(string_of_ns, 'utf-8')

    if string_of_ns == '':
        domain_short = extract_domain(domain)
        string_of_ns = subprocess.check_output(['dig', 'ns', '@8.8.8.8', domain_short, '+short'])
        string_of_ns = str(string_of_ns, 'utf-8')

    return string_of_ns

def can_get_domain_info(domain, output_file):
    output = subprocess.check_output(['dig', domain, '+short'])
    output = str(output, 'utf-8')
    if 'NXDOMAIN' in output:
        output_file.write(f'{domain}\tNXDOMAIN\n')
        return False
    elif 'SERVFAIL' in output:
        output = subprocess.check_output(['dig', '@8.8.8.8', domain, '+short'])
        output = str(output, 'utf-8')
        if 'NXDOMAIN' in output:
            output_file.write(f'{domain}\tNXDOMAIN\n')
            return False
        elif 'SERVFAIL' in output:
            output_file.write(f'{domain}\tSERVFAIL\n')
            return False
    return True

def get_ns_provider_domain_root_from_soa(ns_domain):
    output = subprocess.check_output(['dig', 'soa', '@8.8.8.8', ns_domain, '+short'])
    output = str(output,"utf-8")
    if len(output) > 0:
        ns_provider_contact_array = output.split(' ')
        if len(ns_provider_contact_array) > 2:
            ns_provider_contact = ns_provider_contact_array[1]
            ns_provider_domain_root = tldextract.extract(ns_provider_contact).domain
            return ns_provider_domain_root

def classify_ns(ns, domain):
    is_private = False

    ns_domain = extract_domain(ns)
    ns_domain_root = tldextract.extract(ns).domain

    domain = extract_domain(domain)
    domain_root = tldextract.extract(domain).domain

    if ns_domain == domain:
        is_private = True
    elif ns_domain_root == domain_root:
        is_private = True
    else:
        ns_domain_root = get_ns_provider_domain_root_from_soa(ns_domain)
        if ns_domain_root is None:
            return
        if ns_domain_root == domain_root:
            is_private = True
    
    classification = 'Public'
    if is_private:
        classification = 'Private'
    
    return classification, ns_domain_root

def main():

    file_handlers = initialization()
    
    starting_line = int(sys.argv[2])
    lines_to_read = int (sys.argv[3])
    line_number = 0

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
    domains = set()

    for line in input_file:
        line_number += 1
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
                
                if domain not in domains:
                    domains.add(domain)
                else:
                    continue

                if not can_get_domain_info(domain, output_file):
                    continue
                
                string_of_ns = get_string_of_ns(domain)
                if string_of_ns != '':
                    list_of_ns = string_of_ns.split('\n')[:-1]

                    if list_of_ns is not None:
                        for ns in list_of_ns:    
                            classification, ns_domain_root = classify_ns(ns, domain)

                            nodes.extend([ns_domain_root, domain])
                            edges.append((ns_domain_root, domain))
                            
                            output_file.write(domain + "\t" + ns.rstrip('.') + "\t" + classification + "\n")
            
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
                "color":'#000',
                "x": random.random(),
                "y": random.random()
            }

            # if node represents a NS provider, then we set its color to #00f
            if n.find('.') == -1 :
                nodes[i]['color'] = '#00f'
            
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
