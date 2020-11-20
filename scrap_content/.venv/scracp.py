import requests, json, re, flask
from bs4 import BeautifulSoup
from flask import request, jsonify
from urllib.parse import urlparse

def data_collection(data):

    json_body_temp = []
    json_body = []

    for art in data:

        json_line = {}
        json_underline = {}

        # regex para filtrar o conteudo
        regex_id = re.search(r'(?<=(id\=\"))[^\"]*.*?', str(art))
        title = re.search(r'(?<=(title\=\"))[^\"]*.*?', str(art))
        url_art = art.find("a", attrs={"title" : re.compile('')})
        url = re.search(r'(?<=(href\=\"))[^\"]*.*?', str(url_art))
        date = art.find("time")
        img_art = art.find("img", attrs={"src" : re.compile('')})
        src_img = re.search(r'(https\:)+.+(720x)+.+(jpg)(?=(\")|$)', str(img_art))
        src_img2 = re.search(r'((?<=( ))https\:)+.+(720x)+.+(jpeg)(?=( 720w)|$)', str(img_art))
        #criar novo regex para certas imagens
        
        desc_art = art('div')
        descrip = re.search(r'(?<=(\<p\>))[^(\<)]+.+(?=(\<)|$)', str(desc_art))

        desc_2art = ('div')
        descrip2 = re.search(r'(?<=(erpt\"\>))[^(\<)]+.+(?=(\<)|$)', str(desc_2art))
        descrip3 = re.search(r'(?<=(ank\"\>))[^(\<)]+.+(?=(\<)|$)', str(desc_2art))

        if src_img or src_img2:
            # Append id as a key
            json_line["id_art"] = regex_id.group(0)
            json_body_temp.append(json_line)

            # Dic for content
            json_underline["title_art"] = title.group(0)

            if descrip:
                json_underline["description"] = descrip.group(0)
            if descrip2:
                json_underline["description"] = descrip2.group(0)
            if descrip3:
                json_underline["description"] = descrip3.group(0)
            json_underline["date"] = date.text
            json_underline["url_art"] = url.group(0)

            if src_img:
                json_underline["img_art"] = src_img.group(0)
            if src_img2:
                json_underline["img_art"] = src_img2.group(0)

            # Append Dic above under "content"
            json_line["content"] = json_underline
            json_body_temp.append(json_line)

    #Remove duplicates s   
    for i in range(len(json_body_temp)): 
        if json_body_temp[i] not in json_body_temp[i + 1:]: 
            json_body.append(json_body_temp[i]) 

    return json_body


if __name__ == "__main__":

    app = flask.Flask(__name__)
    #app.config["DEBUG"] = True
    id_page = int()
    url = urlparse("https://pplware.sapo.pt")

    @app.route('/api/v1/resource/main', methods=['GET'])
    def api_main():
        r = requests.get(url.geturl())
        parse = BeautifulSoup(r.content, 'html.parser')
        data = parse('article')

        jbody = data_collection(data)
        jdumps = json.dumps(jbody, ensure_ascii=False, indent=4, separators=(',', ': ')).encode('utf8')
        return jdumps

    @app.route('/api/v1/resource/<int:idPage>', methods=['GET'])
    def api_page(idPage):
        id_page = str(idPage)
        url_completed = "https://pplware.sapo.pt/page/" + id_page + "/"
        next_page_url = urlparse(url_completed)
        r = requests.get(next_page_url.geturl())
        parse = BeautifulSoup(r.content, 'html.parser')
        data = parse('article')

        jbody = data_collection(data)
        jdumps = json.dumps(jbody, ensure_ascii=False, indent=4, separators=(',', ': ')).encode('utf8')
        return jdumps

    app.run()

        