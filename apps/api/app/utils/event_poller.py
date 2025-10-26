"""
Event Poller - Polls for calendar events and detects changes
"""

import asyncio
import json
import logging
import os
import random
import subprocess
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx

logger = logging.getLogger("event_poller")
logging.basicConfig(level=logging.INFO)

# Configuration
POLL_INTERVAL_SEC = 5  # Poll every 5 seconds
MAX_JITTER_SEC = 1  # Random jitter to avoid collisions
BACKOFF_BASE = 2  # Backoff multiplier for errors
POLL_ENABLED = os.getenv("ENABLE_EVENT_POLLER", "1") == "1"
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
SUGGESTION_FILE = Path(__file__).with_name("event_suggestions.json")


class EventPoller:
    """Event poller that monitors calendar events for changes"""

    def __init__(self):
        self.running = False
        self.poll_task = None
        self.client = None
        self.prev_events = {}  # Previous snapshot: {id: event}
        self.lock = asyncio.Lock()
        self.backoff = 0
        


    async def get_today_events(self) -> list[dict]:
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

    def diff_events(self, prev: dict[str, dict], curr_list: list[dict]) -> tuple:
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

    def log_changes(self, added: list[dict], updated: list[dict], removed: list[dict]):
        """Log detected changes with detailed object information"""
        if added:
            logger.info(f"ADDED {len(added)} events:")
            for event in added:
                logger.info(
                    f"  + {event.get('title', 'Untitled')} (ID: {event.get('id')})"
                )
                logger.info(
                    f"    Start: {event.get('when', {}).get('start_time', 'N/A')}"
                )
                logger.info(f"    End: {event.get('when', {}).get('end_time', 'N/A')}")
                logger.info(f"    Location: {event.get('location', 'N/A')}")
                logger.info(f"    Description: {event.get('description', 'N/A')}")
                logger.info(f"    Participants: {len(event.get('participants', []))}")
                logger.info(f"    Updated: {event.get('updated_at', 'N/A')}")
                logger.info("    " + "=" * 50)

        if updated:
            logger.info(f"UPDATED {len(updated)} events:")
            for event in updated:
                event_id = event.get("id")
                old_event = self.prev_events.get(event_id, {})

                logger.info(f"  ~ {event.get('title', 'Untitled')} (ID: {event_id})")

                self._log_field_changes(
                    "Title", old_event.get("title"), event.get("title")
                )
                self._log_field_changes(
                    "Description",
                    old_event.get("description"),
                    event.get("description"),
                )
                self._log_field_changes(
                    "Location", old_event.get("location"), event.get("location")
                )
                self._log_field_changes(
                    "Start Time",
                    old_event.get("when", {}).get("start_time"),
                    event.get("when", {}).get("start_time"),
                )
                self._log_field_changes(
                    "End Time",
                    old_event.get("when", {}).get("end_time"),
                    event.get("when", {}).get("end_time"),
                )
                self._log_field_changes(
                    "Updated At", old_event.get("updated_at"), event.get("updated_at")
                )

                # Log participants changes
                old_participants = old_event.get("participants", [])
                new_participants = event.get("participants", [])
                if old_participants != new_participants:
                    logger.info("    Participants changed:")
                    logger.info(
                        f"      OLD: {[p.get('email') for p in old_participants]}"
                    )
                    logger.info(
                        f"      NEW: {[p.get('email') for p in new_participants]}"
                    )

                logger.info("    " + "=" * 50)

        if removed:
            logger.info(f"REMOVED {len(removed)} events:")
            for event in removed:
                logger.info(
                    f"  - {event.get('title', 'Untitled')} (ID: {event.get('id')})"
                )
                logger.info(
                    f"    Was scheduled: {event.get('when', {}).get('start_time', 'N/A')}"
                )
                logger.info(f"    Location: {event.get('location', 'N/A')}")
                logger.info(
                    f"    Had {len(event.get('participants', []))} participants"
                )
                logger.info("    " + "=" * 50)

    def _log_field_changes(self, field_name: str, old_value, new_value):
        """Log individual field changes"""
        if old_value != new_value:
            logger.info(f"    {field_name}:")
            logger.info(f"      OLD: {old_value}")
            logger.info(f"      NEW: {new_value}")

    def log_full_objects(
        self, added: list[dict], updated: list[dict], removed: list[dict]
    ):
        """Log complete objects for debugging"""
        if added:
            logger.info("FULL OBJECTS - ADDED EVENTS:")
            for i, event in enumerate(added, 1):
                logger.info(f"  Event {i}:")
                logger.info(f"    {event}")
                logger.info("    " + "-" * 30)

        if updated:
            logger.info("FULL OBJECTS - UPDATED EVENTS:")
            for i, event in enumerate(updated, 1):
                event_id = event.get("id")
                old_event = self.prev_events.get(event_id, {})
                logger.info(f"  Event {i} (ID: {event_id}):")
                logger.info(f"    OLD OBJECT: {old_event}")
                logger.info(f"    NEW OBJECT: {event}")
                logger.info("    " + "-" * 30)

        if removed:
            logger.info("FULL OBJECTS - REMOVED EVENTS:")
            for i, event in enumerate(removed, 1):
                logger.info(f"  Event {i}:")
                logger.info(f"    {event}")
                logger.info("    " + "-" * 30)

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

                await self.handle_event_changes(added, updated, removed)
            else:
                logger.debug("No event changes detected")

            # Reset backoff on success
            self.backoff = 0

            # Update snapshot after handling changes so previous data remains available
            self.prev_events = snapshot

        except Exception as e:
            logger.warning(f"Poll failed: {e}")
            self.backoff = min(4, self.backoff + 1)  # Max 4 backoff steps

    async def handle_event_changes(
        self, added: list[dict], updated: list[dict], removed: list[dict]
    ):
        """Handle detected event changes - override this for custom logic"""
        if not self.prev_events and added and not updated and not removed:
            logger.debug("Initial event snapshot captured; skipping AI suggestions")
            return

        descriptions = self._build_change_descriptions(added, updated, removed)
        if not descriptions:
            return

        try:
            from app.dependencies.auth import get_current_user
            from app.dependencies.langchain import ai_event_changed_suggestions
        except Exception as exc:  # pragma: no cover - import errors logged
            logger.error("Unable to import dependencies for AI suggestions: %s", exc)
            return

        user_id = get_current_user()

        try:
            suggestion = await asyncio.to_thread(
                ai_event_changed_suggestions, user_id, descriptions
            )
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("AI suggestion generation failed: %s", exc)
            return

        payload = self._prepare_suggestion_payload(user_id, descriptions, suggestion)

        try:
            await asyncio.to_thread(self._persist_suggestion, payload)
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("Failed to persist suggestion payload: %s", exc)

    def _prepare_suggestion_payload(
        self, user_id: str, descriptions: list[str], suggestion: Any
    ) -> dict[str, Any]:
        """Prepare structured payload for suggestion persistence"""
        if is_dataclass(suggestion):
            suggestion_content: Any = asdict(suggestion)
        elif isinstance(suggestion, dict):
            suggestion_content = suggestion
        else:
            suggestion_content = str(suggestion)

        return {
            "user_id": user_id,
            "generated_at": datetime.utcnow().isoformat(),
            "changes": descriptions,
            "suggestion": suggestion_content,
        }

    def _persist_suggestion(self, payload: dict[str, Any]) -> None:
        """Persist suggestion payload to disk"""
        SUGGESTION_FILE.parent.mkdir(parents=True, exist_ok=True)
        SUGGESTION_FILE.write_text(
            json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8"
        )

        logger.info("Updated event suggestions at %s", SUGGESTION_FILE)
        self._broadcast_suggestion(payload)

    def _build_change_descriptions(
        self, added: list[dict], updated: list[dict], removed: list[dict]
    ) -> list[str]:
        """Build human-readable descriptions for changed events"""
        descriptions: list[str] = []
        for event in added:
            descriptions.append(self._describe_added_event(event))

        for event in updated:
            event_id = event.get("id")
            prev_event = self.prev_events.get(event_id, {}) if event_id else {}
            descriptions.append(self._describe_updated_event(event, prev_event))

        for event in removed:
            descriptions.append(self._describe_removed_event(event))

        return [desc for desc in descriptions if desc]

    def _describe_added_event(self, event: dict) -> str:
        title = event.get("title", "Untitled")
        event_id = event.get("id", "unknown")
        start, end = self._extract_event_times(event)
        location = event.get("location") or "Unspecified location"
        return (
            f"Added event '{title}' (ID: {event_id}) scheduled from {start} to {end}"
            f" at {location}."
        )

    def _describe_updated_event(self, event: dict, prev_event: dict) -> str:
        event_id = event.get("id", "unknown")
        title = event.get("title", "Untitled")

        old_start, old_end = self._extract_event_times(prev_event)
        new_start, new_end = self._extract_event_times(event)

        old_location = prev_event.get("location") or "Unspecified location"
        new_location = event.get("location") or "Unspecified location"

        changes: list[str] = []
        if old_start != new_start:
            changes.append(f"start {old_start} -> {new_start}")
        if old_end != new_end:
            changes.append(f"end {old_end} -> {new_end}")
        if old_location != new_location:
            changes.append(f"location '{old_location}' -> '{new_location}'")

        if not changes:
            changes.append("details were updated without time or location changes")

        return f"Updated event '{title}' (ID: {event_id}); " + ", ".join(changes) + "."

    def _describe_removed_event(self, event: dict) -> str:
        title = event.get("title", "Untitled")
        event_id = event.get("id", "unknown")
        start, end = self._extract_event_times(event)
        return (
            f"Removed event '{title}' (ID: {event_id}) that was scheduled from"
            f" {start} to {end}."
        )

    def _extract_event_times(self, event: dict) -> tuple:
        when = event.get("when") or {}
        start = when.get("start_time")
        end = when.get("end_time")
        return self._format_timestamp(start), self._format_timestamp(end)

    def _format_timestamp(self, raw_value: Any) -> str:
        if raw_value in (None, ""):
            return "unspecified time"

        if isinstance(raw_value, (int, float)):
            try:
                return datetime.fromtimestamp(raw_value).isoformat()
            except Exception:  # pragma: no cover - fallback formatting
                return str(raw_value)

        return str(raw_value)

    def _broadcast_suggestion(self, payload: dict[str, Any]) -> None:
        """Notify Supabase realtime service about updated suggestions"""
        token = (
            os.getenv("SUPABASE_KEY")
        )
        url = os.getenv("SUPABASE_URL")

        if not token or not url:
            logger.warning("Supabase credentials missing; skipping realtime broadcast")
            return

        broadcast_url = url.rstrip("/") + "/realtime/v1/api/broadcast"
        topic = os.getenv("SUPABASE_BROADCAST_TOPIC", "event-changes")
        event_name = os.getenv("SUPABASE_BROADCAST_EVENT", "shout")

        message = {
            "messages": [
                {
                    "topic": topic,
                    "event": event_name,
                    "payload": payload,
                }
            ]
        }

        curl_cmd = [
            "curl",
            "-v",
            "-H",
            f"apikey: {token}",
            "-H",
            "Content-Type: application/json",
            "--data-raw",
            json.dumps(message),
            broadcast_url,
        ]

        try:
            result = subprocess.run(
                curl_cmd,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").replace(token, "***")
            logger.error("Supabase broadcast failed: %s", stderr or exc)
        else:
            if result.returncode == 0:
                logger.info("Supabase broadcast succeeded")

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
