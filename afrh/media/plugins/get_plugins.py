import time
import requests
import os
import datetime
import urllib
import platform

css_plugin_urls = [
    "http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.0/css/bootstrap.min.css",
    "http://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.2.0/css/font-awesome.min.css",
    "http://cdnjs.cloudflare.com/ajax/libs/octicons/2.1.2/octicons.min.css",
    "http://cdnjs.cloudflare.com/ajax/libs/select2/3.5.0/select2-bootstrap.min.css",
    "http://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/3.1.3/css/bootstrap-datetimepicker.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/blueimp-gallery/2.15.2/css/blueimp-gallery.min.css",
    ]

js_plugin_urls = [
    "http://cdnjs.cloudflare.com/ajax/libs/knockout/3.2.0/knockout-min",
    "http://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min",
    "http://cdnjs.cloudflare.com/ajax/libs/d3/3.5.3/d3.min",
    "http://cdnjs.cloudflare.com/ajax/libs/requirejs-async/0.1.1/async",
    "http://cdnjs.cloudflare.com/ajax/libs/flexslider/2.2.2/jquery.flexslider-min",
    "http://blueimp.github.io/Gallery/js/jquery.blueimp-gallery",
    "https://raw.githubusercontent.com/wavded/js-shapefile-to-geojson/master/shapefile",
    "http://cdnjs.cloudflare.com/ajax/libs/backbone.js/1.1.2/backbone-min",
    "http://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.11.1/jquery.validate.min",
    "http://cdnjs.cloudflare.com/ajax/libs/moment.js/2.8.4/moment.min",
    "http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.7.0/underscore-min",
    "http://cdnjs.cloudflare.com/ajax/libs/jquery-easing/1.3/jquery.easing.min",
    "https://cdnjs.cloudflare.com/ajax/libs/blueimp-gallery/2.15.2/js/blueimp-gallery",
    "http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min",
    "http://cdnjs.cloudflare.com/ajax/libs/summernote/0.5.10/summernote.min",
    "http://cdnjs.cloudflare.com/ajax/libs/knockout.mapping/2.4.1/knockout.mapping.min",
    "http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.0/js/bootstrap.min",
    "http://cdnjs.cloudflare.com/ajax/libs/select2/3.5.1/select2.min",
    "https://cdnjs.cloudflare.com/ajax/libs/blueimp-gallery/2.15.2/js/blueimp-helper.min",
    "http://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/3.1.3/js/bootstrap-datetimepicker.min",
    "http://cdnjs.cloudflare.com/ajax/libs/dropzone/3.8.4/dropzone-amd-module.min"
    ]

##for url in css_plugin_urls:
##    req = requests.request('GET', url)
##    print req.status_code
##    if req.status_code == 200:
##
##        out_file = os.path.basename(url)
##        print "retrieving file {}".format(out_file)
##
##        urllib.urlretrieve(url, out_file)
##        print "  file downloaded"

ct = 0
for url in js_plugin_urls:
    url_js = url+".js"
    req = requests.request('GET', url_js)
    print req.status_code
    if req.status_code == 200:

        out_file = os.path.basename(url_js)
        print "retrieving file {}".format(out_file)

        urllib.urlretrieve(url_js, out_file)
        print "  file downloaded"
        ct +=1

print "attempted:", len(js_plugin_urls)
print "successful:", ct

