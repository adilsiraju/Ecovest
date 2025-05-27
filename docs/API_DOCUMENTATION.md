# API Documentation

## Overview

The Ecovest API provides programmatic access to sustainable investment data, impact predictions, and portfolio management functionality.

## Base URL
```
Development: http://127.0.0.1:8000/api/
Production: https://api.ecovest.com/
```

## Authentication

### API Key Authentication
Include your API key in the request header:
```http
Authorization: Api-Key YOUR_API_KEY
```

### Session Authentication
For web applications, use Django's built-in session authentication.

## Endpoints

### Impact Prediction

#### Predict Environmental Impact
Calculates predicted environmental impact for an investment.

```http
POST /api/v1/predict-impact/
```

**Request Body:**
```json
{
    "investment_amount": 1000000,
    "category_names": ["Renewable Energy"],
    "project_duration_months": 12,
    "project_scale": 3,
    "location": "Karnataka",
    "technology_type": "Solar"
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "carbon_reduced": 25000.5,
        "energy_saved": 150000.0,
        "water_conserved": 50000.0,
        "impact_score": 85.2
    },
    "metadata": {
        "prediction_confidence": 0.92,
        "model_version": "v2.1.0",
        "calculated_at": "2025-05-27T10:30:00Z"
    }
}
```

**Parameters:**
- `investment_amount` (number): Investment amount in rupees
- `category_names` (array): List of sustainability categories
- `project_duration_months` (number): Project duration (1-120 months)
- `project_scale` (number): Project scale rating (1-5)
- `location` (string): Indian state or region
- `technology_type` (string): Technology used in the project

### Initiatives

#### List Initiatives
Get a list of available sustainable initiatives.

```http
GET /api/v1/initiatives/
```

**Query Parameters:**
- `category` (string): Filter by category
- `status` (string): Filter by status (active, funded, completed)
- `location` (string): Filter by location
- `page` (number): Page number for pagination
- `page_size` (number): Number of items per page (max 50)

**Response:**
```json
{
    "count": 150,
    "next": "http://api.ecovest.com/v1/initiatives/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Solar Farm Karnataka",
            "description": "Large-scale solar energy project...",
            "category": {
                "id": 1,
                "name": "Renewable Energy"
            },
            "target_amount": 5000000,
            "raised_amount": 2500000,
            "status": "active",
            "location": "Karnataka",
            "created_at": "2025-01-15T09:00:00Z",
            "expected_impact": {
                "carbon_reduced": 125000,
                "energy_generated": 750000,
                "water_conserved": 25000
            }
        }
    ]
}
```

#### Get Initiative Details
Get detailed information about a specific initiative.

```http
GET /api/v1/initiatives/{id}/
```

**Response:**
```json
{
    "id": 1,
    "title": "Solar Farm Karnataka",
    "description": "Detailed project description...",
    "category": {
        "id": 1,
        "name": "Renewable Energy",
        "description": "Clean energy projects"
    },
    "target_amount": 5000000,
    "raised_amount": 2500000,
    "investor_count": 45,
    "status": "active",
    "location": "Karnataka",
    "technology_type": "Solar",
    "project_scale": 4,
    "duration_months": 24,
    "created_at": "2025-01-15T09:00:00Z",
    "funding_deadline": "2025-12-31T23:59:59Z",
    "expected_impact": {
        "carbon_reduced": 125000,
        "energy_generated": 750000,
        "water_conserved": 25000
    },
    "risk_assessment": {
        "overall_score": 7.5,
        "factors": ["technology_maturity", "market_conditions"]
    },
    "images": [
        {
            "url": "/media/initiatives/solar-farm-1.jpg",
            "caption": "Project site overview"
        }
    ]
}
```

### Investments

#### Create Investment
Make an investment in an initiative.

```http
POST /api/v1/investments/
```

**Request Body:**
```json
{
    "initiative_id": 1,
    "amount": 50000,
    "investor_notes": "Excited to support renewable energy!"
}
```

