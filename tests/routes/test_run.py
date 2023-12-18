import unittest
from unittest.mock import Mock, patch

from src.logic.main import EOC
from src.routes.run import stream


class TestRun(unittest.TestCase):
    @patch("src.routes.run.get_node")
    @patch("src.routes.run.server_sent_events")
    @patch("src.routes.run.server_sent_events")
    async def test_stream(self, mock_sse, mock_get_node):
        mock_node = Mock()
        mock_context = Mock()
        mock_get_node.return_value = mock_node
        mock_astream = Mock(return_value=[{"parsed": "data", "partial": True}])
        mock_get_node.return_value.astream = mock_astream

        response = await stream(mock_node, mock_context, astream_func=mock_astream)

        mock_get_node.assert_called_once_with(mock_node)
        mock_astream.assert_called_once_with(mock_context.model_dump(exclude_unset=True) | {"<stream>": True})
        self.assertEqual(response.body, b'data: "partial", "data"\n\n')

        mock_astream.side_effect = EOC()
        response = await stream(mock_node, mock_context, astream_func=mock_astream)
        self.assertEqual(response.body, b'event: complete\ndata: {}\n\n')

        mock_astream.side_effect = Exception()
        response = await stream(mock_node, mock_context)
        self.assertTrue(b'event: error' in response.body)


if __name__ == "__main__":
    unittest.main()
