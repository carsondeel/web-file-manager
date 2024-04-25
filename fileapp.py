# Packages
from flask import Flask
from flask import render_template_string
from flask import redirect
from flask import request
import os
import subprocess
import shutil

# App
app = Flask(__name__)


@app.route('/')
def root():
    return render_template_string('''
        <html>
          <head>
            <title>File manager</title>
          </head>
          <body>
            <div align="center">
              <h1>Local file system</h1>
              <p><strong>CWD: </strong>{{ current_working_directory }}</p>
            </div>
            
            
            <ul>
              <form action="/md">
                <input type="submit" value="New folder"/>
                <input name="folder" type="text" value="new_folder"/>
              </form>
              <li><a href="/cd?path=..">..</a></li>
              {% for item in file_list[0: -1] %}
                {% if '.' not in item%}
                  <li><strong><a href="/cd?path={{current_working_directory + '/' + item}}">{{item}}</a></strong><a href="/rm?dir={{item}}"> X</a></li>
                {% elif '.txt' in item or '.py' in item or '.json' in item %}
                  <li><strong><a href="/view?file={{current_working_directory + '/' + item}}">{{item}}</a></strong></li>
                {% else %}
                  <li>{{item}}</li>
                {% endif%}
              {% endfor %}
            </ul>
          </body>
        </html>
    ''', # Use 'dir' command on Windows
    current_working_directory=os.getcwd(),
         file_list=subprocess.check_output('ls', shell=True).decode('utf-8').split('\n'))

# Handle 'cd' command
@app.route('/cd')
def cd():
    # Run 'level up' command
    os.chdir(request.args.get('path'))
    
    # Redirect to file manager
    return redirect('/')

# Handle 'make directory' command
@app.route('/md')
def md():
    # Create new folder
    os.mkdir(request.args.get('folder'))
    
    # Redirect to file manager
    return redirect('/')

@app.route('/rm')
def rm():
    # 'rm' command
    shutil.rmtree(os.getcwd() + '/' + request.args.get('dir'))
    
    # Redirect to file manager
    return redirect('/')
    
# View files (text)
@app.route('/view')
def view():
    # get the file content
    with open(request.args.get('file')) as f:
        return f.read().replace('\n', '<br>')

# Run the HTTP server
if __name__ == '__main__':
    app.run(debug=True, threaded=True)