import flask

import logic.settings as settings
import logic.report_generator.mailer as mailer

report_generator = flask.Blueprint('report_generator', __name__)

# @report_generator.route('/email', methods=['POST'])
@report_generator.route('/email')
def email_report():
    """Email a report of the simulation of the session_id."""

    # Testing
    request_json = flask.request.args.to_dict()

    # request_json = flask.request.get_json(force=True)
    session_id = request_json['session_id']
    email = request_json['email']

    try:
        mailer.email_report(session_id, email)
        return "Success"
    except:
        flask.abort(404)

# @report_generator.route('/download', methods=['POST'])
@report_generator.route('/download')
def download_report():
    """Download a report of the simulation of the session_id."""

    # Test
    request_json = flask.request.args.to_dict()

    # request_json = request.get_json(force=True)
    session_id = request_json['session_id']
    file_path = settings.BASE_DIR + '/' + \
        settings.OUTPUT_DIRECTORY + session_id + "/report"
    try:
        return flask.send_from_directory(file_path,
            filename=settings.REPORT_NAME + ".pdf", as_attachment=True)
    except FileNotFoundError:
        flask.abort(404)
