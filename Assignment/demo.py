import asyncio
from playwright.async_api import async_playwright # type: ignore

"""
#1 successfully logged in?
#2 incorrect password then app should throw in an error
#3 if we picked a locked user, it should display as such
"""
async def test_login(user_credentials: list[dict]):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto('https://www.saucedemo.com/')
        
        for credentials in user_credentials:
            user_name = credentials['username']
            password = credentials['password']
            
            print(f'Testing for credentilas Username= {user_name} and Password= {password}')
            
            await page.fill('#user-name',user_name)
            await page.fill('#password',password)
            await page.click('#login-button')
            
            try:
                await page.wait_for_selector("h3[data-test='error']",timeout=3000)
                error_message = await page.inner_text("h3[data-test='error']")
                print(f'Invalid login for Username {user_name} and Password {password} : {error_message}')
                
            except:
                try:
                    await page.wait_for_selector(".inventory_list",timeout=3000)
                    print(f'Successfully logged in!')
                except:
                    print(f'Login failed!')
            await page.goto('https://www.saucedemo.com/')
        await browser.close()
        
test_users = [
    {
        "username": "standard_user", "password":"secret_sauce",
    },
    {
        "username": "standard_user", "password":"123"
    },
    {
        "username": "locked_out_user", "password":"secret_sauce",

    }
]

asyncio.run(test_login(test_users))
