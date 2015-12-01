from flask import Flask
from flask import request
from flask import render_template
import urlparse
import re

app = Flask ( __name__ )

def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse.urlparse ( value )
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urlparse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

@app.route( '/' )
def index ():
	return render_template ( "header.html" ) + render_template ( "footer.html" )

@app.route( '/', methods=['POST'] )
def get_mp3():
	text = request.form['text']
	youtube_id = video_id ( text )
	return youtube_id

if __name__ == '__main__':
	app.debug = True
	app.run ();
