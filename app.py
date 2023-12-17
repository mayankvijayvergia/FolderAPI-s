from urllib import response
from flask import Flask, flash, make_response, request, json, render_template, send_from_directory, abort, url_for,redirect
import os
app = Flask(__name__)
app.secret_key = 'zxcv'
app.config['FOLDER'] = r"C:\Users\mayank1.vijay\Desktop\FolderAPI"

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/createfolder', methods=["POST", "GET"])
def createfolder():
    file = request.form.get("filename")
    if request.method == "POST":
        if "." in file:
            return "Please enter Folder name correctly"
        else:
            file = file.strip().capitalize()
            user_folder = os.path.join(app.config['FOLDER'], file)
            if os.path.isdir(user_folder):
                return "Folder Already Exist"
            else:
                os.mkdir(user_folder)
        return f"folder is created under the name {file} and the full path is {user_folder}"
    return render_template("createfolder.html")


@app.route('/list')
def listOfFolders():
    l = os.listdir(app.config['FOLDER'])
    print(l)
    #return json.dumps(l)
    return render_template("listoffolder.html",l=l)


@app.route("/upload")
def dropdown():
    folderlist = next(os.walk(app.config['FOLDER']))[1]
    print(folderlist)
    return render_template("folderdropdown.html", folderlist=folderlist)

@app.route("/uploaded", methods = ["POST","GET"])
def upload():
    folder = request.form.get("Folder")
    path2 = os.path.join(app.config['FOLDER'],folder)
    print(folder)
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        if filename == ""   :
            # res ={"message": "No file Selected"}
            # statuscode = 400
            # return make_response(res,statuscode)
            flash("File type not supported")
            return redirect(url_for('dropdown'))
        if "." in filename:
            f = filename.split(".")
            if f[1] in ('txt','png','jpg','csv','doc','pdf','docx','xlx','xlsx'):
                destination = os.path.join(path2,filename)
                print(destination)
                file.save(destination)
                return render_template("complete.html")
            else:
                # res = {"message": "file type not supported"}
                # statuscode = 400
                # return make_response(res,statuscode)
                flash("File type not supported")
                return redirect(url_for('dropdown'))
                #return redirect(request.url)
        else:
            # res = {"message": "file type not supported"}
            # statuscode = 400
            # return make_response(res,statuscode)
                flash("File type not supported")
                return redirect(url_for('dropdown'))
                #return redirect(request.url)       

@app.route("/download")
def dropdownfolder():
    folderlist = next(os.walk(app.config['FOLDER']))[1]
    print(folderlist)
    return render_template("listfolder.html", folderlist=folderlist)

# @app.route("/download")
# def dropdownfolder():
#     folderlist = os.listdir(app.config['FOLDER'])
#     for item in folderlist:
#         if item.endswith(".py"):
#             folderlist.remove(item)
#     print(folderlist)
#     return render_template("listfolder.html", folderlist=folderlist)


# @app.route("/download")
# def dropdownfolder():
#     folderlist = os.listdir(app.config['FOLDER'])
#     for item in folderlist:
#         if "." in item:
#             folderlist.remove(item)
#     print(folderlist)
#     return render_template("listfolder.html", folderlist=folderlist)

@app.route("/listfile",methods=["GET", "POST"])
def dropdownfile():
    folder = request.form.get("Folder")
    print(folder)
    path1 = os.path.join(app.config['FOLDER'],folder)
    filelist = next(os.walk(path1))[2]
    # for item in filelist:
    #     if "." not in item:
    #         filelist.remove(item)
    print(filelist)
    list1 = [folder,filelist]
    return render_template("listfile.html", list1 = list1 )

@app.route('/downloadfile', methods=["GET", "POST"])
def get():
    name = request.form.get("File")
    print(name)
    foldername = request.form.get("folder")
    print(foldername)
    finalpath = os.path.join(app.config['FOLDER'],foldername)
    print(finalpath)
    print(name)
    try:
        return send_from_directory(finalpath, name, as_attachment=True)
    except FileNotFoundError:
            (404)


@app.route("/delete")
def deletedropdownfolder():
    folderlist = next(os.walk(app.config['FOLDER']))[1]
    print(folderlist)
    return render_template("deletelistfolder.html", folderlist=folderlist)

@app.route("/deletelistfile",methods=["GET", "POST"])
def deletedropdownfile():
    folder = request.form.get("Folder")
    print(folder)
    path1 = os.path.join(app.config['FOLDER'],folder)
    filelist = next(os.walk(path1))[2]
    print(filelist)
    list1 = [folder,filelist]
    return render_template("deletelistfile.html", list1 = list1 )

@app.route('/deletefile', methods=["GET", "POST"])
def deleteget():
    name = request.form.get("File")
    print(name)
    foldername = request.form.get("folder")
    print(foldername)
    finalpath = os.path.join(app.config['FOLDER'],foldername,name)
    os.remove(finalpath)
    return render_template("deletecomplete.html")

if __name__ == "__main__":
    app.run()