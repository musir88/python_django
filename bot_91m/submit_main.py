import time
import requests
import json
import codecs
import random
import os
from selectolax.parser import HTMLParser
import asyncio

class submitMain():

    def joinChannel(self, res, x, ua_list):

        joinchannel_url = res['domain_name'] + "boss91m/join_channel"
        for x in res['data']:
            time.sleep(1)
            bot_url = joinchannel_url + "?channel=" + x['channel'] + "&session_string=" + x['session_string'] + "&admin=" + str(x['admin'])
            res_son = requests.get(bot_url, headers={'User-Agent': ua_list})
            res_son = HTMLParser(res_son.text).body.text()
            res_son = json.loads(res_son)
            # res_son['content'] = x['content']
            res_son['joinChannel'] = 'joinChannel'
            print(HTMLParser(res_son.text).body.text())

        return res['domain_name'] + "boss91m/channelVerify" + "?channel=" + x['channel'] + "&session_string=" + x['session_string']


    def joined_channel(self,res, x, ua_list):
        joinchannel_url = res['domain_name'] + "boss91m/send_message" + "?session_string=" + x['session_string'] + "&admin_id=" + str(x['admin_id'])
        for channel_id in x['channel']:
            time.sleep(1)
            bot_url = joinchannel_url + "&channel=" + channel_id + "&content=" + x['content'] + "&is_fake_content=2"
            res_son = requests.get(bot_url, headers={'User-Agent': ua_list})
            res_son = HTMLParser(res_son.text).body.text()
            res_son = json.loads(res_son)
            # res_son['content'] = x['content']
            res_son['joined_channel'] = 'joined_channel'
            print(res_son)
        return True


    def replyclient(self, res, x, ua_list):
        time.sleep(1)
        replyclient = requests.post(res['domain_name'] + "boss91m/replyclient", data=x)
        print(HTMLParser(replyclient.text).body.text())
        return True

    def savedialogpush(self, res, x, ua_list):
        res_son = requests.get(x['submit_url'], headers={'User-Agent': ua_list})
        res_son = HTMLParser(res_son.text).body.text()
        res_son = json.loads(res_son)
        res_son['submit_url'] = x['submit_url']
        print(res_son)
        return True


    def updateProfile(self, res, x, ua_list):
        joinchannel_url = res['domain_name'] + "boss91m/updateProfile"

        updateProfile = requests.post(joinchannel_url, data=x)
        res_son = HTMLParser(updateProfile.text).body.text()
        res_son = json.loads(res_son)
        # res_son['joinchannel_url'] = joinchannel_url
        # res_son['x'] = x
        print(res_son)
        # print(joinchannel_url)
        # print(x)
        return True

    def verifyChannel(self, res, x, ua_list):
        # time.sleep(3)
        time.sleep(1)
        joinchannel_url = res['domain_name'] + "boss91m/channelVerify" + "?channel=" + x['channel'] + "&session_string=" + x['session_string']
        updateProfile = requests.post(joinchannel_url, data=x)
        print(updateProfile)
        # res_son = HTMLParser(updateProfile.text).body.text()
        # res_son['joinchannel_url'] = joinchannel_url
        # res_son['text'] = 'verifyChannel'
        # print(res_son)
        return True


