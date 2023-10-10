from flask import Flask,render_template, send_file
from Ranking import stock_rank
from Pull_render import get_pull, get_last5, tractor_name, teams
app=Flask(__name__)
app.static_folder='images'

pulldata={"id":0,"distance":0,"speed":0,"load":0}
last5={}
@app.route('/hello')
def hello():

    return 'World!'

@app.route('/')
def home_page():
    data=teams()
    return render_template('home_page.html',data=data)

@app.route('/html')
def html():
    return render_template('temp.html')

@app.route('/tractor/<int:tractor_id>')
def tractor_page(tractor_id):
    return str(tractor_name(tractor_id))

page_data = [
    {"title": "Page 1", "content": "Content for Page 1"},
    {"title": "Page 2", "content": "Content for Page 2"},
    {"title": "Page 3", "content": "Content for Page 3"},
]

@app.route('/tractor/<tractor>')
def tractor(tractor):
    # Your code to handle the tractor page
    return f"This is the {tractor} page for."

@app.route('/page/<int:page_id>')
def display_page(page_id):
    # Check if the requested page_id is within the range of available pages
    dat=get_pull(page_id)
    if dat==0:
        return "404"
    page = dat
    image_name=f"my_plot{page_id}.png"
    return render_template('page.html', page=dat)
    

@app.route('/stock')
def display_stock_class():
    return render_template('stock.html')

@app.route('/render')
def render():
    stock_rank()
    return "Done"

@app.route('/datain/<int:id>/<float:dist>/<float:speed>/<float:load>')
def datain(id,dist,speed,load):
    print(id,dist,speed,load)
    pulldata["id"]=id
    pulldata["distance"]=dist
    pulldata["speed"]=speed
    pulldata["load"]=load
    return "Done"

@app.route('/dataout')
def dataout():
    return pulldata

@app.route('/last5')
def last5():
    get=get_last5()
    return get


@app.route('/Overlay_Ranking')
def serve_image():
    # Replace 'path_to_your_image.png' with the actual path to your image file
    image_path = 'images/Leader_Board_Overlay.png'
    
    # You can specify additional headers if needed
    headers = {'Cache-Control': 'no-cache'}
    
    # Send the image file as a response
    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True,host="192.168.1.139")

