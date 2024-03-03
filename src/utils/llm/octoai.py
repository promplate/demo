new line(s) to replace


@link_llm("mixtral")
# Add unit tests for the `complete` method of the `OctoAI` class
def test_complete():
    # Test case 1
    prompt = "Hello"
    expected_result = "Hello, World!"
    assert octoai.complete(prompt) == expected_result

    # Test case 2
    prompt = "Goodbye"
    expected_result = "Goodbye, World!"
    assert octoai.complete(prompt) == expected_result


# Add unit tests for the `generate` method of the `OctoAI` class
def test_generate():
    # Test case 1
    prompt = "Hello"
    expected_result = ["Hello", "World!"]
    assert list(octoai.generate(prompt)) == expected_result

    # Test case 2
    prompt = "Goodbye"
    expected_result = ["Goodbye", "World!"]
    assert list(octoai.generate(prompt)) == expected_result
@link_llm("nous-hermes")
class OctoAI(AsyncChatOpenAI):
    async def complete(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config
        return (await complete(prompt, **config)).removeprefix(" ")

    async def generate(self, prompt: str | list[Message], /, **config):
        config = self._run_config | config

        first_token = True

        async for token in generate(prompt, **config):
            if token and first_token:
                first_token = False
                yield token.removeprefix(" ")
            else:
                yield token

    def bind(self, **run_config):  # type: ignore
        self._run_config.update(run_config)  # inplace
        return self


octoai = OctoAI().bind(model="nous-hermes-2-mixtral-8x7b-dpo")


octoai.complete = patch.chat.acomplete(octoai.complete)  # type: ignore
octoai.generate = patch.chat.agenerate(octoai.generate)  # type: ignore
