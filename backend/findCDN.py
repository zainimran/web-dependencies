import sys
import subprocess
from icecream import ic
import json
import tldextract
import requests

def main():
    input_p = sys.argv[1]

    input_f =  open(input_p, 'r')
    output_f = open('output.json', 'w')
    output_f2 = open('output-detailed.json', 'w')

    starting_line = int(sys.argv[2])
    lines_to_read = int (sys.argv[3])
    line_n = 0
    result = []
    detailed_result = []
    urls_parsed = set()

    for line in input_f:
        try:
            line_n += 1
            if line_n >= starting_line + lines_to_read:
                break
            elif line_n >= starting_line:
                ic(line_n)
                try:
                    url = line.strip('\n').split(' ')[2]
                except:
                    ic("Wrong file format")
                    continue

                extract = tldextract.extract(url)
                website_sld = extract.subdomain + '.' + extract.domain + '.' + extract.suffix
                website_tld = extract.domain + '.' + extract.suffix

                if website_sld not in urls_parsed:
                    urls_parsed.add(website_sld)
                else:
                    continue
                
                server_url = 'http://localhost:8080'
                payload = json.dumps({ 'url': url })
                headers = { 'content-type': 'application/json' }
                r = requests.post(server_url, data=payload, headers=headers)
                output = r.json()
                cdn_info = { 'website': website_sld, 'CDN output': output }
                detailed_result.append(cdn_info)
                cdn_records = output.get('everything')
                if cdn_records is None:
                    continue
                
                cdns = set()
                for record in cdn_records:
                    cnames = record['cnames']
                    cnames_tld = []
                    for cn in cnames:
                        extract = tldextract.extract(cn)
                        cn_tld = extract.domain + '.' + extract.suffix
                        cnames_tld.append(cn_tld)

                    if any(cname == website_tld for cname in cnames_tld):
                        cdn = record['cdn']
                        if cdn is not None:
                            cdns.add(cdn)
                
                if bool(cdns):
                    website_cdn = {'website': website_sld, 'CDNs': list(cdns)}
                    result.append(website_cdn)
    
        except subprocess.CalledProcessError as e:
                ic(str(e.output))
        except requests.exceptions.RequestException as e:
                ic(str(e))
    
    output_f.write(json.dumps(result, indent=4))
    output_f2.write(json.dumps(detailed_result, indent=4))

if __name__ == "__main__":
    main()
