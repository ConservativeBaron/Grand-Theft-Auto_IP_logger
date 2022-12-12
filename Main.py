# Import the necessary modules
import sys
import time
import subprocess
import requests
import re
from statistics import mode

# Define a function that returns the mode of a given list
def most_common(List):
    return(mode(List))

# Get the user IP from the command line arguments
userip = sys.argv[1]

# Print a message while we wait for the lobby info to be retrieved
print("Getting Lobby Info Please Wait!")
time.sleep(1)

# Initialize some empty lists to store the results of the tcpdump command
tcpdump_results = []
ips_found = []

# Generate a filename for the tcpdump output based on the current timestamp
dump_name = str(round(time.time()))+'.pcap'

# Run the tcpdump command, filtering the output to include only the desired IP addresses
# and save the output to the file with the generated name
tcpdump = subprocess.getoutput(f'tcpdump -i tun0 src {userip} and udp and greater 45 and not host 65.55.42.183 and not host 185.34.106.11 and not host 24.190.220.30 and not 70.65.127.36 and not host 73.104.127.227 and not dst net 10.8.0.0/16 and not net 192.168.0.0/16 -nn -c 250 > '+dump_name)

# Wait for the tcpdump command to complete
time.sleep(1)

# Open the file containing the tcpdump output and read its contents
with open(dump_name, "r") as f:
    dump = f.readlines()
    # Iterate over each line in the file
    for line in dump:

        # If the line contains the string 'IP', process it
        if 'IP' in line:

            # Split the line by spaces, extract the fourth element (the IP address),
            # and split that by dots to get the individual octets
            liine = line.split(" ")[4]
            aliine = liine.split(".")[0]
            bliine = liine.split(".")[1]
            cliine = liine.split(".")[2]
            dliine = liine.split(".")[3]

            # Concatenate the octets back together to form the IP address
            # and append it to the list of IPs found
            eliine = aliine+"."+bliine+"."+cliine+"."+dliine
            tcpdump_results.append(eliine)

def display_ips(tcpdump_results):
    # Check if any IPs were found in the tcpdump results
    if len(tcpdump_results) == 0:
        print("No Lobby Found")
        subprocess.getoutput(f"pkill -f {userip}")
        return
        
    print("Lobby Has Been Found!")
    
    # Create a list of unique IPs found in the tcpdump results
    ips_found = list(set(tcpdump_results))
    
    print("--------------------------------------------------------------------------------")
    print("Player IP's Found In Your Lobby [{}/32] (not including youself)".format(len(ips_found)))
    print("Here Are The Listed IP's In GTA 5 Lobby")
    print(" ")
    print("Scanning GTA 5 Lobby")
    print(" ")
    
    # Print a table header for the IPs
    print("       IP       ||    COUNTRY     ||  STATE/REGION  ||      CITY      ||         ISP          ")
    print("----------------||----------------||----------------||----------------||----------------------")
    
    # For each IP in the list of unique IPs
    for nongeo in ips_found:
        # Make a request to an IP geolocation API
        res = requests.get("http://ip-api.com/line/"+nongeo+"?fields=country,regionName,city,isp")
        
        if res.status_code == 200:
            # Parse the response to extract the country, region, city, and ISP
            loc = res.text
            country, regionName, city, isp = loc.splitlines()[0:4]
            
            # Filter out known service provider IPs
            if re.search('Google|Microsoft|Take-two Interactive Software|Take-two|Interactive|Software|Amazon|Cloudflare|i3D.net B.V', isp):
                pass
            else:
                # Print the IP and its geolocation information
                print(f"{nongeo.ljust(15, ' ')} || {country.ljust(14, ' ')} || {regionName.ljust(14, ' ')} || {city.ljust(14, ' ')} || {isp}")
       
        else:
            # If the API request fails, print an error message
            print(f"{nongeo} || Failed To Locate IP (Api request failure)")
    
    print("--------------------------------------------------------------------------------")

# Displaying IPs captured
display_ips(tcpdump_results)

# Finalizing the script
subprocess.getoutput(f"rm -rf ./{dump_name}")
input("Press ENTER to exit script...")
