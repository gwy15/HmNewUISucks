'''
实现 MITM 的主体插件
'''
import os
import re
import gzip
import zlib
import json

from mitmproxy import http

dataVersion = '20180909' + '01'
resVersion = '20180909' + '123456'
manifestUrl = 'https://github.com/gwy15/HmNewUISucksData/raw/master/warshipgirlsr.manifest.gz'


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
        pass

    @catch
    def request(self, flow: http.HTTPFlow):
        if 'jr.moefantasy.com' not in flow.request.host:
            flow.response = http.HTTPResponse.make(404, b'')

        # print(f'requesting {flow.request.url}')
        if flow.request.url.find('index/getInitConfigs') > 0:
            self.onGetInitConfigs(flow)

    @catch
    def response(self, flow: http.HTTPFlow):
        print(f'response host: {flow.request.host}')
        if re.match(self.VERSION_HOST, flow.request.host):
            self.onVersionCheck(flow)
        elif 'jr.moefantasy.com/active/getUserData/' in flow.request.url:
            self.onActiveGetUserData(flow)

    def onGetInitConfigs(self, flow):
        '替换 getInitConfigs'
        print('replacing getInitConfigs...')
        if os.path.exists('cache/init.dat'):
            with open('cache/init.dat', 'rb') as f:
                data = f.read()
        else:
            data = gzip.compress(open('cache/init.txt', 'rb').read())
            with open('cache/init.dat', 'wb') as f:
                f.write(data)

        flow.response = http.HTTPResponse.make(200, data)

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

        data = json.loads(
            zlib.decompress(flow.response.get_content()).decode())

        data['DataVersion'] = dataVersion
        data['ResVersion'] = resVersion

        flow.response.set_content(
            zlib.compress(json.dumps(data).encode()))


def request(flow):
    return ZjsnHelper().request(flow)


def http_connect(flow):
    return ZjsnHelper().http_connect(flow)


def response(flow):
    return ZjsnHelper().response(flow)
