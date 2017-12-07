from database import dump_db
from flask import abort, flash, Flask, jsonify, make_response, redirect, render_template, request, Response, stream_with_context, url_for
import secrets
from subprocess import PIPE, Popen, STDOUT
import time
from wtforms import Form, IntegerField, SelectField, StringField, validators

app = Flask(__name__)

class AddForm(Form):
    size = SelectField('Size', validators=[validators.Required()], choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')])
    env = SelectField('Environment', validators=[validators.Required()], choices=[('test', 'Test'), ('production', 'Production')])
    name = StringField('Network Name', validators=[validators.Required(), validators.Length(min=0, max=50)]) # Add character validator (no whitespace)
    owner = StringField('Network POC Email', validators=[validators.Required(), validators.Length(min=0, max=50)]) # Add character validator (no whitespace)

class DeleteForm(Form):
    index = IntegerField('ID', validators=[validators.Required()])

def fulfill(action, size, env, name, owner, index):
    with open('./log/fulfill.log', 'w') as logfile:
        Popen(['python fulfill.py {} {} {} {} {} {}'.format(action, size, name, env, owner, index)], shell=True, universal_newlines=True, stdout=logfile)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddForm(request.form)
    flash('Requests will take approximately 45 seconds to fulfill after submission', 'info')
    if request.method == 'POST' and form.validate():
        action = 'add'
        size = form.size.data
        env = form.env.data
        name = form.name.data
        owner = form.owner.data
        index = 'null'
        fulfill(action, size, env, name, owner, index)
        flash('Request to {} a {} network named {} in the {} environment for {} submitted'.format(action, size, name, env, owner), 'success')
        return redirect(url_for('status'))
    return render_template('home.html', form=form)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    form = DeleteForm(request.form)
    flash('Requests will take approximately 45 seconds to fulfill after submission', 'info')
    if request.method == 'POST' and form.validate():
        action = 'delete'
        size = 'null'
        env = 'null'
        name = 'null'
        owner = 'null'
        index = form.index.data
        fulfill(action, size, env, name, owner, index)
        return redirect(url_for('status'))
        flash('Request to {} record ID {} submitted'.format(action, index), 'success')
    return render_template('delete.html', form=form)

@app.route('/status')
def status():
    flash('Redirected for status...', 'info')
    time.sleep(45)
    with open('./log/fulfill.log', 'r') as logfile:
        status = (logfile.read()).split('\n')
    return render_template('status.html', status=status)

@app.route('/netmenu')
def netmenu():
    networks = dump_db()
    return render_template('netmenu.html', menu=networks)

@app.route('/howto')
def howto():
    return render_template('howto.html')

@app.route('/api/v1.0/netmenu', methods=['GET'])
def get_netmenu():
    networks = dump_db()
    return jsonify({'networks': networks})

@app.route('/api/v1.0/netmenu/<int:net_index>', methods=['GET'])
def get_net(net_index):
    networks = dump_db()
    network = [net for net in networks if net['id'] == net_index]
    if len(network) == 0:
        abort(404)
    return jsonify({'network': network[0]})

@app.errorhandler(404)
def net_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.secret_key = secrets.secret_key
    app.run(debug=True)
