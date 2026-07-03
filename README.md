# Media Monitoring Application - Palm Oil Industry

A comprehensive media monitoring system designed to track all forms of online media coverage related to the Indonesian palm oil industry across national, subnational, international, and social media platforms.

## Overview

This application monitors:
- **National & Subnational Media**: Indonesian news outlets and regional publications
- **International Media**: Global news coverage
- **Journals**: Academic and professional publications (national and international)
- **Social Media**: LinkedIn, Facebook, Instagram

## Key Monitoring Focus Areas

### 1. Production & Supply Chain
- Fresh Fruit Bunches (TBS/Tandan Buah Segar)
- Palm seedlings (bibit sawit)
- Smallholder farmers (petani plasma, petani swadaya)
- Palm oil mills (PKS/Pabrik Kelapa Sawit)
- Replanting programs (PSR/Peremajaan Sawit Rakyat)

### 2. Products & Derivatives
- Crude Palm Oil (CPO)
- Palm Kernel Oil (PKO)
- Biodiesel variants (B35, B40, B50)
- Fatty Acid Methyl Ester (FAME)
- Oleochemicals and refining

### 3. Market & Policy
- CPO and TBS pricing
- Export regulations and tariffs
- Domestic Market Obligation (DMO)
- Domestic Price Obligation (DPO)
- BPDPKS (Palm Oil Export Fund)
- Anti-deforestation legislation (EUDR)

### 4. Sustainability & Environmental
- RSPO (Roundtable on Sustainable Palm Oil)
- ISPO (Indonesian Sustainable Palm Oil)
- NDPE (No Deforestation, No Peat, No Exploitation)
- Deforestation monitoring
- Forest fires (karhutla)
- Peatland protection
- Carbon emissions
- POME (Palm Oil Mill Effluent)
- Land conflicts

### 5. Social Impact
- Worker rights and conditions
- Child labor concerns
- Palm oil boycotts
- NGO campaigns (Greenpeace, Walhi, Sawit Watch)
- Reputational challenges

## Technology Stack

- **Backend**: Python (FastAPI/Django)
- **Data Collection**: Web scrapers, API integrations
- **Search**: Elasticsearch for indexing and searching
- **Database**: PostgreSQL for structured data
- **Message Queue**: Celery/RabbitMQ for async tasks
- **Frontend**: React/Vue.js dashboard
- **ML/NLP**: Sentiment analysis, entity extraction
- **Deployment**: Docker, Kubernetes

## Project Structure

```
media-monitoring-app/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── scrapers/
│   ├── collectors/
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
├── docker-compose.yml
├── .env.example
└── docs/
```

## Getting Started

See [SETUP.md](./docs/SETUP.md) for installation and configuration instructions.

## Features

- Real-time media monitoring across multiple platforms
- Advanced keyword filtering with boolean logic
- Sentiment analysis of articles
- Source credibility scoring
- Geographic tagging and analysis
- Automated alerts and notifications
- Comprehensive analytics dashboard
- Historical trend analysis
- Export capabilities (CSV, PDF, JSON)
- Multi-language support

## API Documentation

See [API.md](./docs/API.md) for detailed API endpoints.

## Configuration

All monitoring keywords and filters are defined in `config/keywords.json`.

## License

MIT
