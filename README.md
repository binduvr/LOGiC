# LOGiC Off Grid Location Analyser
This application was designed to take simple inputs and provide users with information when considering off-grid energy systems

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
* A python virtual environment manager, such as [Anaconda](https://www.anaconda.com/distribution/).

* [CBC-Solver](https://ampl.com/dl/open/cbc/) must be installed and added to the PATH environment variable in order for the application to make calculations. [How to set environment variables](http://www.computerhope.com/issues/ch000549.htm).

* A LaTeX compiler such as [MiKTeX](https://miktex.org/download) must be installed to allow for report functionality and must also be added to the PATH environment variable, the same way the CBC-Solver is added.

### Installing
1. Create a new python environment using Python version 3.6. We will use Anaconda as an example.
```
conda create -n yourenvname python=3.6
source activate yourenvname
```

2. Move to the directory you would like to install to.
```
cd path/to/install/directory
```

3. Clone the master branch of the repository.
```
git clone https://github.com/binduvr/LOGiC.git
```

4. Move into the cloned directory
```
cd LOGiC
```

5. Install the requirements for the application
```
pip install -r requirements.txt
```

### Running the application
To run the application:
1. Run run.py to start the web server
```
python run.py
```

2. The server is now running. Please check the wiki for a list of routes and their functions.


## Authors

* **Martha Hoffmann** - *Developer of Offgridders* ([Offgridders](https://github.com/smartie2076/offgridders)) - Reiner Lemoine Institute, Berlin
* **Marien Boonman** - Off Grid Test Center, Spanbroek
* **Bindu van Raak** - Off Grid Test Center, Spanbroek

## Acknowledgments

A special thanks to Martha Hoffmann from the Reiner Lemoine Institute in Berlin for the development of Offgridders, the main core of this application.

