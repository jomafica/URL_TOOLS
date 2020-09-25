import socket
import json
import requests
#  Example https://IP/api/v2/monitor/system/interface/?access_token=xwd8y3fb7QNf9HcGtNnm5NrGG5ky31

ip = input("IP: ")
token = "?access_token=xwd8y3fb7QNf9HcGtNnm5NrGG5ky31"
url = "https://" + str(ip) + "/api/v2/monitor/"
system_usage = "system/resource/usage/"
system_time = "system/time/"
system_vresource = "system/vdom-resource/"

response = requests.get(url + system_vresource + token, verify=False)
jparsed_dic = json.loads(response.content)
#print(type(jparsed_dic))
#print(response.url)

def iterate_dict(values):
    if isinstance(values, dict):
        for key, value in values.items():
            if isinstance(value, dict):
                print("____________________________________________")
                print(key + ":")
                print("____________________________________________")
                iterate_dict(value)
                print("\n")
            else:
                print(key + " : " + str(value))


iterate_dict(jparsed_dic['results'])




