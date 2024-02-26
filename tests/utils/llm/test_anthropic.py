from unittest.mock import Mock

import pytest
from utils.llm.anthropic import complete, generate, split


# Test split function
def test_split_with_system_message():
    prompt = [
        {"role": "system", "content": "System message"},
        {"role": "user", "content": "User message"},
    ]
    expected_messages = [{"role": "user", "content": "User message"}]
    expected_system_message = "System message"
    
    messages, system_message = split(prompt)
    
    assert messages == expected_messages
    assert system_message == expected_system_message

def test_split_without_system_message():
    prompt = [{"role": "user", "content": "User message"}]
    expected_messages = [{"role": "user", "content": "User message"}]
    expected_system_message = None
    
    messages, system_message = split(prompt)
    
    assert messages == expected_messages
    assert system_message == expected_system_message

# Test complete function
@pytest.mark.asyncio
async def test_complete():
    prompt = "User prompt"
    expected_completion_text = "Completion text"
    
    mock_anthropic = Mock()
    mock_anthropic.messages.create.return_value = Mock(content=[Mock(text=expected_completion_text)])
    
    result = await complete(prompt, anthropic=mock_anthropic)
    
    assert result == expected_completion_text
    mock_anthropic.messages.create.assert_called_once_with(
        messages=[{"role": "user", "content": prompt}],
        system=None,
        max_tokens=4096
    )

# Test generate function
@pytest.mark.asyncio
async def test_generate():
    prompt = "User prompt"
    expected_generated_text = "Generated text"
    
    mock_anthropic = Mock()
    mock_anthropic.messages.create.return_value.__aenter__.return_value = Mock()
    mock_anthropic.messages.create.return_value.__aenter__.return_value.__aiter__.return_value = [
        Mock(type="content_block_delta", delta=Mock(text=expected_generated_text))
    ]
    
    generated_texts = []
    async for text in generate(prompt, anthropic=mock_anthropic):
        generated_texts.append(text)
    
    assert generated_texts == [expected_generated_text]
    mock_anthropic.messages.create.assert_called_once_with(
        messages=[{"role": "user", "content": prompt}],
        system=None,
        max_tokens=4096,
        stream=True
    )
