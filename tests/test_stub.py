import unittest

import asynctest
from httpx import AsyncClient
from src.logic.tools.stub import Browser


class TestBrowser(asynctest.TestCase):
    def setUp(self):
        self.browser = Browser()
        self.browser.client = asynctest.CoroutineMock(spec=AsyncClient)

    async def test_successful_fetch(self):
        test_url = "http://test.com"
        expected_response = {"key": "value"}
        self.browser.client.get.return_value = asynctest.MagicMock()
        self.browser.client.get.return_value.json.return_value = expected_response

        response = await self.browser(test_url)

        self.browser.client.get.assert_called_once_with(test_url, headers=self.browser.headers)
        self.assertEqual(response, expected_response)

    async def test_unsuccessful_fetch(self):
        test_url = "http://test.com"
        self.browser.client.get.side_effect = Exception("Fetch failed")

        with self.assertRaises(Exception):
            await self.browser(test_url)

        self.browser.client.get.assert_called_once_with(test_url, headers=self.browser.headers)

    async def test_non_json_response(self):
        test_url = "http://test.com"
        self.browser.client.get.return_value = asynctest.MagicMock()
        self.browser.client.get.return_value.json.side_effect = JSONDecodeError("Invalid JSON", doc="", pos=0)

        with self.assertRaises(JSONDecodeError):
            await self.browser(test_url)

        self.browser.client.get.assert_called_once_with(test_url, headers=self.browser.headers)

if __name__ == "__main__":
    unittest.main()
