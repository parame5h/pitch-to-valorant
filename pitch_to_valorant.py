import asyncio
import llm
import logging
from agents import jett,viper, sova, reyna, sage
from tools import utils



async def main():
    pitch = "An AI B2B startup that helps small businesses automate their customer support"
    keywords = utils.extract_keywords(pitch)
    
    jett_response, viper_response = await asyncio.gather(
    asyncio.to_thread(jett.ask_jett, pitch, keywords),
    asyncio.to_thread(viper.ask_viper, pitch, keywords),
)
    print("Waiting for 15 seconds before asking Reyna and Sova to avoid rate limiting...")
    await asyncio.sleep(15)

    reyna_response, sova_response = await asyncio.gather(
    asyncio.to_thread(reyna.ask_reyna, pitch, keywords),
    asyncio.to_thread(sova.ask_sova, pitch, keywords),
)   


    
    sage_response = await asyncio.to_thread(sage.ask_sage, jett_response, viper_response, reyna_response, sova_response)
    print(sage_response)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    