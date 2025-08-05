# YieldMax ETF Intraday Trade Scraper

This project downloads the latest intraday trades file from [YieldMax TSLY](https://www.yieldmaxetfs.com/ym/intraday-file) and stores it in a PostgreSQL database on AWS RDS.

## Setup

### Environment Variables

Create a `.env` file or set these in your deployment environment:

```bash
DB_HOST=your-db-host
DB_PORT=5432
DB_NAME=your-db-name
DB_USER=your-username
DB_PASSWORD=your-password
```

### Run Locally

```bash
docker build -t yieldmax-scraper .
docker run --env-file .env yieldmax-scraper
```

### Deploy

You can run this container on any scheduler like:

- AWS ECS with EventBridge
- GitHub Actions with secrets
- AWS Lambda with Docker
