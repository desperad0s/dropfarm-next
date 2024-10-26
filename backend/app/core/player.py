from typing import List, Dict, Any, Optional
from playwright.async_api import Page
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Player:
    def __init__(self, page: Page):
        self.page = page
        self.playing = False
        self.stop_requested = False

    async def play_steps(self, steps: List[Dict[str, Any]], repeat: bool = False):
        """Play recorded steps"""
        try:
            self.playing = True
            self.stop_requested = False
            
            while not self.stop_requested:
                start_time = datetime.now().timestamp()
                
                for step in steps:
                    if self.stop_requested:
                        break

                    # Calculate wait time
                    current_time = datetime.now().timestamp() - start_time
                    wait_time = step['time'] - current_time
                    if wait_time > 0:
                        await asyncio.sleep(wait_time)

                    # Execute step
                    if step['type'] == 'click':
                        await self._execute_click(step['x'], step['y'])

                    # Update progress
                    logger.debug(f"Executed step: {step}")

                if not repeat:
                    break

            return {"status": "playback_completed"}

        except Exception as e:
            logger.error(f"Playback error: {str(e)}")
            raise
        finally:
            self.playing = False

    async def stop_playback(self):
        """Stop ongoing playback"""
        self.stop_requested = True
        while self.playing:
            await asyncio.sleep(0.1)
        return {"status": "playback_stopped"}

    async def _execute_click(self, x: float, y: float):
        """Execute a click at relative coordinates"""
        try:
            # Get viewport size
            viewport = await self.page.evaluate("""() => ({
                width: document.documentElement.clientWidth,
                height: document.documentElement.clientHeight
            })""")
            
            # Convert relative to absolute coordinates
            abs_x = x * viewport['width']
            abs_y = y * viewport['height']

            # Execute click
            await self.page.mouse.click(abs_x, abs_y)

        except Exception as e:
            logger.error(f"Click execution failed: {str(e)}")
            raise

    @property
    def is_playing(self) -> bool:
        return self.playing