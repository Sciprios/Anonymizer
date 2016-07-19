from subprocess import call

if __name__== '__main__':
    call(["sudo", "python", "static/get-pip.py"])

    requirements = []
    with open("static/requirements.txt") as req_file:
        requirements = req_file.readlines()

    for requirement in requirements:
        call(["sudo", "pip", "install", requirement])
