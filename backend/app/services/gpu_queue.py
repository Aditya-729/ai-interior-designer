"""
GPU queue controller for managing concurrent inference jobs.
"""

import asyncio
from typing import Dict, Optional, Callable, Any
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)


class GPUQueue:
    """Queue controller for GPU inference jobs."""

    def __init__(self, max_concurrent: int = 2):
        self.max_concurrent = max_concurrent
        self.active_jobs: Dict[str, dict] = {}
        self.queue: asyncio.Queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.cancelled_jobs: set = set()

    async def submit_job(
        self,
        job_id: str,
        job_data: dict,
        execute_fn: Callable[[dict], Any],
    ) -> Optional[str]:
        """
        Submit job to queue.
        
        Returns:
            Job ID if accepted, None if queue is full
        """
        if len(self.active_jobs) >= self.max_concurrent and self.queue.qsize() >= 10:
            logger.warning(f"Queue full, rejecting job {job_id}")
            return None

        job = {
            "id": job_id,
            "data": job_data,
            "execute_fn": execute_fn,
            "status": "queued",
            "created_at": datetime.utcnow(),
        }

        await self.queue.put(job)
        logger.info(f"Job {job_id} queued. Queue depth: {self.queue.qsize()}")
        
        # Start processing if not already running
        asyncio.create_task(self._process_queue())
        
        return job_id

    async def _process_queue(self):
        """Process queued jobs."""
        while not self.queue.empty():
            if len(self.active_jobs) >= self.max_concurrent:
                break

            job = await self.queue.get()
            
            if job["id"] in self.cancelled_jobs:
                self.cancelled_jobs.discard(job["id"])
                continue

            async with self.semaphore:
                self.active_jobs[job["id"]] = {
                    "status": "processing",
                    "started_at": datetime.utcnow(),
                }

                try:
                    logger.info(f"Processing job {job['id']}")
                    await job["execute_fn"](job["data"])
                    self.active_jobs[job["id"]]["status"] = "completed"
                except asyncio.CancelledError:
                    logger.info(f"Job {job['id']} cancelled")
                    self.active_jobs[job["id"]]["status"] = "cancelled"
                except Exception as e:
                    logger.error(f"Job {job['id']} failed: {e}")
                    self.active_jobs[job["id"]]["status"] = "failed"
                    self.active_jobs[job["id"]]["error"] = str(e)
                finally:
                    # Remove from active after a delay
                    await asyncio.sleep(1)
                    if job["id"] in self.active_jobs:
                        del self.active_jobs[job["id"]]

    async def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a job.
        
        Returns:
            True if job was cancelled, False if not found
        """
        if job_id in self.active_jobs:
            # Mark as cancelled
            self.active_jobs[job_id]["status"] = "cancelling"
            self.cancelled_jobs.add(job_id)
            logger.info(f"Job {job_id} marked for cancellation")
            return True
        
        # Check if in queue
        # Note: This is a simplified implementation
        # In production, you'd need to track queue items better
        self.cancelled_jobs.add(job_id)
        return True

    def get_queue_status(self) -> dict:
        """Get current queue status for health checks."""
        return {
            "status": "operational",
            "queue_depth": self.queue.qsize(),
            "active_jobs": len(self.active_jobs),
            "max_concurrent": self.max_concurrent,
            "max_queue_depth": 10,  # From config
        }

    def get_job_status(self, job_id: str) -> Optional[dict]:
        """Get status of a specific job."""
        if job_id in self.active_jobs:
            return self.active_jobs[job_id]
        return None


# Global queue instance (will be initialized with config)
gpu_queue: Optional[GPUQueue] = None

def init_gpu_queue(max_concurrent: int = 2):
    """Initialize GPU queue with config."""
    global gpu_queue
    gpu_queue = GPUQueue(max_concurrent=max_concurrent)
    return gpu_queue
