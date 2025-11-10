# YSenseAI™ Backend Deployment Guide

## Quick Start

### Local Development

```bash
# Install dependencies
pip3 install -r requirements.txt

# Set environment variable
export OPENAI_API_KEY="your-api-key"

# Run example
python3 perception_toolkit.py

# Create founder's wisdom drops
python3 create_founder_wisdom_drops.py

# Start API server
python3 api_server.py
```

The API server will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/api/docs`

### Production Deployment (Google Cloud Run)

```bash
# Create Dockerfile
cat > Dockerfile << 'DOCKER'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]
DOCKER

# Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT/ysense-backend
gcloud run deploy ysense-backend \
  --image gcr.io/YOUR_PROJECT/ysense-backend \
  --platform managed \
  --region asia-southeast1 \
  --set-env-vars OPENAI_API_KEY=your-key
```

## Integration with Streamlit Frontend

Add to your Streamlit app:

```python
import requests
import streamlit as st

API_URL = "https://your-backend.run.app"

def process_experience(story, primary_word, primary_desc,
                      secondary_word, secondary_desc,
                      tertiary_word, tertiary_desc):
    response = requests.post(
        f"{API_URL}/api/v1/process-experience",
        json={
            "story": story,
            "primary_vibe_word": primary_word,
            "primary_vibe_description": primary_desc,
            "secondary_resonance_word": secondary_word,
            "secondary_resonance_description": secondary_desc,
            "tertiary_essence_word": tertiary_word,
            "tertiary_essence_description": tertiary_desc,
            "contributor_id": st.session_state.user_id,
            "consent_tier": "public"
        }
    )
    return response.json()

# In your Streamlit app
if st.button("Process Experience"):
    with st.spinner("Processing through Five Layers..."):
        wisdom_drop = process_experience(
            story, primary_word, primary_desc,
            secondary_word, secondary_desc,
            tertiary_word, tertiary_desc
        )
    st.success(f"Wisdom Drop Created: {wisdom_drop['wisdom_drop_id']}")
    st.json(wisdom_drop)
```

## Environment Variables

Required:
- `OPENAI_API_KEY` - OpenAI API key for LLM processing

Optional:
- `MODEL_NAME` - LLM model to use (default: gpt-4.1-mini)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis for caching

## Database Setup (PostgreSQL)

```sql
CREATE TABLE wisdom_drops (
    wisdom_drop_id VARCHAR(50) PRIMARY KEY,
    contributor_id VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    consent_tier VARCHAR(20) NOT NULL,
    original_input JSONB NOT NULL,
    five_layer_analysis JSONB NOT NULL,
    composite_analysis JSONB NOT NULL,
    attribution_score FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_contributor ON wisdom_drops(contributor_id);
CREATE INDEX idx_timestamp ON wisdom_drops(timestamp);
CREATE INDEX idx_consent_tier ON wisdom_drops(consent_tier);
```

## Monitoring

Add health check endpoint to your monitoring:

```bash
curl https://your-backend.run.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-03T19:58:19.848931Z"
}
```

## Rate Limiting

Recommended rate limits:
- 10 requests per minute per user
- 100 requests per hour per user
- 1000 requests per day per user

## Cost Estimation

Per wisdom drop:
- LLM API calls: 6 requests (5 layers + composite)
- Average tokens: ~2000 input + ~500 output per request
- Cost (gpt-4.1-mini): ~$0.02 per wisdom drop

For 1000 wisdom drops/month: ~$20/month in LLM costs

## Security

1. **API Authentication**: Implement API key authentication
2. **Rate Limiting**: Use Redis for distributed rate limiting
3. **Input Validation**: Validate all user inputs
4. **CORS**: Configure allowed origins
5. **HTTPS**: Always use HTTPS in production

## Troubleshooting

### JSON Parsing Errors
- Ensure `response_format={"type": "json_object"}` is set
- Check LLM model supports JSON mode

### Slow Processing
- Use gpt-4.1-nano for faster processing
- Implement caching for repeated requests
- Consider batch processing

### Memory Issues
- Limit concurrent requests
- Use streaming responses for large outputs
- Implement request queuing

## Next Steps

1. Add database integration
2. Implement authentication
3. Add caching layer
4. Set up monitoring and logging
5. Create admin dashboard
6. Implement batch processing
7. Add webhook notifications

