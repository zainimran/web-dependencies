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

    starting_line = int(sys.argv[2])
    lines_to_read = int (sys.argv[3])
    line_n = 0
    result = []
    try:
        for line in input_f:
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
                
                server_url = 'http://localhost:8080'
                payload = json.dumps({ 'url': url })
                headers = { 'content-type': 'application/json' }
                r = requests.post(server_url, data=payload, headers=headers)
                output = r.json()
                extract = tldextract.extract(url)
                website_sld = extract.subdomain + '.' + extract.domain + '.' + extract.suffix
                # cdn_info = {website_sld: {k: output[k] for k in ('assetcdn', 'basecdn')}}
                cdn_info = { 'website': website_sld, 'CDN output': output }
                result.append(cdn_info)

        output_f.write(json.dumps(result, indent=4))

    except subprocess.CalledProcessError as e:
            ic(str(e.output))
            pass

if __name__ == "__main__":
    main()
