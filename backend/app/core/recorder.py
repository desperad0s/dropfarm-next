from datetime import datetime
from typing import List, Dict, Any, Optional
from playwright.async_api import Page
import logging
import json

logger = logging.getLogger(__name__)

class Recorder:
    def __init__(self, page: Page):
        self.page = page
        self.recording = False
        self.steps: List[Dict[str, Any]] = []
        self.start_time: Optional[float] = None

    async def start_recording(self):
        """Start recording user actions"""
        try:
            self.recording = True
            self.start_time = datetime.now().timestamp()
            self.steps = []

            # Setup click listener
            await self.page.evaluate("""
                window.recordedClicks = [];
                document.addEventListener('click', function(e) {
                    if (!e.isTrusted) return;  // Only record real user clicks
                    
                    const rect = document.documentElement.getBoundingClientRect();
                    const x = e.clientX / rect.width;  // Store as percentage
                    const y = e.clientY / rect.height;
                    
                    window.recordedClicks.push({
                        type: 'click',
                        x: x,
                        y: y,
                        time: Date.now()
                    });
                }, true);
            """)

            logger.info("Recording started")
            return {"status": "recording_started"}

        except Exception as e:
            logger.error(f"Failed to start recording: {str(e)}")
            raise

    async def stop_recording(self) -> List[Dict[str, Any]]:
        """Stop recording and return recorded steps"""
        try:
            if not self.recording:
                return []

            # Get recorded clicks from browser
            recorded_clicks = await self.page.evaluate("window.recordedClicks")
            
            # Convert timestamps to relative time from start
            start_time = recorded_clicks[0]['time'] if recorded_clicks else 0
            
            self.steps = [{
                'type': 'click',
                'x': click['x'],
                'y': click['y'],
                'time': (click['time'] - start_time) / 1000  # Convert to seconds
            } for click in recorded_clicks]

            # Reset recording state
            await self.page.evaluate("window.recordedClicks = [];")
            self.recording = False
            
            logger.info(f"Recording stopped. Captured {len(self.steps)} steps")
            return self.steps

        except Exception as e:
            logger.error(f"Failed to stop recording: {str(e)}")
            raise
        finally:
            self.recording = False

    @property
    def is_recording(self) -> bool:
        return self.recording