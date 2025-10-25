"""
Event Poller - Polls for calendar events and detects changes
"""

import asyncio
import logging
import os
import random
from datetime import datetime
from typing import Dict, Any, List

import httpx

logger = logging.getLogger("event_poller")
logging.basicConfig(level=logging.INFO)

# Configuration
POLL_INTERVAL_SEC = 5  # Poll every 5 seconds
MAX_JITTER_SEC = 1  # Random jitter to avoid collisions
BACKOFF_BASE = 2  # Backoff multiplier for errors
POLL_ENABLED = os.getenv("ENABLE_EVENT_POLLER", "1") == "1"
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class EventPoller:
    """Event poller that monitors calendar events for changes"""

    def __init__(self):
        self.running = False
        self.poll_task = None
        self.client = None
        self.prev_events = {}  # Previous snapshot: {id: event}
        self.lock = asyncio.Lock()
        self.backoff = 0

    async def get_today_events(self) -> List[dict]:
        """Get today's events from the API"""
        try:
            # Ensure client is available and not closed
            if not self.client or self.client.is_closed:
                logger.warning("HTTP client is closed, recreating...")
                self.client = httpx.AsyncClient(http2=True, timeout=10)

            # Call our own API endpoint
            response = await self.client.get(
                f"{API_BASE_URL}/calendar/events/today", timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get("events", [])
        except Exception as e:
            logger.error(f"Failed to get today's events: {e}")
            raise

    def diff_events(self, prev: Dict[str, dict], curr_list: List[dict]) -> tuple:
        """Compare previous and current events to find changes"""
        curr = {e["id"]: e for e in curr_list}

        # Find added events
        added = [e for event_id, e in curr.items() if event_id not in prev]

        # Find removed events
        removed = [e for event_id, e in prev.items() if event_id not in curr]

        # Find updated events (compare updated_at or modified fields)
        updated = []
        for event_id, e in curr.items():
            if event_id in prev:
                prev_event = prev[event_id]
                # Check if event was modified (compare relevant fields)
                if (
                    e.get("updated_at") != prev_event.get("updated_at")
                    or e.get("title") != prev_event.get("title")
                    or e.get("description") != prev_event.get("description")
                    or e.get("location") != prev_event.get("location")
                ):
                    updated.append(e)

        return added, updated, removed, curr

    def log_changes(self, added: List[dict], updated: List[dict], removed: List[dict]):
        """Log detected changes with detailed object information"""
        if added:
            logger.info(f"ADDED {len(added)} events:")
            for event in added:
                logger.info(f"  + {event.get('title', 'Untitled')} (ID: {event.get('id')})")
                logger.info(f"    Start: {event.get('when', {}).get('start_time', 'N/A')}")
                logger.info(f"    End: {event.get('when', {}).get('end_time', 'N/A')}")
                logger.info(f"    Location: {event.get('location', 'N/A')}")
                logger.info(f"    Description: {event.get('description', 'N/A')}")
                logger.info(f"    Participants: {len(event.get('participants', []))}")
                logger.info(f"    Updated: {event.get('updated_at', 'N/A')}")
                logger.info("    " + "="*50)

        if updated:
            logger.info(f"UPDATED {len(updated)} events:")
            for event in updated:
                event_id = event.get('id')
                old_event = self.prev_events.get(event_id, {})
                
                logger.info(f"  ~ {event.get('title', 'Untitled')} (ID: {event_id})")
                
                self._log_field_changes("Title", old_event.get('title'), event.get('title'))
                self._log_field_changes("Description", old_event.get('description'), event.get('description'))
                self._log_field_changes("Location", old_event.get('location'), event.get('location'))
                self._log_field_changes("Start Time", old_event.get('when', {}).get('start_time'), event.get('when', {}).get('start_time'))
                self._log_field_changes("End Time", old_event.get('when', {}).get('end_time'), event.get('when', {}).get('end_time'))
                self._log_field_changes("Updated At", old_event.get('updated_at'), event.get('updated_at'))
                
                # Log participants changes
                old_participants = old_event.get('participants', [])
                new_participants = event.get('participants', [])
                if old_participants != new_participants:
                    logger.info(f"    Participants changed:")
                    logger.info(f"      OLD: {[p.get('email') for p in old_participants]}")
                    logger.info(f"      NEW: {[p.get('email') for p in new_participants]}")
                
                logger.info("    " + "="*50)

        if removed:
            logger.info(f"REMOVED {len(removed)} events:")
            for event in removed:
                logger.info(f"  - {event.get('title', 'Untitled')} (ID: {event.get('id')})")
                logger.info(f"    Was scheduled: {event.get('when', {}).get('start_time', 'N/A')}")
                logger.info(f"    Location: {event.get('location', 'N/A')}")
                logger.info(f"    Had {len(event.get('participants', []))} participants")
                logger.info("    " + "="*50)
    
    def _log_field_changes(self, field_name: str, old_value, new_value):
        """Log individual field changes"""
        if old_value != new_value:
            logger.info(f"    {field_name}:")
            logger.info(f"      OLD: {old_value}")
            logger.info(f"      NEW: {new_value}")
    
    def log_full_objects(self, added: List[dict], updated: List[dict], removed: List[dict]):
        """Log complete objects for debugging"""
        if added:
            logger.info("FULL OBJECTS - ADDED EVENTS:")
            for i, event in enumerate(added, 1):
                logger.info(f"  Event {i}:")
                logger.info(f"    {event}")
                logger.info("    " + "-"*30)
        
        if updated:
            logger.info("FULL OBJECTS - UPDATED EVENTS:")
            for i, event in enumerate(updated, 1):
                event_id = event.get('id')
                old_event = self.prev_events.get(event_id, {})
                logger.info(f"  Event {i} (ID: {event_id}):")
                logger.info(f"    OLD OBJECT: {old_event}")
                logger.info(f"    NEW OBJECT: {event}")
                logger.info("    " + "-"*30)
        
        if removed:
            logger.info("FULL OBJECTS - REMOVED EVENTS:")
            for i, event in enumerate(removed, 1):
                logger.info(f"  Event {i}:")
                logger.info(f"    {event}")
                logger.info("    " + "-"*30)

    async def poll_once(self):
        """Perform a single poll operation"""
        try:
            # Get current events
            events = await self.get_today_events()

            # Compare with previous snapshot
            added, updated, removed, snapshot = self.diff_events(
                self.prev_events, events
            )

            # Log changes if any
            if added or updated or removed:
                logger.info(f"Event changes detected at {datetime.now().isoformat()}")
                
                # Log detailed changes
                self.log_changes(added, updated, removed)
                
                # Log full objects for debugging (if enabled)
                self.log_full_objects(added, updated, removed)

                # Update snapshot
                self.prev_events = snapshot

                await self.handle_event_changes(added, updated, removed)
            else:
                logger.debug("No event changes detected")

            # Reset backoff on success
            self.backoff = 0

        except Exception as e:
            logger.warning(f"Poll failed: {e}")
            self.backoff = min(4, self.backoff + 1)  # Max 4 backoff steps

    async def handle_event_changes(
        self, added: List[dict], updated: List[dict], removed: List[dict]
    ):
        """Handle detected event changes - override this for custom logic"""
        pass

    async def poller_loop(self):
        """Main polling loop"""
        logger.info("Event poller started")

        while self.running:
            # Avoid overlapping polls
            if self.lock.locked():
                await asyncio.sleep(0.1)
                continue

            async with self.lock:
                await self.poll_once()

            # Calculate sleep time with backoff and jitter
            base_interval = POLL_INTERVAL_SEC * (2**self.backoff if self.backoff else 1)
            jitter = random.uniform(0, MAX_JITTER_SEC)
            sleep_time = base_interval + jitter

            logger.debug(f"Sleeping for {sleep_time:.1f}s (backoff: {self.backoff})")
            await asyncio.sleep(sleep_time)

        logger.info("Event poller stopped")

    async def start(self):
        """Start the poller"""
        if not POLL_ENABLED:
            logger.info("Event poller disabled via ENABLE_EVENT_POLLER env var")
            return

        if self.running:
            logger.warning("Poller already running")
            return

        # Initialize HTTP client
        self.client = httpx.AsyncClient(http2=True, timeout=10)

        # Start polling
        self.running = True
        self.poll_task = asyncio.create_task(self.poller_loop())
        logger.info(f"Event poller started - API URL: {API_BASE_URL}")

    async def stop(self):
        """Stop the poller"""
        if not self.running:
            return

        logger.info("Stopping event poller...")
        self.running = False

        if self.poll_task:
            self.poll_task.cancel()
            try:
                await self.poll_task
            except asyncio.CancelledError:
                pass

        # Close client only after poller is stopped
        if self.client:
            await self.client.aclose()
            self.client = None

        logger.info("Event poller stopped")

    def is_running(self) -> bool:
        """Check if poller is running"""
        return self.running and self.poll_task is not None and not self.poll_task.done()


# Global poller instance
event_poller = EventPoller()
