import os
import json
import subprocess
import random
import re
import sys
from flask import Flask, request, send_file, redirect

try:
    import speedtest
except ImportError:
    os.system("pip3 install speedtest-cli")

app = Flask(__name__)

@app.route("/backend")
def backend():
    return send_file("/usr/bin/backend")

@app.route("/cektrg")
def cektrg():
    x = subprocess.check_output(
        "cat /etc/trojan-go/akun.conf | grep '###' | cut -d ' ' -f2 | nl", 
        shell=True
    ).decode("ascii")
    return x

@app.route("/rentrg")
def rentrg():
    num = request.args.get("num")
    exp = request.args.get("exp")
    cmd = f'printf "%s\n" "{num}" "{exp}"| renew-trgo'
    x = subprocess.check_output(cmd, shell=True).decode("utf-8")
    return x

@app.route("/cektr")
def cektr():
    x = subprocess.check_output(
        "cat /etc/trojan/akun.conf | grep '###' | cut -d ' ' -f2 | nl", 
        shell=True
    ).decode("ascii")
    return x

@app.route("/rentr")
def rentr():
    num = request.args.get("num")
    exp = request.args.get("exp")
    cmd = f'printf "%s\n" "{num}" "{exp}"| renew-tr'
    x = subprocess.check_output(cmd, shell=True).decode("utf-8")
    return x

@app.route("/renws")
def renws():
    num = request.args.get("num")
    exp = request.args.get("exp")
    cmd = f'printf "%s\n" "{num}" "{exp}"| renew-ws'
    x = subprocess.check_output(cmd, shell=True).decode("utf-8")
    return x

@app.route("/create-trgo")
def create_trgo():
    try:
        user = request.args.get("user")
        exp = request.args.get("exp")
        x = subprocess.Popen(
            ["add-trgo"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
        )
        out, _ = x.communicate(bytes(f"{user}\n{exp}\nx\nx", "utf-8"))
        trgo = re.search("trojan-go://(.*)", out.decode("utf-8")).group(0)
        return trgo
    except Exception as e:
        return f"error: {str(e)}"

@app.route("/trial-trgo")
def trial_trgo():
    try:
        user = "trialX" + str(random.randint(10, 1000))
        exp = "1"
        x = subprocess.Popen(
            ["add-trgo"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
        )
        out, _ = x.communicate(bytes(f"{user}\n{exp}\nx\nx", "utf-8"))
        trgo = re.search("trojan-go://(.*)", out.decode("utf-8")).group(0)
        return trgo
    except Exception as e:
        return f"error: {str(e)}"

@app.route("/trojan-create")
def create_trojan():
    user = request.args.get('user')
    exp = request.args.get('exp')
    x = subprocess.Popen(
        ["add-tr"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
    )
    out, _ = x.communicate(bytes(f"{user}\n{exp}\nx\nx", "utf-8"))
    out = out.decode("utf-8")
    a = [x.group() for x in re.finditer("trojan://(.*)", out)]
    if a:
        return a[0]
    else:
        return "error"

@app.route("/trial-trojan")
def trial_trojan():
    user = "trialX" + str(random.randint(10, 1000))
    exp = "1"
    x = subprocess.Popen(
        ["add-tr"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
    )
    out, _ = x.communicate(bytes(f"{user}\n{exp}\nx\nx", "utf-8"))
    out = out.decode("utf-8")
    a = [x.group() for x in re.finditer("trojan://(.*)", out)]
    return a[0] if a else "error"

@app.route("/create-vmess")
def create_vmess():
    user = request.args.get("user")
    exp = request.args.get("exp")
    x = subprocess.Popen(
        ["add-ws"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
    )
    out, _ = x.communicate(bytes(f"{user}\n{exp}\n0\nx", "utf-8"))
    out = out.decode("utf-8")
    a = [x.group() for x in re.finditer("vmess://(.*)", out)]
    if a:
        return str(a)
    else:
        return "error"

@app.route("/trial-vmess")
def trial_vmess():
    user = "trialX" + str(random.randint(10, 1000))
    x = subprocess.Popen(
        ["add-ws"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
    )
    out, _ = x.communicate(bytes(f"{user}\n1\n0\nx", "utf-8"))
    out = out.decode("utf-8")
    a = [x.group() for x in re.finditer("vmess://(.*)", out)]
    return str(a)

@app.route("/trial-ssh")
def trial_ssh():
    trial = subprocess.check_output("echo trial`</dev/urandom tr -dc X-Z0-9 | head -c4`", shell=True).decode("ascii")
    subprocess.check_output(f'useradd -e `date -d "1 days" +"%Y-%m-%d"` -s /bin/false -M {trial}', shell=True)
    subprocess.check_output(f'usermod --password $(echo 1 | openssl passwd -1 -stdin) {trial}', shell=True)
    return trial + ":1"

@app.route("/adduser/exp")
def add_user_exp():
    u = request.args.get("user")
    p = request.args.get("password")
    exp = request.args.get("exp")
    try:
        subprocess.check_output(f'useradd -e `date -d "{exp} days" +"%Y-%m-%d"` -s /bin/false -M {u}', shell=True)
        subprocess.check_output(f'usermod --password $(echo {p} | openssl passwd -1 -stdin) {u}', shell=True)
    except Exception as e:
        return f"error: {str(e)}"
    return "success"

@app.route("/renew")
def renew():
    u = request.args.get("user")
    p = request.args.get("password")
    exp = request.args.get("exp")
    try:
        subprocess.check_output(f'userdel -f {u}', shell=True)
        subprocess.check_output(f'useradd -e `date -d "{exp} days" +"%Y-%m-%d"` -s /bin/false -M {u}', shell=True)
        subprocess.check_output(f'usermod --password $(echo {p} | openssl passwd -1 -stdin) {u}', shell=True)
        return "success"
    except Exception as e:
        return f"error: {str(e)}"

@app.route("/deluser")
def deluser():
    u = request.args.get("user")
    try:
        subprocess.check_output(f'userdel -f {u}', shell=True)
    except Exception as e:
        return f"error: {str(e)}"
    return "success"

if __name__ == "__main__":
    app.run(host=sys.argv[1], port=6969)
