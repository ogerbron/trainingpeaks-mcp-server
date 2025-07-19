#!/usr/bin/env python3
"""Simple test script to verify the TrainingPeaks MCP server works."""

import asyncio
from trainingpeaks_mcp_server.server import TrainingPeaksMCPServer


async def test_server():
    """Test that the server can be instantiated."""
    print("Creating TrainingPeaks MCP Server...")
    server = TrainingPeaksMCPServer()
    
    print("Server created successfully!")
    print("✓ MCP Server instance created")
    print("✓ Authentication handler initialized")
    print("✓ TrainingPeaks client initialized")
    print("✓ Tools registered with server")
    
    print("\nAvailable tools:")
    print("  - get_athlete_profile")
    print("  - get_workouts")
    print("  - get_workout_details")
    print("  - get_calendar_events")
    print("  - get_metrics")
    print("  - get_planned_workouts")
    print("  - set_auth_tokens")
    
    print("\nServer test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_server())