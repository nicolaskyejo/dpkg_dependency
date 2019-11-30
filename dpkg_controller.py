from flask import Flask, render_template, make_response
from dpkg_status_parser import dpkg_parser


package_structure = dpkg_parser()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def landing_page():
    """View for package names found"""
    package_names = package_structure.keys()
    return render_template('index.html', package_names=package_names)


@app.route('/package/<package_name>', methods=['GET'])
def package_routes(package_name):
    """View for specific package info"""
    package_info = package_structure.get(package_name)
    if package_info is not None:
        return render_template('package_info.html', package_name=package_name, package_info=package_info)
    return make_response('Could not find package information...', 404)


if __name__ == '__main__':
    app.run(debug=True)
