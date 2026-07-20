"""Tests for the scheduler module."""
import pytest


def test_scheduler_module_imports():
    """Test that the scheduler module can be imported."""
    from app.scheduler.scheduler import scheduler
    assert scheduler is not None


def test_scheduler_has_job_registered():
    """Test that the ingestion job is registered."""
    from app.scheduler.scheduler import scheduler
    jobs = scheduler.get_jobs()
    assert len(jobs) == 1


def test_scheduler_lifecycle():
    """Test that the scheduler can start and stop properly."""
    from app.scheduler.scheduler import scheduler
    
    scheduler.start()
    assert scheduler.running
    scheduler.shutdown()
    assert not scheduler.running


def test_scheduled_ingestion():
    """Test that the scheduled ingestion function runs without crashing."""
    from app.scheduler.scheduler import scheduled_ingestion
    scheduled_ingestion()  # Should complete without error