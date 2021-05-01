import requests, json, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

def iteratev2(values):
    json_body = []
    tags = {}
    for key , value in values.items():
        if not isinstance(value, dict):
            tags[key] = value


    for keyr , valuer in values['results'].items():
        #print(keyr)
        if isinstance(values['results'][keyr], dict):
            json_line = {}
            json_line['measurement'] = keyr
            json_line['tags'] = tags
            fields = {}
            for keyf , valuef in valuer.items():
                fields[keyf] = valuef
            json_line['fields'] = fields
            #print(json_line)
            json_body.append(json_line)
        else:
            json_line = {}
            json_line['measurement'] = keyr
            json_line['tags'] = tags
            json_line['fields'] = {keyr:valuer}
            #print(json_line)
            json_body.append(json_line)
    return json_body


def write__to_influx(json_body):
    for x in json_body:
        print(x)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = x
        write_api.write(bucket, org, data)

def main():
    json_body = {}
    if isinstance(jparsed_dic, list):
        for x in jparsed_dic:
           json_body = iteratev2(x)
           write__to_influx(json_body)
    else:
        json_body = iteratev2(jparsed_dic)
        write__to_influx(json_body)
    #print(json_body)



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

    while response.status_code == 200:
        main()
        time.sleep(5)

