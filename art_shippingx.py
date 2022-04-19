import requests
import json
import platform
import subprocess
import os
from fabric import Connection
from dotenv import load_dotenv
load_dotenv()


def get_xi_data(url):
    response = requests.get(url)
    data = json.loads(response.text)
    data = data[0]['fields']
    return data


""" 
* sends SMS alerts
* @params url, params
* return dict
"""


def alert(url, params):
    headers = {'Content-type': 'application/json; charset=utf-8'}
    try:
       r = requests.post(url, json=params, headers=headers)
    except requests.exceptions.Timeout as e:
        print("timeout error: ", e)
        return False
    except requests.exceptions.TooManyRedirects as e:
        print("too many redirects: ", e)
        return False
    except requests.exceptions.RequestException as e:
        print("catastrophic error: ", e)
        return False
    return r


recipients = ["+265998006237", "+265991450316", "+265995246144", "+265998276712", "+265992182669"] 

cluster = get_xi_data('http://10.44.0.52/sites/api/v1/get_single_cluster/1')

for site_id in cluster['site']:
    site = get_xi_data('http://10.44.0.52/sites/api/v1/get_single_site/' + str(site_id))

    # functionality for ping re-tries
    count = 0

    while (count < 3):

        # lets check if the site is available
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        if subprocess.call(['ping', param, '1', site['ip_address']]) == 0:

            # ship art updates to remote site
            push_art = "rsync " + "-r $WORKSPACE/BHT-Core/apps/ART/ " + site['username'] + "@" + site['ip_address'] + ":/var/www/html/BHT-Core/apps"
            os.system(push_art)
            
            # ship core and art setup script to remote site
            push_art_script = "rsync " + "-r $WORKSPACE/art_setup.sh " + site['username'] + "@" + site['ip_address'] + ":/var/www/html/BHT-Core/apps/ART"
            os.system(push_art_script)

            # run core and art setup script
            run_art_script = "ssh " + site['username'] + "@" + site[
                'ip_address'] + " 'cd /var/www/html/BHT-Core/apps/ART && ./art_setup.sh'"
            os.system(run_art_script)
            result = Connection("" + site['username'] + "@" + site['ip_address'] + "").run(
                'cd /var/www/html/BHT-Core/apps/ART && git describe', hide=True)
            msg = "{0.stdout}"

            version = msg.format(result).strip()

            art_version = "v4.15.3"

            if art_version == version:
                msgx = "Hi there,\n\nDeployment of ART to " + version + " for " + site[
                    'name'] + " completed succesfully.\n\nThanks!\nEGPAF HIS."
            else:
                msgx = "Hi there,\n\nSomething went wrong while checking out to the latest ART version. Current version is " + version + " for " + \
                       site['name'] + ".\n\nThanks!\nEGPAF HIS."

            # send sms alert
            for recipient in recipients:
                msg = "Hi there,\n\nDeployment of ART to " + version + " for " + site['name'] + " completed succesfully.\n\nThanks!\nEGPAF HIS."
                params = {
                    "api_key": os.getenv('API_KEY'),
                    "recipient": recipient,
                    "message": msgx
                }
                alert("http://sms-api.hismalawi.org/v1/sms/send", params)

            count = 3
        else:
            count = count + 1

            # make sure we are sending the alert at the last pint attempt
            if count == 3:
                for recipient in recipients:
                    msg = "Hi there,\n\nDeployment of ART to v4.15.3 for " + site['name'] + " failed to complete after several connection attempts.\n\nThanks!\nEGPAF HIS."
                    params = {
                        "api_key": os.getenv('API_KEY'),
                        "recipient": recipient,
                        "message": msg
                    }
                    alert("http://sms-api.hismalawi.org/v1/sms/send", params)
