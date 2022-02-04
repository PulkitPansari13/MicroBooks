from flask import Flask, Response, request, jsonify
import requests


app = Flask(__name__)

valid_services = {
    'users': 'http://users:8000/users/',
    'content': 'http://content:8000/books/',
    'interaction': 'http://interaction:8000/interaction/',
    'fakeusers': 'http://users:8000/ingestfake/',
    'ingestcontent': 'http://content:8000/ingestfake/',
    'fakeinteraction': 'http://interaction:8000/ingestfake/',
}

ALLOWED_EXTENSIONS = set(['csv'])

@app.route('/api/users', methods=['POST', 'GET'])
def user_list():
    req_url = valid_services['users']
    r = requests.request(method=request.method,url=req_url, data=request.data, headers=request.headers)
    return Response(
        r.content,
        status=r.status_code,
        content_type=r.headers.get('content-type'),
    )

@app.route('/api/users/<userid>', methods=['PUT', 'GET', 'DELETE'])
def user_detail(userid):
    req_url = valid_services['users'] + userid
    r = requests.request(method=request.method,url=req_url, data=request.data, headers=request.headers)
    return Response(
        r.content,
        status=r.status_code,
        content_type=r.headers.get('content-type'),
    )


@app.route('/api/books/<list_type>', methods=['GET'])
def content_list(list_type):
    req_url = valid_services['content'] + list_type
    r = requests.request(method=request.method,url=req_url, data=request.data, headers=request.headers)
    return Response(
        r.content,
        status=r.status_code,
        content_type=r.headers.get('content-type'),
    )

@app.route('/api/books', methods=['POST'])
def content_create():
    req_url = valid_services['content']
    r = requests.request(method=request.method,url=req_url, data=request.data, headers=request.headers)
    return Response(
        r.content,
        status=r.status_code,
        content_type=r.headers.get('content-type'),
    )


@app.route('/api/books/<bookid>', methods=['PUT', 'GET', 'DELETE'])
def content_detail(bookid):
    req_url = valid_services['content'] + bookid
    r = requests.request(method=request.method,url=req_url, data=request.data, headers=request.headers)
    return Response(
        r.content,
        status=r.status_code,
        content_type=r.headers.get('content-type'),
    )


@app.route('/api/interaction/book/<bookid>/like', methods=['POST'])
def content_like_toggle(bookid):
    req_url = valid_services['interaction'] + f'book/{bookid}/like'
    r = requests.request(method=request.method,url=req_url, data=request.data, headers=request.headers)
    return Response(
        r.content,
        status=r.status_code,
        content_type=r.headers.get('content-type'),
    )

@app.route('/api/interaction/book/<bookid>/read', methods=['POST'])
def content_read(bookid):
    req_url = valid_services['interaction'] + f'book/{bookid}/read'
    r = requests.request(method=request.method,url=req_url, data=request.data, headers=request.headers)
    return Response(
        r.content,
        status=r.status_code,
        content_type=r.headers.get('content-type'),
    )




def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/ingest-data', methods=['POST'])
def upload_file():
	# check if the post request has the file part
    if 'csv_file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['csv_file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        ingestuserurl = valid_services['fakeusers']
        ingestcontenturl = valid_services['ingestcontent']
        ingestinteractionurl = valid_services['fakeinteraction']
        
        user_request = requests.post(ingestuserurl)
        if user_request.status_code != 201:
            resp = jsonify({'message' : 'could not sent file'})
            resp.status_code = 400
            return resp
        file_to_upload = {'csv_file': ('data.csv', file, 'text/csv')}
        r = requests.post(ingestcontenturl, files=file_to_upload)
        # r = requests.post(ingestcontenturl)
        if r.status_code == 201:

            interaction_request = requests.post(ingestinteractionurl)
            if interaction_request.status_code != 201:
                resp = jsonify({'message' : 'Content ingested but failed to create interaction.'})
                resp.status_code = 201
                return resp

            resp = jsonify({'message' : 'Content ingested successfully!'})
            resp.status_code = 201
            return resp

        elif r.status_code == 400:
            return Response(
                r.content,
                status=r.status_code,
                content_type=r.headers.get('content-type'),
            )
        else:
            resp = jsonify({'message' : 'CSV file not in required format or is empty'})
            resp.status_code = 400
            return resp
    else:
        resp = jsonify({'message' : 'Only csv files are allowed'})
        resp.status_code = 400
        return resp


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(error=str(e)), 405




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)