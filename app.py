import docker
from flask import Flask, abort, render_template, redirect, current_app, request, url_for
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")

def index():
    remote_ip = request.remote_addr
    if remote_ip not in current_app.config["ALLOWED_IPS"]:
       abort(403, "Access Denied")
    client = docker.from_env()
    container_list = query_container(client)
    return render_template('index.html', container_list=container_list)

def query_container(client):
   containers = client.containers.list(all=True), filters={"name":"valheim"})
   return containers

@app.route("/manage", methods=['POST'])

def manage():
   remote_ip = request.remote_addr
   app.logger.warning(current_app.config["ALLOWED_IPS"])
   if remote_ip not in current_app.config["ALLOWED_IPS"]:
      abort(403, "Access Denied")
   app.logger.warning("Hitting manage endpoint from IP: " + remote_ip)
   client=docker.from_env()
   checked=request.form.getlist("container_select")
   #return request.form
   if 'start' in request.form:
      app.logger.warning("Start button clicked.")
      for item in checked:
         app.logger.warning("Item: " + item)
         item_name = item.strip()
         try:
            container = client.containers.get(item_name)
            app.logger.warning(container.name)
            container.start()

            container.start()
         except Exception as e:
            app.logger.warning("Error starting container " + item_name)
            app.logger.warning("Exception: {0}".format(e))
   elif 'shutdown' in request.form:
      app.logger.warning("Shutdown button clicked.")
      for item in checked:
         app.logger.warning("Item to shutdown: " + item)
         item_name = item.strip()
         try:
            container = client.containers.get(item_name)
            container.stop()
         except Exception as e:
            app.logger.warning("Error stopping container " + item_name)
            app.logger.warning("Exception: {0}".format(e))
   elif 'restart' in request.form:
      app.logger.warning("Restart button clicked.")
      for item in checked:
         app.logger.warning("Item to restart: " + item)
         item_name = item.strip()
         try:
            container = client.containers.get(item_name)
            container.restart()
         except Exception as e:
            app.logger.warning("Error restarting container " + item_name)
            app.logger.warning("Exception: {0}".format(e))
   app.logger.warning("Redirecting...")
   return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
