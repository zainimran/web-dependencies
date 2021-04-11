import sys
import subprocess
from icecream import ic
import json
import tldextract

def main():
    input_p = sys.argv[1]

    input_f =  open(input_p, 'r')
    output_f = open('output.json', 'w')

    starting_line = int(sys.argv[2])
    lines_to_read = int (sys.argv[3])
    line_n = 0
    result = []
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
            
            try:
                output = subprocess.check_output(['docker', 'run', '-it', 'turbobytes/cdnfinder', 'cdnfindercli', '--full', url])
                output = str(output, 'utf-8')
                output = output.split('\r\n', 1)[1]
                output = json.loads(output)
                extract = tldextract.extract(url)
                website_sld = extract.subdomain + '.' + extract.domain + '.' + extract.suffix
                cdn_info = {website_sld: {k: output[k] for k in ('assetcdn', 'basecdn')}}
                ic(cdn_info)
                result.append(cdn_info)
            except subprocess.CalledProcessError as e:
                ic(str(e.output))
                pass
    output_f.write(json.dumps(result))

if __name__ == "__main__":
    main()
