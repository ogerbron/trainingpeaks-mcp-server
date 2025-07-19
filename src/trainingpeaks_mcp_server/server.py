"""TrainingPeaks MCP Server implementation."""

import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    InitializeResult,
    Tool,
    TextContent,
    Implementation,
)
from mcp.server.lowlevel import NotificationOptions
from .auth import TrainingPeaksAuth
from .client import TrainingPeaksClient


class TrainingPeaksMCPServer:
    """MCP Server for TrainingPeaks API integration."""
    
    def __init__(self):
        self.server = Server("trainingpeaks-mcp-server")
        self.auth = TrainingPeaksAuth()
        self.client = TrainingPeaksClient(self.auth)
        self._setup_tools()
    
    def _setup_tools(self):
        """Setup MCP tools for TrainingPeaks API."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available TrainingPeaks tools."""
            return [
                Tool(
                    name="get_athlete_profile",
                    description="Get the authenticated athlete's profile information including basic details and training zones",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_workouts",
                    description="Get athlete's workouts within a specified date range",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_date": {
                                "type": "string",
                                "description": "Start date in YYYY-MM-DD format (optional)"
                            },
                            "end_date": {
                                "type": "string", 
                                "description": "End date in YYYY-MM-DD format (optional)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of workouts to return (default: 50)",
                                "default": 50
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="get_workout_details",
                    description="Get detailed information about a specific workout",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "workout_id": {
                                "type": "string",
                                "description": "The unique identifier of the workout"
                            }
                        },
                        "required": ["workout_id"]
                    }
                ),
                Tool(
                    name="get_calendar_events",
                    description="Get calendar events from athlete's TrainingPeaks calendar",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_date": {
                                "type": "string",
                                "description": "Start date in YYYY-MM-DD format (optional)"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date in YYYY-MM-DD format (optional)"
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="get_metrics",
                    description="Get metrics data such as weight, HRV, steps, stress, and sleep quality",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "metric_type": {
                                "type": "string",
                                "description": "Type of metric (weight, hrv, steps, stress, sleep)",
                                "enum": ["weight", "hrv", "steps", "stress", "sleep"]
                            },
                            "start_date": {
                                "type": "string",
                                "description": "Start date in YYYY-MM-DD format (optional)"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date in YYYY-MM-DD format (optional)"
                            }
                        },
                        "required": ["metric_type"]
                    }
                ),
                Tool(
                    name="get_planned_workouts",
                    description="Get planned workouts for the athlete up to 7 days in the future",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "days_ahead": {
                                "type": "integer",
                                "description": "Number of days ahead to retrieve (max: 7, default: 7)",
                                "default": 7,
                                "maximum": 7
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="set_auth_tokens",
                    description="Set authentication tokens for TrainingPeaks API access",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "access_token": {
                                "type": "string",
                                "description": "OAuth access token"
                            },
                            "refresh_token": {
                                "type": "string",
                                "description": "OAuth refresh token"
                            },
                            "expires_in": {
                                "type": "integer",
                                "description": "Token expiration time in seconds"
                            }
                        },
                        "required": ["access_token", "refresh_token", "expires_in"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Execute TrainingPeaks tool calls."""
            try:
                if name == "get_athlete_profile":
                    result = await self.client.get_athlete_profile()

                elif name == "get_workouts":
                    result = await self.client.get_workouts(
                        start_date=arguments.get("start_date"),
                        end_date=arguments.get("end_date"),
                        limit=arguments.get("limit", 50)
                    )
                    
                elif name == "get_workout_details":
                    result = await self.client.get_workout_details(
                        workout_id=arguments["workout_id"]
                    )
                    
                elif name == "get_calendar_events":
                    result = await self.client.get_calendar_events(
                        start_date=arguments.get("start_date"),
                        end_date=arguments.get("end_date")
                    )
                    
                elif name == "get_metrics":
                    result = await self.client.get_metrics(
                        metric_type=arguments["metric_type"],
                        start_date=arguments.get("start_date"),
                        end_date=arguments.get("end_date")
                    )
                    
                elif name == "get_planned_workouts":
                    result = await self.client.get_planned_workouts(
                        days_ahead=arguments.get("days_ahead", 7)
                    )
                    
                elif name == "set_auth_tokens":
                    self.auth.set_tokens(
                        access_token=arguments["access_token"],
                        refresh_token=arguments["refresh_token"],
                        expires_in=arguments["expires_in"]
                    )
                    result = {"status": "success", "message": "Tokens set successfully"}
                    
                else:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Unknown tool: {name}")]
                    )
                
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(result, indent=2))]
                )
                
            except Exception as e:
                error_msg = f"Error calling {name}: {str(e)}"
                return CallToolResult(
                    content=[TextContent(type="text", text=error_msg)],
                    isError=True
                )


async def amain():
    """Async main entry point for the TrainingPeaks MCP server."""
    mcp_server = TrainingPeaksMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.server.run(
            read_stream,
            write_stream,
            InitializeResult(
                protocolVersion="2024-11-05",
                serverInfo=Implementation(
                    name="trainingpeaks-mcp-server",
                    version="0.1.0"
                ),
                capabilities=mcp_server.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities=None
                )
            )
        )


def main():
    """Main entry point for the TrainingPeaks MCP server."""
    asyncio.run(amain())


if __name__ == "__main__":
    main()