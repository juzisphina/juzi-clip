"""Offline tests of proxy parsing, route order and messages. Run: python -m unittest -v"""
import unittest
from unittest import mock

from clipsaver import net
from clipsaver.i18n import set_lang


class ParseTest(unittest.TestCase):
    def test_forms(self):
        self.assertEqual(net.parse_proxy('127.0.0.1:7890'), 'http://127.0.0.1:7890')
        self.assertEqual(net.parse_proxy('http://127.0.0.1:7890/'), 'http://127.0.0.1:7890')
        self.assertEqual(net.parse_proxy('socks5h://127.0.0.1:7891'), 'socks5://127.0.0.1:7891')
        self.assertEqual(net.parse_proxy(' SOCKS5://localhost:1080 '), 'socks5://localhost:1080')
        for bad in ('', 'abc', '127.0.0.1', 'ftp://1.2.3.4:21', '127.0.0.1:99999'):
            self.assertIsNone(net.parse_proxy(bad), bad)


class RoutesTest(unittest.TestCase):
    def test_switch_and_order(self):
        with mock.patch.object(net, 'known_type', side_effect=lambda p: p):
            on = net.routes(True, ['127.0.0.1:7892', 'socks5://127.0.0.1:7890', '127.0.0.1:7892'])
            self.assertEqual([r.proxy for r in on],
                             ['http://127.0.0.1:7892', 'socks5://127.0.0.1:7890', None])   # list order, no repeats, direct last
            self.assertEqual([r.proxy for r in net.routes(False, ['127.0.0.1:7892'])], [None])


class MessageTest(unittest.TestCase):
    def setUp(self):
        set_lang('hans')

    def tearDown(self):
        set_lang('hant')

    def test_friendly(self):
        self.assertIn('没有程序', net.friendly('ConnectionRefusedError: [Errno 61] Connection refused'))
        self.assertIn('超时', net.friendly('TimeoutError: timed out'))
        self.assertIn('证书', net.friendly('SSLCertVerificationError: certificate verify failed'))
        self.assertIn('端口类型不对', net.friendly('RemoteDisconnected: Remote end closed connection without response'))
        set_lang('hant')    # 繁體 (default) uses Taiwan wording
        self.assertEqual(net.friendly('TimeoutError: timed out'), '逾時')
        self.assertEqual(net.friendly('SSLCertVerificationError: certificate verify failed'), '憑證驗證失敗')
        self.assertEqual(net.friendly('ConnectionRefusedError: refused'), '這個連接埠沒有程式在用')


class HantTest(unittest.TestCase):
    def test_taiwan_wording(self):
        from clipsaver.hant import to_hant
        self.assertEqual(to_hant('把帖子链接粘贴到这里'), '把貼文連結貼到這裡')
        self.assertEqual(to_hant('下载视频'), '下載影片')
        self.assertEqual(to_hant('打开网络设置'), '打開網路設定')
        self.assertEqual(to_hant('复制错误信息'), '複製錯誤訊息')

    def test_certificates_bundled_when_available(self):
        ctx = net.ssl_context()
        self.assertTrue(ctx.check_hostname)


if __name__ == '__main__':
    unittest.main()
