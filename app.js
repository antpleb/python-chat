#!javascript
'use strict';
const fs = require('fs');
const { spawn } = require('child_process');
const run = spawn("python", ["client.py"]);
const attempt_connect = {
    "attempt" : "false"
}
var possible_error = "";
var error = false;
fs.writeFileSync('test.txt', "test");
fs.writeFileSync('attempt_connect.json', attempt_connect);
fs.watchFile("error.json", (eventtype) => {
    if (eventtype == "change") {
        fs.readFile('error.json', 'utf8', (err, data) => {
            if (err) {
                return;
            }
            else {
                possible_error = data;
                error = true;
            }
        })
    }
});
var connect;
connect = false;
while (!connect){
    var ip = prompt("Please enter the host ip: ");
    if (ip != null || ip != "") {
        var port = prompt("Please enter the host port: ");
        if (port != null || port != "") {
            var username = prompt("Please enter your username: ");
            const connect_data = {
                "ip" : ip,
                "port" : port,
                "username" : username
            }
            fs.writeFileSync('connect_data.json', connect_data, 'utf8', callback);
            fs.watchFile('attempt_connect.json', (eventtype) => {
                if (eventtype == "change") {
                    fs.readFileSync('attempt_connect.json', 'utf8', (err, data) => {
                        if (err) {
                            return;
                        }
                        else {
                            if (JSON.stringify('attempt_connect.json')["attempt"] == "true"){
                                connect = true;
                            }
                        }
                    })
                }
            });
        }
    }
    
}
