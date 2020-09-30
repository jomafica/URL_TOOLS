import requests, json, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def iterate_dict(values):
    json_body = []
    for d in jparsed_dic:
        if isinstance(d,dict):
            for keyz, valuez in d.items():
                tags = {}
                if isinstance(valuez, dict):
                    for keyy, valuey in valuez.items():
                        json_line = {}
                        if isinstance(valuey, dict):
                            json_line["measurement"] = keyy
                            fields = {}
                            for keyx, valuex in valuey.items():
                                fields[keyx] = valuex
                            json_line['tags'] = tags
                            json_line['fields'] = fields
                            json_body.append(json_line)
                        else:
                            pass
                            #print(keyy + ":" + str(valuey))
                else:
                    tags[keyz] = valuez
                    #print(keyz + ":" + str(valuez))
    return json_body

def main():
    json_body = iterate_dict(jparsed_dic)
    print(json_body)
    for x in json_body:
        #print(x)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = x
        write_api.write(bucket, org, data)


if __name__ == "__main__":
    token = "wZHGNmVTp7yZWBm3abuTgmLEiCzDOcVdfw1EndTcefGxi5LHX9sy6uMKv5NoFDaiE2RCIrx-lsu1iSiU7afWOg=="
    org = "c3c0eae17214c20e"
    bucket = "8ef9a01e310a0902"
    client = InfluxDBClient(url="http://10.36.0.187:9999", token=token)

    ip = ("10.36.0.57")
    token = "?access_token=xwd8y3fb7QNf9HcGtNnm5NrGG5ky31&vdom=*"
    url = "https://" + str(ip) + "/api/v2/monitor/"
    system_usage = "system/resource/usage/"
    system_time = "system/time/"
    system_vresource = "system/vdom-resource/"

    response = requests.get(url + system_vresource + token, verify=False)
    jparsed_dic = json.loads(response.content)

    parsed_json = {}
    main()
    #while response.status_code == 200:
#
    #    time.sleep(5)

