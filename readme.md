# INFRASTRUCTURE CC
Simple multi-datacenter infrastructure overview and monitoring dashboard.

![Home](https://github.com/andreacarriero/infrastructure-cc/raw/master/screenshots/home.png)

---

![Datacenters](https://github.com/andreacarriero/infrastructure-cc/raw/master/screenshots/datacenters.png)

---

![Datacenter](https://github.com/andreacarriero/infrastructure-cc/raw/master/screenshots/datacenter.png)

---

![Nodes](https://github.com/andreacarriero/infrastructure-cc/raw/master/screenshots/nodes.png)

---

![Node](https://github.com/andreacarriero/infrastructure-cc/raw/master/screenshots/node.png)

---

![Projects](https://github.com/andreacarriero/infrastructure-cc/raw/master/screenshots/projects.png)

---

![Project](https://github.com/andreacarriero/infrastructure-cc/raw/master/screenshots/project.png)

---

![Project Command Job](https://github.com/andreacarriero/infrastructure-cc/raw/master/screenshots/project_command_job.png)


### cc_server
Application server written in Python. Handles API calls.

0. `mv data/configuration.json.example data/configuration.json`
1. `virtualenv venv -p python3`
2. `source venv/bin/activate`
3. `pip3 install -r requirements`
4. `python3 manage.py runserver`

### cc_admin_ui
SPA made with Vue.js and Buefy.

0. `npm install`
1. `node_modules/.bin/poi`
