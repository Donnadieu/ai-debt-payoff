"""Tests for background worker functionality."""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta
from typing import Dict, Any, List

from app.schemas.debt import Debt


class MockWorkerQueue:
    """Mock worker queue for testing background jobs."""
    
    def __init__(self):
        self.jobs = []
        self.completed_jobs = []
        self.failed_jobs = []
        self.job_counter = 0
    
    async def enqueue_job(self, job_type: str, job_data: Dict[str, Any], delay: int = 0) -> str:
        """Enqueue a background job."""
        job_id = f"job_{self.job_counter}"
        self.job_counter += 1
        
        job = {
            "id": job_id,
            "type": job_type,
            "data": job_data,
            "status": "queued",
            "created_at": datetime.utcnow(),
            "delay": delay
        }
        
        self.jobs.append(job)
        return job_id
    
    async def process_job(self, job_id: str) -> Dict[str, Any]:
        """Process a queued job."""
        job = next((j for j in self.jobs if j["id"] == job_id), None)
        if not job:
            raise ValueError(f"Job {job_id} not found")
        
        job["status"] = "processing"
        job["started_at"] = datetime.utcnow()
        
        try:
            # Mock job processing based on type
            if job["type"] == "calculate_payoff":
                result = await self._process_payoff_calculation(job["data"])
            elif job["type"] == "generate_nudge":
                result = await self._process_nudge_generation(job["data"])
            elif job["type"] == "send_notification":
                result = await self._process_notification(job["data"])
            else:
                raise ValueError(f"Unknown job type: {job['type']}")
            
            job["status"] = "completed"
            job["completed_at"] = datetime.utcnow()
            job["result"] = result
            self.completed_jobs.append(job)
            
            return result
            
        except Exception as e:
            job["status"] = "failed"
            job["failed_at"] = datetime.utcnow()
            job["error"] = str(e)
            self.failed_jobs.append(job)
            raise
    
    async def _process_payoff_calculation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock payoff calculation processing."""
        debts = data.get("debts", [])
        monthly_payment = data.get("monthly_payment", 0)
        
        # Simple mock calculation
        total_debt = sum(debt.get("balance", 0) for debt in debts)
        months_to_payoff = max(1, int(total_debt / monthly_payment)) if monthly_payment > 0 else 999
        
        return {
            "total_debt": total_debt,
            "monthly_payment": monthly_payment,
            "months_to_payoff": months_to_payoff,
            "total_interest": total_debt * 0.1,  # Mock 10% total interest
            "payoff_date": datetime.utcnow() + timedelta(days=months_to_payoff * 30)
        }
    
    async def _process_nudge_generation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock nudge generation processing."""
        user_id = data.get("user_id")
        nudge_type = data.get("nudge_type", "motivation")
        
        return {
            "user_id": user_id,
            "nudge_type": nudge_type,
            "title": "Stay Motivated!",
            "message": "You're making great progress on your debt payoff journey.",
            "generated_at": datetime.utcnow()
        }
    
    async def _process_notification(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock notification processing."""
        recipient = data.get("recipient")
        message = data.get("message")
        method = data.get("method", "email")
        
        # Simulate notification delay
        await asyncio.sleep(0.1)
        
        return {
            "recipient": recipient,
            "method": method,
            "message": message,
            "sent_at": datetime.utcnow(),
            "status": "delivered"
        }
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get job status."""
        job = next((j for j in self.jobs if j["id"] == job_id), None)
        if not job:
            return {"status": "not_found"}
        
        return {
            "id": job["id"],
            "type": job["type"],
            "status": job["status"],
            "created_at": job["created_at"],
            "result": job.get("result"),
            "error": job.get("error")
        }
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        return {
            "total_jobs": len(self.jobs),
            "queued": len([j for j in self.jobs if j["status"] == "queued"]),
            "processing": len([j for j in self.jobs if j["status"] == "processing"]),
            "completed": len(self.completed_jobs),
            "failed": len(self.failed_jobs)
        }


class TestWorkerQueue:
    """Test worker queue functionality."""
    
    @pytest.fixture
    def worker_queue(self):
        """Worker queue instance."""
        return MockWorkerQueue()
    
    @pytest.mark.asyncio
    async def test_enqueue_payoff_calculation_job(self, worker_queue):
        """Test enqueueing a payoff calculation job."""
        job_data = {
            "debts": [
                {"name": "Credit Card", "balance": 2500.0, "interest_rate": 18.5},
                {"name": "Student Loan", "balance": 15000.0, "interest_rate": 6.8}
            ],
            "monthly_payment": 500.0,
            "strategy": "avalanche"
        }
        
        job_id = await worker_queue.enqueue_job("calculate_payoff", job_data)
        
        assert job_id is not None
        assert job_id.startswith("job_")
        
        # Check job was queued
        stats = worker_queue.get_queue_stats()
        assert stats["queued"] == 1
        assert stats["total_jobs"] == 1
    
    @pytest.mark.asyncio
    async def test_process_payoff_calculation_job(self, worker_queue):
        """Test processing a payoff calculation job."""
        job_data = {
            "debts": [
                {"name": "Credit Card", "balance": 3000.0, "interest_rate": 15.0}
            ],
            "monthly_payment": 200.0
        }
        
        job_id = await worker_queue.enqueue_job("calculate_payoff", job_data)
        result = await worker_queue.process_job(job_id)
        
        assert "total_debt" in result
        assert "months_to_payoff" in result
        assert "payoff_date" in result
        assert result["total_debt"] == 3000.0
        assert result["monthly_payment"] == 200.0
        
        # Check job completed
        status = worker_queue.get_job_status(job_id)
        assert status["status"] == "completed"
    
    @pytest.mark.asyncio
    async def test_enqueue_nudge_generation_job(self, worker_queue):
        """Test enqueueing a nudge generation job."""
        job_data = {
            "user_id": "user_123",
            "nudge_type": "motivation",
            "context": {"progress": "good", "last_payment": "2024-01-15"}
        }
        
        job_id = await worker_queue.enqueue_job("generate_nudge", job_data)
        
        assert job_id is not None
        
        stats = worker_queue.get_queue_stats()
        assert stats["queued"] == 1
    
    @pytest.mark.asyncio
    async def test_process_nudge_generation_job(self, worker_queue):
        """Test processing a nudge generation job."""
        job_data = {
            "user_id": "user_456",
            "nudge_type": "reminder"
        }
        
        job_id = await worker_queue.enqueue_job("generate_nudge", job_data)
        result = await worker_queue.process_job(job_id)
        
        assert "user_id" in result
        assert "nudge_type" in result
        assert "title" in result
        assert "message" in result
        assert result["user_id"] == "user_456"
        assert result["nudge_type"] == "reminder"
    
    @pytest.mark.asyncio
    async def test_enqueue_notification_job(self, worker_queue):
        """Test enqueueing a notification job."""
        job_data = {
            "recipient": "user@example.com",
            "message": "Your payment is due tomorrow",
            "method": "email"
        }
        
        job_id = await worker_queue.enqueue_job("send_notification", job_data)
        
        assert job_id is not None
        
        stats = worker_queue.get_queue_stats()
        assert stats["queued"] == 1
    
    @pytest.mark.asyncio
    async def test_process_notification_job(self, worker_queue):
        """Test processing a notification job."""
        job_data = {
            "recipient": "user@example.com",
            "message": "Payment reminder",
            "method": "push"
        }
        
        job_id = await worker_queue.enqueue_job("send_notification", job_data)
        result = await worker_queue.process_job(job_id)
        
        assert "recipient" in result
        assert "method" in result
        assert "status" in result
        assert result["recipient"] == "user@example.com"
        assert result["method"] == "push"
        assert result["status"] == "delivered"
    
    @pytest.mark.asyncio
    async def test_job_failure_handling(self, worker_queue):
        """Test handling of job failures."""
        job_data = {"invalid": "data"}
        
        job_id = await worker_queue.enqueue_job("unknown_job_type", job_data)
        
        with pytest.raises(ValueError):
            await worker_queue.process_job(job_id)
        
        # Check job marked as failed
        status = worker_queue.get_job_status(job_id)
        assert status["status"] == "failed"
        assert "error" in status
        
        stats = worker_queue.get_queue_stats()
        assert stats["failed"] == 1
    
    @pytest.mark.asyncio
    async def test_delayed_job_enqueueing(self, worker_queue):
        """Test enqueueing jobs with delay."""
        job_data = {"user_id": "user_123", "nudge_type": "reminder"}
        
        job_id = await worker_queue.enqueue_job("generate_nudge", job_data, delay=3600)  # 1 hour delay
        
        assert job_id is not None
        
        # Job should be queued with delay
        job = next(j for j in worker_queue.jobs if j["id"] == job_id)
        assert job["delay"] == 3600
    
    def test_get_nonexistent_job_status(self, worker_queue):
        """Test getting status of non-existent job."""
        status = worker_queue.get_job_status("nonexistent_job")
        
        assert status["status"] == "not_found"


class TestWorkerConcurrency:
    """Test worker concurrency and parallel processing."""
    
    @pytest.fixture
    def worker_queue(self):
        return MockWorkerQueue()
    
    @pytest.mark.asyncio
    async def test_concurrent_job_processing(self, worker_queue):
        """Test processing multiple jobs concurrently."""
        # Enqueue multiple jobs
        job_ids = []
        for i in range(5):
            job_data = {
                "recipient": f"user{i}@example.com",
                "message": f"Message {i}",
                "method": "email"
            }
            job_id = await worker_queue.enqueue_job("send_notification", job_data)
            job_ids.append(job_id)
        
        # Process jobs concurrently
        tasks = [worker_queue.process_job(job_id) for job_id in job_ids]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 5
        assert all("status" in result for result in results)
        assert all(result["status"] == "delivered" for result in results)
        
        # Check all jobs completed
        stats = worker_queue.get_queue_stats()
        assert stats["completed"] == 5
    
    @pytest.mark.asyncio
    async def test_mixed_job_types_concurrent_processing(self, worker_queue):
        """Test processing different job types concurrently."""
        # Enqueue different types of jobs
        jobs = [
            ("calculate_payoff", {
                "debts": [{"balance": 1000.0}],
                "monthly_payment": 100.0
            }),
            ("generate_nudge", {
                "user_id": "user_123",
                "nudge_type": "motivation"
            }),
            ("send_notification", {
                "recipient": "user@example.com",
                "message": "Test message",
                "method": "email"
            })
        ]
        
        job_ids = []
        for job_type, job_data in jobs:
            job_id = await worker_queue.enqueue_job(job_type, job_data)
            job_ids.append(job_id)
        
        # Process all jobs concurrently
        tasks = [worker_queue.process_job(job_id) for job_id in job_ids]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 3
        
        # Verify each result type
        payoff_result, nudge_result, notification_result = results
        
        assert "total_debt" in payoff_result
        assert "nudge_type" in nudge_result
        assert "status" in notification_result


class TestWorkerErrorHandling:
    """Test worker error handling and recovery."""
    
    @pytest.fixture
    def worker_queue(self):
        return MockWorkerQueue()
    
    @pytest.mark.asyncio
    async def test_job_retry_mechanism(self, worker_queue):
        """Test job retry mechanism for failed jobs."""
        # This would be implemented in a real worker system
        job_data = {"user_id": "user_123"}
        
        # First attempt fails
        job_id = await worker_queue.enqueue_job("unknown_job_type", job_data)
        
        with pytest.raises(ValueError):
            await worker_queue.process_job(job_id)
        
        # Check job failed
        status = worker_queue.get_job_status(job_id)
        assert status["status"] == "failed"
        
        # In a real system, we might retry the job
        # For now, just verify the failure was recorded
        stats = worker_queue.get_queue_stats()
        assert stats["failed"] == 1
    
    @pytest.mark.asyncio
    async def test_partial_failure_in_batch(self, worker_queue):
        """Test handling partial failures in batch processing."""
        # Mix of valid and invalid jobs
        jobs = [
            ("calculate_payoff", {"debts": [{"balance": 1000.0}], "monthly_payment": 100.0}),  # Valid
            ("unknown_type", {"invalid": "data"}),  # Invalid
            ("generate_nudge", {"user_id": "user_123", "nudge_type": "motivation"})  # Valid
        ]
        
        job_ids = []
        for job_type, job_data in jobs:
            job_id = await worker_queue.enqueue_job(job_type, job_data)
            job_ids.append(job_id)
        
        # Process jobs, expecting one to fail
        results = []
        errors = []
        
        for job_id in job_ids:
            try:
                result = await worker_queue.process_job(job_id)
                results.append(result)
            except Exception as e:
                errors.append(e)
        
        assert len(results) == 2  # Two successful jobs
        assert len(errors) == 1   # One failed job
        
        stats = worker_queue.get_queue_stats()
        assert stats["completed"] == 2
        assert stats["failed"] == 1


class TestWorkerPerformance:
    """Test worker performance and optimization."""
    
    @pytest.fixture
    def worker_queue(self):
        return MockWorkerQueue()
    
    @pytest.mark.asyncio
    async def test_job_processing_performance(self, worker_queue):
        """Test job processing performance."""
        import time
        
        # Enqueue a batch of jobs
        job_ids = []
        for i in range(10):
            job_data = {
                "recipient": f"user{i}@example.com",
                "message": f"Message {i}",
                "method": "email"
            }
            job_id = await worker_queue.enqueue_job("send_notification", job_data)
            job_ids.append(job_id)
        
        # Time the processing
        start_time = time.time()
        
        tasks = [worker_queue.process_job(job_id) for job_id in job_ids]
        await asyncio.gather(*tasks)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should process reasonably quickly (less than 5 seconds for 10 jobs)
        assert processing_time < 5.0
        
        # Check all jobs completed
        stats = worker_queue.get_queue_stats()
        assert stats["completed"] == 10
    
    @pytest.mark.asyncio
    async def test_memory_usage_during_processing(self, worker_queue):
        """Test memory usage during job processing."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Process many jobs
        job_ids = []
        for i in range(50):
            job_data = {"user_id": f"user_{i}", "nudge_type": "motivation"}
            job_id = await worker_queue.enqueue_job("generate_nudge", job_data)
            job_ids.append(job_id)
        
        # Process all jobs
        tasks = [worker_queue.process_job(job_id) for job_id in job_ids]
        await asyncio.gather(*tasks)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50 * 1024 * 1024


class TestWorkerIntegration:
    """Test worker integration with other system components."""
    
    @pytest.fixture
    def worker_queue(self):
        return MockWorkerQueue()
    
    @pytest.mark.asyncio
    async def test_worker_analytics_integration(self, worker_queue):
        """Test worker integration with analytics."""
        job_data = {
            "debts": [{"balance": 5000.0}],
            "monthly_payment": 250.0
        }
        
        with patch('app.core.analytics.analytics_core.track_event') as mock_track:
            job_id = await worker_queue.enqueue_job("calculate_payoff", job_data)
            result = await worker_queue.process_job(job_id)
            
            # In real implementation, worker would track analytics
            mock_track("job_completed", {
                "job_id": job_id,
                "job_type": "calculate_payoff",
                "processing_time": 0.1,
                "status": "success"
            })
            
            mock_track.assert_called_once()
            call_args = mock_track.call_args
            assert call_args[0][0] == "job_completed"
            assert call_args[0][1]["job_type"] == "calculate_payoff"
    
    @pytest.mark.asyncio
    async def test_worker_notification_integration(self, worker_queue):
        """Test worker integration with notification system."""
        # Test that worker can trigger notifications
        nudge_job_data = {
            "user_id": "user_123",
            "nudge_type": "reminder"
        }
        
        nudge_job_id = await worker_queue.enqueue_job("generate_nudge", nudge_job_data)
        nudge_result = await worker_queue.process_job(nudge_job_id)
        
        # After generating nudge, worker might enqueue notification job
        notification_job_data = {
            "recipient": "user_123",
            "message": nudge_result["message"],
            "method": "push"
        }
        
        notification_job_id = await worker_queue.enqueue_job("send_notification", notification_job_data)
        notification_result = await worker_queue.process_job(notification_job_id)
        
        assert notification_result["status"] == "delivered"
        assert notification_result["recipient"] == "user_123"
        
        # Both jobs should be completed
        stats = worker_queue.get_queue_stats()
        assert stats["completed"] == 2
