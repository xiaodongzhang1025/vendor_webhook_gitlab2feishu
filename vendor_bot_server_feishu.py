#-*- coding: UTF-8 -*-
from bottle import Bottle, route, run, request, template, static_file
from time import localtime,strftime
import os
import sys
import requests
import gitlab
import json
from xml.dom.minidom import parse
import xml.dom.minidom

#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf8')

app = Bottle()
ACCESS_CODE = "qigan2016"

@app.route('/')
@app.route('/<path>')
def index(path='index'):
    print (request.method)  #POST
    print strftime("%Y-%m-%d %A %H:%M:%S",localtime())
    print "./", path
    return static_file("%s.html"%path, root='./html/')
    
@app.route('/css/<path>', method='GET')
def index(path):
    print (request.method)  #POST
    print strftime("%Y-%m-%d %A %H:%M:%S",localtime())
    print "./css", path
    return static_file("%s"%path, root='./css/')
##########################################################

@app.route('/vendor_bot', method='POST')
#@app.route('/vendor_bot', method='GET')
#@app.route('/vendor_bot') 
def vendor_bot():
    feishu_bot_url="https://open.feishu.cn/open-apis/bot/v2/hook/b5249baf-809b-497c-9220-9080edc38fb5"
    result = False
    post_string = ''
    post_dict = {}
    #print (request.method)  
    #print strftime("%Y-%m-%d %A %H:%M:%S",localtime())
    if request.method == "GET":
        print "==> GET..."
    elif request.method == "POST":
        print "==> POST..."
    try:
        # bottle for gitlab system hook function
        for key in request.params.keys():
            post_string = post_string + key
        for value in request.params.values():
            post_string = post_string + value
            
        #print '--------------------------------'
        #print post_string
        post_dict = json.loads(post_string)
        print type(post_dict), post_dict
        
        print "event_name", post_dict.get("event_name")
        print "push_options", post_dict.get("push_options")
        if post_dict.get("event_name") == "push":
            result = True
            push_before = post_dict.get("before")
            push_after = post_dict.get("after")
            commits = post_dict.get("commits")
            for commit in commits:
                commit_url = commit.get("url")
                commit_id = commit.get("id")
                commit_timestamp = commit.get("timestamp")
                author_dict = commit.get("author")
                commit_author_name = author_dict.get("name")
                commit_msg = commit.get("message")
                commit_repository_dict = post_dict.get("repository")
                commit_repository_name = "NULL"
                if commit_repository_dict:
                    commit_repository_name = commit_repository_dict.get("name")
                commit_branch = post_dict.get("ref")
                if commit_branch.startswith('refs/heads/'):
                    commit_branch = commit_branch[len('refs/heads/'):]
                print "--------"
                #print "commit_id", commit_id
                #print "commit_url", commit_url
                #print "commit_timestamp", commit_timestamp
                #print "commit_author_name", commit_author_name
                #print "commit_msg", commit_msg
                #print "commit_repository", commit_repository
                #print "commit_branch", commit_branch
                ##################################################################
                feishu_text_msg = commit_author_name + " pushed to branch " + commit_branch + " at repository " + commit_repository_name + "\r\n    " + commit_id[0:8] + ": " + commit_msg + "\r\n    " + commit_url
                feishu_text_data = {}
                dict_content = {}
                dict_content["text"] = feishu_text_msg
                feishu_text_data["msg_type"] = "text"
                feishu_text_data["content"] = dict_content
                print feishu_text_data
                ##################################################################
                feishu_rich_text_data = {}
                dict_content = {}
                dict_content["post"] = {"zh_cn":{"title": commit_author_name + " pushed to branch " + commit_branch + " at repository " + commit_repository_name, 
                                                "content": [
                                                                #第一行
                                                                [
                                                                    {
                                                                        "tag": "a",
                                                                        "text": commit_id[0:8],
                                                                        "href": commit_url
                                                                    },
                                                                    {
                                                                        "tag": "text",
                                                                        "text": ": "
                                                                    }
                                                                ],
                                                                #第二行
                                                                [
                                                                    {
                                                                        "tag": "text",
                                                                        "text": commit_msg
                                                                    }
                                                                ]
                                                            ]
                                                }
                                        }
                feishu_rich_text_data["msg_type"] = "post"
                feishu_rich_text_data["content"] = dict_content
                print feishu_rich_text_data
                ##################################################################
                feishu_headers = {"Content-Type": "application/json"}
                response = requests.post(feishu_bot_url, headers=feishu_headers, data=json.dumps(feishu_rich_text_data))
                print response, response.json()
        
    except Exception, err:
        #print err
        print '===> Exception'
        print str(err).decode("string_escape")
    finally:
        print '===> Finally'
    content = """
创建失败
"""
    if result == True:
        content = """
创建成功
"""
    return content

if __name__ == '__main__':
    run(app, host = '0.0.0.0', port = 6666)
