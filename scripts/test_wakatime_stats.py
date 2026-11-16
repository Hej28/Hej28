import contextlib
import io
import unittest
from unittest.mock import Mock
from urllib.error import HTTPError, URLError

from wakatime_stats import load_weekly


class WeeklyStatsTests(unittest.TestCase):
    def test_oauth_header_and_precedence(self):
        data = {'languages': [{'name': 'Python', 'text': '1 hr', 'percent': 100}], 'is_up_to_date': True}
        fetch = Mock(return_value={'data': data})
        weekly, status, _ = load_weekly(fetch, ' personal-token\n', 'old-plugin-key')
        self.assertEqual(weekly, data)
        self.assertEqual(status, '最近 7 天 · WakaTime')
        self.assertEqual(fetch.call_args.kwargs['headers']['Authorization'], 'Bearer personal-token')
        self.assertNotIn('personal-token', fetch.call_args.args[0])

    def test_legacy_secret_can_contain_oauth_token(self):
        fetch = Mock(return_value={'data': {'languages': []}})
        load_weekly(fetch, legacy_key='personal-token')
        self.assertEqual(fetch.call_args.kwargs['headers']['Authorization'], 'Bearer personal-token')

    def test_missing_credentials_does_not_request(self):
        fetch = Mock()
        weekly, status, _ = load_weekly(fetch)
        self.assertIsNone(weekly)
        self.assertEqual(status, 'WakaTime 尚未連接')
        fetch.assert_not_called()

    def test_auth_errors_are_actionable_and_do_not_log_secrets(self):
        for code in (401, 403):
            with self.subTest(code=code):
                fetch = Mock(side_effect=HTTPError('https://example.invalid/secret-token', code, 'secret-token', {}, io.BytesIO(b'secret-token')))
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    weekly, status, _ = load_weekly(fetch, 'secret-token')
                self.assertIsNone(weekly)
                self.assertEqual(status, 'WakaTime 需要更新授權')
                self.assertIn(str(code), output.getvalue())
                self.assertNotIn('secret-token', output.getvalue())

    def test_empty_stats_and_calculating_stats_are_distinct(self):
        ready = load_weekly(Mock(return_value={'data': {'languages': [], 'is_up_to_date': True}}), 'token')
        pending = load_weekly(Mock(return_value={'data': {'languages': [], 'is_up_to_date': False}}), 'token')
        self.assertIsNotNone(ready[0])
        self.assertNotEqual(ready[1], pending[1])

    def test_transient_failures_and_invalid_payloads(self):
        for failure in (URLError('secret-token'), TimeoutError('secret-token'), HTTPError('https://example.invalid', 503, 'secret-token', {}, None)):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = load_weekly(Mock(side_effect=failure), 'secret-token')
            self.assertEqual(result[1], 'WakaTime 暫時無法更新')
            self.assertNotIn('secret-token', output.getvalue())
        for payload in ({}, {'data': None}, {'data': {'languages': 'invalid'}}):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertIsNone(load_weekly(Mock(return_value=payload), 'token')[0])
        with contextlib.redirect_stdout(io.StringIO()):
            limited = load_weekly(Mock(side_effect=HTTPError('https://example.invalid', 429, '', {}, None)), 'token')
        self.assertEqual(limited[1], 'WakaTime 稍後重試')


if __name__ == '__main__':
    unittest.main()
