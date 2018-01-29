##################################
#Ping Utility
### Made by Hiten Sethiya
import requests
import csv
import time

url = "http://www.spfld.com/cgi-bin/ping"
trace_url = "https://api.hackertarget.com/mtr/?q="

hosts = [#hosts
]
sizes = ["64", "128", "256", "512", "1024", "2048"]
for host in hosts:
    query = {'q':host}
    response = requests.request("GET", trace_url, params=query)
    with open('ping_traceroutes.txt','a') as tr_record:
        tr_record.write("-------------------------\n",host,"Local Time ::",time.strftime("%d %b %Y %H:%M:%S", time.localtime()),"\n")
        tr_record.write(response.text)
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
            fieldnames = ['Host', 'Frame Size', 'RTT Min', 'RTT Avg', 'RTT Max', 'RTT Mdev', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Host': host,
                             'Frame Size': size,
                             'RTT Min': response.text.splitlines()[i].split('/')[3].split('=')[1].strip(),
                             'RTT Avg': response.text.splitlines()[i].split('/')[4],
                             'RTT Max': response.text.splitlines()[i].split('/')[5],
                             'RTT Mdev': response.text.splitlines()[i].split('/')[6].split()[0].strip(),
                             'Time': time.strftime("%d %b %Y %H:%M:%S", time.localtime())
                             })
print('Finished! Check the results in \'ping_results.csv\' Enjoy!!')
