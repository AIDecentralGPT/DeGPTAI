from playwright.async_api import async_playwright
import re

class PlayWrightUtil:

    async def login_twitter(self, keyword: str):
        username = "BrookeHamp25599"
        password = "i1FpNoLs6EIVsUiu"
        email = "ydarsmjzaq@rambler.ru"
        async with async_playwright() as p:  # 使用async_playwright而不是sync_playwright
            browser = await p.chromium.launch(
                headless=True, 
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
            context = await browser.new_context(bypass_csp=True, ignore_https_errors=True,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            page = await context.new_page()

            try:
                # 导航到登录页面
                await page.goto("https://x.com/i/flow/login", wait_until="networkidle")

                # 输入用户名
                await page.wait_for_selector('input[autocomplete="username"]', timeout=3000)
                await page.screenshot(path='playwright/username.png')
                await page.fill('input[autocomplete="username"]', username)
                # await page.click('button[role="button"]:has-text("下一步")')
                await page.click('button[role="button"]:has-text("Next")')

                try:
                    # 输入邮箱验证
                    await page.wait_for_selector('input[data-testid="ocfEnterTextTextInput"]', timeout=3000)
                    await page.screenshot(path='playwright/email.png')
                    await page.fill('input[data-testid="ocfEnterTextTextInput"]', email)
                    # await page.click('button[role="button"]:has-text("下一步")')
                    await page.click('button[role="button"]:has-text("Next")')
                except:
                    print("没有邮箱验证")

                # 输入密码
                await page.wait_for_selector('input[name="password"]', timeout=3000)
                await page.screenshot(path='playwright/password.png')
                await page.fill('input[name="password"]', password)
                # 点击登录
                # await page.click('button[role="button"]:has-text("登录")')
                await page.click('button[role="button"]:has-text("Log in")')
                    
                # 等待登录成功
                await page.wait_for_selector('button[aria-label="账号菜单"]')
                await page.screenshot(path='playwright/accountmenu.png')
                print("登录成功！")

                # 现在可以访问需要登录的内容
                await page.goto(f'https://x.com/search?q={keyword}&src=typed_query')

                # 等待推文加载
                await page.wait_for_selector('article[data-testid="tweet"]')
                await page.screenshot(path='playwright/article.png')
                await self.scroll_to_load(page, scroll_times=4)
                
                # 提取推文信息
                tweet_datas = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('article[data-testid="tweet"]')).map(tweet => {
                        return {
                            username: tweet.querySelector('div[data-testid="User-Name"] a')?.innerText,
                            profile_image_url_https: tweet.querySelector('div[data-testid="User-Name"] img')?.src,
                            full_text: tweet.querySelector('div[data-testid="tweetText"]')?.innerText,
                            link: tweet.querySelector('div[data-testid="User-Name"] a[href*="/status/"]')?.href,
                            media_url_https: tweet.querySelector('div[data-testid="tweetPhoto"] img')?.src,
                            tweet_created_at: tweet.querySelector('time')?.dateTime,
                            like: tweet.querySelector('button[data-testid="like"]')?.innerText
                        };
                    })
                }''')
                
                # 重构
                tweet_tran = []
                for tweet_data in tweet_datas:
                    # 提取用户名和推文ID
                    link = tweet_data.get('link', '')
                    match = re.search(r'https?://x\.com/([^/]+)/status/(\d+)', link)
                    tweet_tran.append({
                        "name": tweet_data.get('username'),
                        "screen_name": match.group(1) if match else None,
                        "id_str": match.group(2) if match else None,
                        "profile_image_url": tweet_data.get('profile_image_url_https'),
                        "full_text": tweet_data.get('full_text'),
                        "media_url_https": tweet_data.get('media_url_https'),
                        "tweet_created_at": tweet_data.get('tweet_created_at'),
                        "favorite_count": tweet_data.get('like')
                    })
                await browser.close()
                return {"content": tweet_tran}
            except Exception as e:
                print(f"登录失败: {e}")
                await browser.close()
                return []

    # add page scroll
    async def scroll_to_load(self, page, scroll_times=3):
        for _ in range(scroll_times):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)

PlayWrightInstall = PlayWrightUtil()