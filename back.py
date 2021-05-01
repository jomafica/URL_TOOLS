import re
import time
import os.path
import sys
import requests
import json
import concurrent.futures

ipliist = []

class Cache:

    def directory(self):

        cachepath = self.path() + "\\cache.txt"

        return cachepath

    def path(self):

        direct = "\\Result"
        currentdir = os.getcwd()
        path = currentdir + direct

        try:
            os.mkdir(path)

        except:
            pass

        return path

    def create_cache(self):

        try:

            ca = open(self.directory(), 'w+')

            return ca

        except Exception as e:
            print(e)

    def open_cache(self):

        try:

            ca = open(self.directory(), 'a+')

            return ca

        except Exception as e:
            print(e)

    def close_cache(self):
        self.directory().closefile()

    def readliness(self):
        return open(self.directory(), 'r')

def workers_head(func_to_call, arg, cachess):

    lst = []

    resuslfd = []

    for i in arg:
        lst = i

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:

        future = {executor.submit(func_to_call, ip, cachess):ip for ip in lst}

        for futuresult in concurrent.futures.as_completed(future):

            try:

                if futuresult.result():

                    resuslfd.append(futuresult.result())

            except Exception as e:
                print("Workers_level:",e)

        return resuslfd

def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def open_iplist(ipslist, cache):
    try:
        ids = 0

        temp_jbodys = hit_cache(ipslist,cache)
        return_jbody = []

        for dics in temp_jbodys:
            ids += 1
            updict = {"id" : ids}
            updict.update(dics)
            return_jbody.append(updict)

        return return_jbody
    except Exception as e:
        print(e)
        sys.exit(1)

def hit_cache(file_to_handle, cache):

    final_jbody = []
    currentiplst = []
    existiplst = []
    existlst = []
    cha = cache.open_cache()

    if os.path.getsize(cache.directory()) == 0: 

        return workers_head(request, file_to_handle.values(), cha)

    else:        

        for k,iiip in file_to_handle.items():

            for ip in iiip:

                currentiplst.append(ip.strip())
                my_regex = r"{0}".format(ip.strip())
                
                try:

                    for zx in cache.readliness().readlines():

                        temp_search = re.match(my_regex, zx)

                        if temp_search:
                            existiplst.append(ip.strip())
                            existlst.append(json.loads(temp_search.string.replace("\'","\"").strip()))
                            
                except Exception as e:
                    print("Hit_cache:",e)

    if existiplst:

        diff_list = Diff(currentiplst,existiplst)

        temporary_list = []

        if diff_list:

            check_avail = workers_head(request, [diff_list], cha)

            if len(check_avail) != 0:
                for iii in check_avail:
                    temporary_list.append(iii)

        for ipps in existiplst:

            my_regex = r"{0}".format(ipps.strip())

            for lstst in existlst:

                for keeys, vaalues in lstst.items():
                    
                    if keeys == "permalink":

                        temporary_search = re.match(my_regex, vaalues)

                        if temporary_search:

                            temporary_list.append(resultss([lstst], my_regex))
        return temporary_list

    temporary_listss = []
    check_avail = workers_head(request, [currentiplst], cha)

    if len(check_avail) != 0:
        for iii in check_avail:
            temporary_listss.append(iii)
        return temporary_listss

def request(iqs,cches):

    try:
        resp_code = {}
    
        existlsta = []

        result = requests.get("https://www.threatcrowd.org/searchApi/v2/ip/report/?", params = {"ip": iqs}, timeout=5)

        if result.json() != {}:

            resp_code = json.loads(result.content)

            for k, v in resp_code.items():

                if k == "response_code":

                    if v == str(1):
                        
                        existlsta.append(json.loads(result.content))

                        cches.write("%s\n" %(json.loads(result.content)))

                        try:

                            return resultss(existlsta,iqs)

                        except Exception as e:
                            print(iqs)
                            print("request:", e)
                    else:

                        print("\nMiss:",iqs, "status code: ",v)
                        return False

    except Exception as e:
        print(e)