**Response:**
```json
{
    "id": 123,
    "initiative": {
        "id": 1,
        "title": "Solar Farm Karnataka"
    },
    "amount": 50000,
    "status": "confirmed",
    "predicted_impact": {
        "carbon_reduced": 1250,
        "energy_saved": 7500,
        "water_conserved": 250
    },
    "created_at": "2025-05-27T10:30:00Z",
    "expected_return": {
        "roi_percentage": 8.5,
        "payback_period_months": 36
    }
}
```

#### Get Portfolio
Get user's investment portfolio.

```http
GET /api/v1/portfolio/
```

**Response:**
```json
{
    "total_invested": 250000,
    "total_return": 275000,
    "total_impact": {
        "carbon_reduced": 12500,
        "energy_saved": 75000,
        "water_conserved": 2500
    },
    "investments": [
        {
            "id": 123,
            "initiative_title": "Solar Farm Karnataka",
            "amount": 50000,
            "current_value": 55000,
            "status": "active",
            "roi_percentage": 10.0
        }
    ],
    "performance_metrics": {
        "monthly_return": 2.1,
        "volatility": 0.15,
        "sharpe_ratio": 1.4
    }
}
```

### Categories

#### List Categories
Get available investment categories.

```http
GET /api/v1/categories/
```

**Response:**
```json
[
    {
        "id": 1,
        "name": "Renewable Energy",
        "description": "Solar, wind, and other clean energy projects",
        "initiative_count": 25,
        "total_funded": 15000000,
        "average_roi": 8.5
    },
    {
        "id": 2,
        "name": "Water Conservation",
        "description": "Water saving and purification projects",
        "initiative_count": 12,
        "total_funded": 8000000,
        "average_roi": 7.2
    }
]
```

## Error Handling

### Error Response Format
```json
{
    "success": false,
    "error": {
        "code": "INVALID_AMOUNT",
        "message": "Investment amount must be positive",
        "details": {
            "field": "investment_amount",
            "provided_value": -1000
        }
    }
}
```

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error

### Common Error Codes
- `INVALID_API_KEY` - API key is missing or invalid
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `INSUFFICIENT_FUNDS` - User has insufficient balance
- `INVALID_AMOUNT` - Investment amount is invalid
- `INITIATIVE_CLOSED` - Initiative is no longer accepting investments
- `PREDICTION_FAILED` - Impact prediction could not be calculated

## Rate Limiting

- **Free Tier**: 100 requests per hour
- **Premium Tier**: 1000 requests per hour
- **Enterprise**: Custom limits

Rate limit headers are included in responses:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1622547600
```

## SDKs and Libraries

### Python SDK
```bash
pip install ecovest-python
```

```python
from ecovest import EcovestClient

client = EcovestClient(api_key="your_api_key")

# Predict impact
impact = client.predict_impact(
    investment_amount=100000,
    category_names=["Renewable Energy"],
    project_duration_months=12,
    project_scale=3,
    location="Karnataka",
    technology_type="Solar"
)

print(f"Carbon reduced: {impact.carbon_reduced} kg CO2")
```

### JavaScript SDK
```bash
npm install ecovest-js
```

```javascript
import { EcovestClient } from 'ecovest-js';

const client = new EcovestClient({ apiKey: 'your_api_key' });

const impact = await client.predictImpact({
    investmentAmount: 100000,
    categoryNames: ['Renewable Energy'],
    projectDurationMonths: 12,
    projectScale: 3,
    location: 'Karnataka',
    technologyType: 'Solar'
});

console.log(`Carbon reduced: ${impact.carbonReduced} kg CO2`);
```

## Webhooks

### Available Events
- `investment.created` - New investment made
- `initiative.funded` - Initiative reaches funding goal
- `portfolio.updated` - Portfolio value changes significantly

### Webhook Payload Example
```json
{
    "event": "investment.created",
    "data": {
        "investment_id": 123,
        "user_id": 456,
        "initiative_id": 1,
        "amount": 50000
    },
    "timestamp": "2025-05-27T10:30:00Z"
}
```

## Support

- **Documentation**: https://docs.ecovest.com
- **API Support**: api-support@ecovest.com
- **Status Page**: https://status.ecovest.com
