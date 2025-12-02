import requests
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from random import randint, choice, uniform

import asyncio
import concurrent.futures

import time
import argparse

urls = ["www.google.com"]

proxy_servers = [
    "154.194.12.101:80",
    "154.194.12.0:80",
    "133.18.234.13:80",
    "103.169.142.0:80",
    "109.135.16.145:8789",
    "85.208.200.185:8081",
    "103.169.142.105:80"
]

user_agents = [
    "Mozilla/5.0 (Linux; Android 16; SM-A536B Build/BP2A.250605.031.A3) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/142.0.7444.102 Mobile Safari/537.36 SznProhlizec/14.0.0a",
    "Mozilla/5.0 (iPad; CPU iPad OS 5_1_1 like Mac OS X) AppleWebKit/531.0 (KHTML, like Gecko) CriOS/20.0.813.0 Mobile/96L305 Safari/531.0",
    "Mozilla/5.0 (Linux; Android 16; SM-A156B Build/BP2A.250605.031.A3) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/142.0.7444.102 Mobile Safari/537.36 SznProhlizec/14.0.0a"
]

brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

chrome_options = Options()
# chrome_options.binary_location = brave_path
chrome_options.add_argument("--headless")  # run without GUI
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

is_stealth = False
is_proxied = False
is_debug = False

async def dovisit(T):
    delay = uniform(0.0, 1.0) * T
    await asyncio.sleep(delay)
    
    rv = 0
    try:
        prx = "-"
        if is_proxied:
            prx = str.strip(choice(proxy_servers))
            chrome_options.add_argument(f"--proxy-server={prx}")

        ua = choice(user_agents)        
        chrome_options.add_argument(f"--user-agent={ua}")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        if (stealth):
            stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        
        # print(f"> {delay} {idproxy}")
        u = randint(0, len(urls)-1)
        driver.get(urls[u])

        # print(f"  - {driver.title}")
        rv = (driver.title, ua, prx) if is_debug else (f"{delay:.3f}", u, prx)

        time.sleep(randint(2,3))
        # driver.save_screenshot(f"screenshot/spage-{delay}-{randint(0,999)}.png")

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_script("return navigator.language")

        driver.quit()
    except Exception as e:
        rv = (-1, f"{str(e)}", ua, prx)

    return rv

def done_callback(inp):
    try:
        res = inp.result()
        print(f"{inp.get_name()}: {res}")
    except asyncio.CancelledError:
        print(f"- Cancelled")
    except Exception as e:
        print(f"- Callback raised: {e}")

async def main(T, N, stealth=False):
    tasks = set()

    for i in range(N):
        t = asyncio.create_task(dovisit(T))
        t.add_done_callback(done_callback)

        tasks.add(t)

    await asyncio.gather(*tasks)
    # await asyncio.sleep(300)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ninja traffic for website"
    )

    parser.add_argument("T", type=int, help="Total duration push")
    parser.add_argument("N", type=int, help="Total ninja traffic generated")
    parser.add_argument("--url-file", type=str, help="File containing target URLs")
    parser.add_argument("--proxy-file", type=str, help="File containing proxy")
    parser.add_argument("--ua-file", type=str, help="File containing user-agents")
    parser.add_argument("--stealth", action="store_true", help="Use stealth mode")
    parser.add_argument("--proxy", action="store_true", help="Use proxies")
    parser.add_argument("--debug", action="store_true", help="Print debug")

    T = 1800
    N = 100
    the_url = ""
    the_proxy = ""
    the_ua = ""
    
    args = parser.parse_args()

    T = args.T
    N = args.N
    the_url = args.url_file if args.url_file is not None else "" 
    the_proxy = args.proxy_file if args.proxy_file is not None else ""
    the_ua = args.ua_file if args.ua_file is not None else ""

    is_stealth = args.stealth
    is_proxied = args.proxy
    is_debug = args.debug

    if len(the_proxy) > 0:
        is_proxied = True
        with open(the_proxy, "r") as f:
            proxy_servers = f.readlines()
            f.close()

    if len(the_url) > 0:
        with open(the_url, "r") as f:
            urls = f.readlines()
            f.close()

    if len(the_ua) > 0:
        with open(the_ua, "r") as f:
            user_agents = f.readlines()
            f.close()
    
    # print(f"{T} {N} {the_url} {the_proxy} {args.stealth}")
    # print(f"{urls}")

    asyncio.run(main(T, N))