def resultss(r_answer,ips):

    csv = {}
    idlst = None
    lstresolv = None
    lstresolv2 = None
    lstresolv3 = None
    dom = None
    dom2 = None
    dom3 = None
    avhashes = None
    avhashes2 = None
    avhashes3 = None
    permalink =None

    if isinstance(r_answer, list):
        ipliist = ips
        for x in r_answer:
            csv["IP"] = ipliist
            for k,v in x.items():
                if k == "resolutions":
                    temp_list = []
                    for l in v:
                        temp = l.values()
                        for o in temp:
                            temp_list.append(o)
                    if len(v) >= 3:
                        dom = temp_list[-1]
                        csv["Domain"] = dom
                        lstresolv= temp_list[-2]
                        csv["Last resolved"] = lstresolv
                        dom2 = temp_list[-3]
                        csv["Domain 2"] = dom2
                        lstresolv2 = temp_list[-4]
                        csv["Last resolved 2"] = lstresolv2
                        dom3 = temp_list[-5]
                        csv["Domain 3"] = dom3
                        lstresolv3 = temp_list[-6]
                        csv["Last resolved 3"] = lstresolv3
                    else:   
                        if len(v) == 2:
                            dom = temp_list[-1]
                            csv["Domain"] = dom
                            lstresolv = temp_list[-2]
                            csv["Last resolved"] = lstresolv
                            dom2 = temp_list[-3]
                            csv["Domain 2"] = dom2
                            lstresolv2 = temp_list[-4]
                            csv["Last resolved 2"] = lstresolv2
                            dom3 = "none"
                            csv["Domain 3"] = dom3
                            lstresolv3 = "none"
                            csv["Last resolved 3"] = lstresolv3
                        else:    
                            if len(v) == 1:
                                dom = temp_list[-1]
                                csv["Domain"] = dom                                 
                                lstresolv = temp_list[-2]
                                csv["Last resolved"] = lstresolv
                                dom2 = "none"
                                csv["Domain 2"] = dom2
                                lstresolv2 = "none"
                                csv["Last resolved 2"] = lstresolv2
                                dom3 = "none"
                                csv["Domain 3"] = dom3   
                                lstresolv3 = "none"
                                csv["Last resolved 3"] = lstresolv3
                            else:
                                dom = "none"
                                csv["Domain"] = dom                                
                                lstresolv = "none"
                                csv["Last resolved"] = lstresolv
                                dom2 = "none"
                                csv["Domain 2"] = dom2
                                lstresolv2 = "none"
                                csv["Last resolved 2"] = lstresolv2
                                dom3 = "none"
                                csv["Domain 3"] = dom3   
                                lstresolv3 = "none"
                                csv["Last resolved 3"] = lstresolv3
                elif k == "hashes":
                    temp_list = []
                    if len(v) != 0: 
                        for l in v:
                            temp_list.append(l)
                        if len(v) >= 3:
                            avhashes = temp_list[0]
                            csv["Hashe"] = avhashes
                            avhashes2 = temp_list[1]
                            csv["Hashe 2"] = avhashes2
                            avhashes3 = temp_list[2]
                            csv["Hashe 3"] = avhashes3
                        else:
                            if len(v) == 2:
                                avhashes = temp_list[0]
                                csv["Hashe"] = avhashes
                                avhashes2 = temp_list[1]
                                csv["Hashe 2"] = avhashes2
                                avhashes3 = "none"
                                csv["Hashe 3"] = avhashes3
                            else:
                                avhashes = temp_list[0]
                                csv["Hashe"] = avhashes
                                avhashes2 = "none"
                                csv["Hashe 2"] = avhashes2
                                avhashes3 = "none"
                                csv["Hashe 3"] = avhashes3
                    else:
                        avhashes = "none"
                        csv["Hashe"] = avhashes
                        avhashes2 = "none"
                        csv["Hashe 2"] = avhashes2
                        avhashes3 = "none"
                        csv["Hashe 3"] = avhashes3
                elif k == "permalink":
                    permalink = v
                    csv["Permalink"] = permalink
    return csv

def main(IPlst):
    ch = Cache()
    return open_iplist(json.loads(IPlst), ch)
