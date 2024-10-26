from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from ..core.browser import browser_manager
from ..core.recorder import Recorder
from ..core.player import Player

router = APIRouter()

# Store instances for active sessions
active_recorders: Dict[str, Recorder] = {}
active_players: Dict[str, Player] = {}

@router.post("/record/{routine_id}/start")
async def start_recording(routine_id: str):
    """Start recording a new routine"""
    try:
        if routine_id in active_recorders:
            raise HTTPException(400, "Recording already in progress")

        recorder = Recorder(browser_manager.page)
        active_recorders[routine_id] = recorder
        
        return await recorder.start_recording()

    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/record/{routine_id}/stop")
async def stop_recording(routine_id: str):
    """Stop recording and save steps"""
    try:
        recorder = active_recorders.get(routine_id)
        if not recorder:
            raise HTTPException(404, "No active recording found")

        steps = await recorder.stop_recording()
        del active_recorders[routine_id]
        
        return {"steps": steps}

    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/play/{routine_id}")
async def start_playback(
    routine_id: str,
    steps: List[Dict[str, Any]],
    repeat: bool = False
):
    """Start routine playback"""
    try:
        if routine_id in active_players:
            raise HTTPException(400, "Playback already in progress")

        player = Player(browser_manager.page)
        active_players[routine_id] = player
        
        # Start playback in background
        background_tasks = BackgroundTasks()
        background_tasks.add_task(player.play_steps, steps, repeat)
        
        return {"status": "playback_started"}

    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/play/{routine_id}/stop")
async def stop_playback(routine_id: str):
    """Stop routine playback"""
    try:
        player = active_players.get(routine_id)
        if not player:
            raise HTTPException(404, "No active playback found")

        await player.stop_playback()
        del active_players[routine_id]
        
        return {"status": "playback_stopped"}

    except Exception as e:
        raise HTTPException(500, str(e))