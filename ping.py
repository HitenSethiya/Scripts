##################################
# Ping Utility
### Made by Hiten Sethiya
import requests
import csv
import time

url = "http://www.spfld.com/cgi-bin/ping"
trace_url = "https://api.hackertarget.com/mtr/"

hosts = ["flipkart.com"#Add more
        ]
sizes = ["64", "128", "256", "512", "1024", "2048"]
for host in hosts:
    query = {'q': host}
    response = requests.request("GET", trace_url, params=query)
    with open('ping_traceroutes.txt', 'a') as tr_record:
        tr_record.write("----------------------------------\n"+host + " Local Time :: " + str(time.strftime("%d %b %Y %H:%M:%S", time.localtime())) + "\n")
        tr_record.write(response.text)
    print("printed traceroute")
    ## Because only multiple size data of only one host is required 
    if(host==hosts[0]):
        sizes = ["64", "128", "256", "512", "1024", "2048"]
    else:
        sizes = ["64"]
    for size in sizes:
        querystring = {"remote_host": host, "dns": "on", "count": "20", "size": size}
        response = requests.request("GET", url, params=querystring)
        flag = 1
        for index, line in enumerate(response.text.splitlines()):
            if line[0:3] == 'rtt':
                i = index
                flag = 0
        if flag == 1:
            print(host, size, ' Failed')
            continue
        print(host, size, 'Done', 'response = ', response.text.splitlines()[i])
        with open('ping_results.csv', 'a') as csvfile:
            fieldnames = ['Host', 'Frame Size','Packets Recieved','Packets Transmitted','Packet loss','Total Time', 'RTT Min', 'RTT Avg', 'RTT Max', 'RTT Mdev', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Host': host,
                             'Frame Size': size,
                             'Packets Recieved':response.text.splitlines()[i-1].split()[3].strip(),
                             'Packets Transmitted':response.text.splitlines()[i-1].split()[0].strip(),
                             'Packet loss':response.text.splitlines()[i-1].split()[5].strip(),
                             'Total Time':response.text.splitlines()[i-1].split()[9].strip(),
                             'RTT Min': response.text.splitlines()[i].split('/')[3].split('=')[1].strip()+'ms',
                             'RTT Avg': response.text.splitlines()[i].split('/')[4]+'ms',
                             'RTT Max': response.text.splitlines()[i].split('/')[5]+'ms',
                             'RTT Mdev': response.text.splitlines()[i].split('/')[6].split()[0].strip()+'ms',
                             'Time': time.strftime("%d %b %Y %H:%M:%S", time.localtime())
                             })
print('Finished! Check the results in \'ping_results.csv\' and \'ping_traceroutes\' Enjoy!!')
