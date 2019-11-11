import flask
import os.path

import logic.settings as settings
import logic.report_generator.mailer as mailer
import logic.report_generator.importer as importer
import logic.report_generator.generator as generator
import logic.report_generator.compiler as compiler

report_generator = flask.Blueprint('report_generator', __name__)

@report_generator.route('/email', methods=['POST'])
# @report_generator.route('/email')
def email_report():
    """Email a report of the simulation of the session_id."""

    # Testing
    # request_json = flask.request.args.to_dict()

    request_json = flask.request.get_json(force=True)
    session_id = str(request_json['session_id'])
    email = request_json['email']

    # Check if document has already been generated
    file_path = settings.OUTPUT_DIRECTORY + session_id \
        + "/report/" + settings.REPORT_NAME + ".pdf"

    if not os.path.exists(file_path):
        reportdict = importer.import_data(session_id)
        generator.generate_report(session_id, reportdict)
        compiler.compile(session_id, reportdict)

    # Mail report
    try:
        mailer.email_report(session_id, email)
        return "Success"
    except:
        flask.abort(404)

@report_generator.route('/download/<session_id>', methods=['GET'])
def download_report(session_id):
    """Download a report of the simulation of the session_id."""

    file_path = settings.BASE_DIR + '/' + \
        settings.OUTPUT_DIRECTORY + str(session_id) + "/report"
    try:
        return flask.send_from_directory(file_path,
            filename=settings.REPORT_NAME + ".pdf", as_attachment=True)
    except FileNotFoundError:
        flask.abort(404)
