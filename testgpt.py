import os
from sydney import SydneyClient
import asyncio

os.environ["BING_COOKIES"] = "1lKi7iFasOqQklxeN7F-YgDKh07IFW8Jh-6K3FyaZ9KSD4_CPOSAGCSFxFIUF4axA064bfOliqIhm1IxmZnfEF2OgbJTOBrHSBiqfu080hDBHaWShAeeFaDwrgik-6YILfhD3Rqvqom358u5-5lG6r0QKfqvuJqH55bXSyjPW6ozf9x9Kpy1ww7kFauGzJl5FRLqm4ZSlXMsBbQx262Kk0A"


async def main() -> None:
    async with SydneyClient() as sydney:
        while True:
            prompt = input("You: ")

            if prompt == "!reset":
                await sydney.reset_conversation()
                continue
            elif prompt == "!exit":
                break

            print("Sydney: ", end="", flush=True)
            async for response in sydney.ask_stream(prompt):
                print(response, end="", flush=True)
            print("\n")


if __name__ == "__main__":
    asyncio.run(main())