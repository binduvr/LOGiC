import flask

import logic.settings as settings
import logic.report_generator.mailer as mailer


report_generator = flask.Blueprint('report_generator', __name__)

@report_generator.route('/generate/<session_id>', methods=['GET'])
def generate_report(session_id):
    try:
        reportdict = importer(session_id)
        generator(session_id,reportdict) #mod from C4 reportgenerator repgen @@Bindu; moeten dit soort functies altijd een 0 returnen?
        compiler(session_id,reportdict)
        #TODO post pdf
    except:
        flask.abort(404)

# @report_generator.route('/email', methods=['POST'])
@report_generator.route('/email')
def email_report():
    """Email a report of the simulation of the session_id."""

    # request_json = request.get_json(force=True)

    # session_id = request_json['session_id']
    # email = request_json['email']

    # Test
    session_id = "20191028143512"
    email = "b.j.vanraak@gmail.com"
    # mailer.email_report(session_id, email)

# STOPPED WORKING FOR SOME REASON

    try:
        mailer.email_report(session_id, email)
        return "Success"
    except:
        flask.abort(404)

# FIXME: Fix this problem
@report_generator.route('/download', methods=['POST'])
def download_report(session_id):
    """Download a report of the simulation of the session_id."""

    request_json = request.get_json(force=True)
    session_id = request_json['session_id']

    file_path = settings.OUTPUT_DIRECTORY + session_id

    try:
        return flask.send_from_directory(file_path, filename='report.pdf',
            as_attachment=True)
    except FileNotFoundError:
        flask.abort(404)
