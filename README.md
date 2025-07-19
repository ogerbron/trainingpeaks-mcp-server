# TrainingPeaks MCP Server

An MCP (Model Context Protocol) server that enables Claude to interact with the TrainingPeaks API for retrieving athlete data, workouts, metrics, and calendar events.

## Features

- **Athlete Profile**: Get basic profile information and training zones
- **Workouts**: Retrieve workout history and detailed workout information
- **Calendar Events**: Access TrainingPeaks calendar events
- **Metrics**: Get health and fitness metrics (weight, HRV, steps, stress, sleep)
- **Planned Workouts**: Retrieve upcoming planned workouts (up to 7 days)
- **OAuth 2.0 Authentication**: Secure authentication with TrainingPeaks API

## Prerequisites

- Python 3.8+
- TrainingPeaks API credentials (client_id, client_secret)
- API access approval from TrainingPeaks (required for production use)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd trainingpeaks-mcp-server
```

2. Install dependencies:
```bash
pip install -e .
```

3. Copy environment configuration:
```bash
cp .env.example .env
```

4. Edit `.env` with your TrainingPeaks API credentials:
```env
TRAININGPEAKS_CLIENT_ID=your_client_id_here
TRAININGPEAKS_CLIENT_SECRET=your_client_secret_here
TRAININGPEAKS_REDIRECT_URI=http://localhost:8080/callback
TRAININGPEAKS_SCOPES=athlete:profile,athlete:workouts
TRAININGPEAKS_ENVIRONMENT=sandbox
```

## Usage

### Running the MCP Server

```bash
trainingpeaks-mcp-server
```

Or alternatively:
```bash
python -m trainingpeaks_mcp_server.server
```

To test that the server works:
```bash
python test_server.py
```

### Available Tools

1. **get_athlete_profile**: Get athlete's profile and training zones
2. **get_workouts**: Retrieve workouts with optional date filtering
3. **get_workout_details**: Get detailed information about a specific workout
4. **get_calendar_events**: Access calendar events within a date range
5. **get_metrics**: Get health metrics (weight, HRV, steps, stress, sleep)
6. **get_planned_workouts**: Retrieve upcoming planned workouts
7. **set_auth_tokens**: Set OAuth tokens for API authentication

### Authentication

Before using the API tools, you need to authenticate:

1. Use TrainingPeaks OAuth flow to obtain access and refresh tokens
2. Use the `set_auth_tokens` tool to provide tokens to the MCP server
3. The server will automatically handle token refresh when needed

## API Access

**Important**: TrainingPeaks API access is currently limited to approved commercial applications. To request access:

1. Visit https://api.trainingpeaks.com/request-access
2. Provide information about your application and use case
3. Allow 7-10 days for response

For development/testing, use the sandbox environment.

## Configuration

The server supports both production and sandbox environments:

- **Sandbox**: `TRAININGPEAKS_ENVIRONMENT=sandbox`
- **Production**: `TRAININGPEAKS_ENVIRONMENT=production`

## Development

Install development dependencies:
```bash
pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```

Format code:
```bash
black src/
ruff check src/
```

## License

MIT License - see LICENSE file for details.
