'''
实现 MITM 的主体插件
'''

import re
import gzip
import json

from mitmproxy import http

dataVersion = '20180909' + '01'
resVersion = '20180909' + '123456'
# TODO: update static server
manifestUrl = f'http://192.168.137.1:8000/cache/warshipgirlsr.manifest.gz'


def catch(func):
    def newfunc(*args, **kws):
        try:
            return func(*args, **kws)
        except Exception as ex:
            import traceback
            traceback.print_exc()
            raise
    return newfunc


class ZjsnHelper:
    VERSION_HOST = re.compile(r'version(\.channel)?\.jr\.moefantasy\.com')

    @catch
    def http_connect(self, flow):
        print(f'connecting {flow.request.url}')

    @catch
    def request(self, flow: http.HTTPFlow):
        print(f'requesting {flow.request.url}')
        # NOTICE: ignore for now
        if flow.request.url.find('index/getInitConfigs') > 0:
            # self.onGetInitConfigs(flow)
            pass

    @catch
    def response(self, flow: http.HTTPFlow):
        print(f'response host: {flow.request.host}')
        if re.match(self.VERSION_HOST, flow.request.host):
            self.onVersionCheck(flow)
            return
        if re.match(r'login(ios)\.jr\.moefantasy\.com', flow.request.host):
            print(flow.response)

    def onGetInitConfigs(self, flow):
        '替换 getInitConfigs'
        print('replacing getInitConfigs...')
        flow.response = http.HTTPResponse.make(
            200,
            gzip.compress(open('cache/init.txt', 'rb').read())
        )

    def onVersionCheck(self, flow: http.HTTPFlow):
        '替换 version check'
        print('replacing version check...')
        data = json.loads(flow.response.get_text())

        data['DataVersion'] = dataVersion
        data['ResVersion'] = resVersion
        data['ResUrl'] = manifestUrl
        data['ResUrlWu'] = manifestUrl
        data['version']['DataVersion'] = dataVersion
        data['version']['isMandatory'] = 0
        data['version']['newVersionId'] = '3.8.0'
        data['version']['hasNewVersion'] = 0

        flow.response.set_text(json.dumps(data))

    def onActiveGetUserData(self, flow):
        print('replacing active/getUserData')
        data = json.loads(flow.response.get_text())

        data['DataVersion'] = dataVersion
        data['ResVersion'] = resVersion

        flow.response.set_text(json.dumps(data))


def request(flow):
    return ZjsnHelper().request(flow)


def http_connect(flow):
    return ZjsnHelper().http_connect(flow)


def response(flow):
    return ZjsnHelper().response(flow)
