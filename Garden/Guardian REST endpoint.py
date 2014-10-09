"""
we need to install weget in windows, and linux platform no need install wget

"""


import os
import json
import urllib
import subprocess
from BeautifulSoup import BeautifulSoup

class BaseClass(object):
    """
	This class that contains generic code for connecting to an API like Guardian.
	"""
    def __init__(self, api_url):
	"""
	this constracter  open api url
	"""
        self.url = api_url
        self.base_json = self.open_url(api_url)
   
    def open_url(self, url):
        """
	This method return open url and read the content 
	"""
        return urllib.urlopen(url).read()
         
    def get_response(self):
	"""
	This method returns the json response
	"""
        response = json.loads(self.base_json)["response"]
        return response

    def parse_html(self, page):
	"""
	this method return the parse html
	
	"""
        html_content = self.open_url(page)
        parsed_html = BeautifulSoup(html_content)
        
        return parsed_html
    
    def save(self, files, local_path_dir):
	"""
	This method return images files store in Local System
	"""
        if not os.path.exists(local_path_dir):
            os.makedirs(local_path_dir)

        old_cwd = os.getcwd()
        os.chdir(local_path_dir)
        for static_file_url in files:
            p = subprocess.Popen(["wget", "-c", static_file_url], stdout=subprocess.PIPE)
            output = p.stdout.readlines() 

        os.chdir(old_cwd)

class GuardianAPI(BaseClass):
    """
    This class for Guardian API. 
    """

    def __init__(self, url):
        """ 
		Call the Guardian REST endpoint and retrieve the data 
		"""
        super(GuardianAPI, self).__init__(url)
        self.response = self.get_response()
        self.results = self.response["results"]
    
    def get_images(self):
        """
        
		Iterate the objects 
       
		For each object call the contained url; 
	    a. Parse the contents of the returned object and attempt to extract the image hrefs 
        """
        images = []
        for result in self.results:
            try:
                web_url = result["webUrl"]
                parsed_html = self.parse_html(web_url)
                content_div = parsed_html.body.find('div', {'id':'content'})
                images.append(content_div.find('img').get('src'))
            except:
                pass
            
        return images

if __name__ == "__main__":
    url = "http://content.guardianapis.com/search?api-key=test&q=obama"
    images_dir = 'images'

    g = GuardianAPI(url)
    images = g.get_images()
    #Request the images directly and save to a folder.
    #images are nothing but static files 
    g.save(images, images_dir)
