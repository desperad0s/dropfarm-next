from playwright.async_api import async_playwright, Browser, Page
import logging
import os

logger = logging.getLogger(__name__)

class BrowserManager:
    def __init__(self):
        self._browser = None
        self._context = None
        self._page = None
    
    async def start(self):
        """Initialize browser session"""
        try:
            playwright = await async_playwright().start()
            self._browser = await playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage'
                ],
                channel="chromium"  # Use the installed Chromium
            )
            
            self._context = await self._browser.new_context(
                viewport=None,
                no_viewport=True
            )
            self._page = await self._context.new_page()
            await self._page.goto('https://web.telegram.org/k/')
            logger.info("Browser session started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start browser: {str(e)}")
            await self.cleanup()
            raise

    async def cleanup(self):
        """Clean up browser resources"""
        try:
            if self._page:
                await self._page.close()
            if self._context:
                await self._context.close()
            if self._browser:
                await self._browser.close()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

    @property
    def page(self) -> Page:
        """Get current page"""
        if not self._page:
            raise RuntimeError("Browser not initialized")
        return self._page

browser_manager = BrowserManager()