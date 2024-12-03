# Data Directory Overview

Welcome to the `data/` directory of the Coffee Tasting Sessions repository. This directory contains all the data related to the coffee tasting sessions, including information about coffees, participants, sessions, ratings, and rankings.

## Directory Structure

The `data/` directory is organized as follows:

```
data/
├── participants.yaml
├── coffees/
│   └── <coffee_id>.yaml
└── sessions/
    └── <session_date>/
        ├── participants.yaml
        ├── coffees/  
        │   └── <coffee_id>.yaml
        └── rankings/
            └── <participant_id>.yaml
```

### 1. `coffees/`

- **Purpose**: Stores global metadata for each coffee bean.
- **Contents**: YAML files named `<coffee_id>.yaml`.
- **Data Included**:
  - `coffee_id`: Unique identifier for the coffee.
  - `url`: URL to the coffee's webpage or additional information.
  - `name`: Name of the coffee.
  - `roaster`: Name of the coffee roaster.
  - `origin`: Country or region of origin.
  - `process_method`: Processing method (e.g., Washed, Natural).
  - `roast_level`: Roast level (e.g., Light, Medium, Dark).
  - `flavor_notes`: List of flavor notes.
- **Example File**: `coffees/ethiopia_yirgacheffe.yaml`

### 2. `participants.yaml` and `sessions/<session_date>/participants.yaml`

> [WARNING!]
> This section is wrong.

- **Purpose**: Contains list of participants.
- **Contents**: YAML files named `participants.yaml`.
- **Data Included**: 
  - `participants.yaml`: List of content id that participated at least once.
  - `sessions/<session_date>/participants.yaml`: List of content id that participated within this session.

### 3. `sessions/`

- **Purpose**: Stores data specific to each tasting session.
- **Contents**: Subdirectories named after the session date in `YYYY-MM-DD` format.

#### a. `sessions/<session_date>/coffees/`

- **Purpose**: Contains session-specific information about the coffees tasted.
- **Contents**: YAML files named `<coffee_id>.yaml`.
- **Data Included**:
  - `coffee_id`: Identifier matching a file in `data/coffees/`.
  - `session_date`: Date of the session.
  - `submitted_by`: `participant_id` of who brought the coffee.
  - `roast_date`: Date the coffee was roasted.
  - `crop_date`: Date the coffee was harvested.
  - `weight`: Weight of the coffee in grams.
  - `price`: Price of the coffee.
- **Example File**: `sessions/2023-10-15/coffees/ethiopia_yirgacheffe.yaml`

#### b. `sessions/<session_date>/rankings/`

- **Purpose**: Contains participant rankings and ratings for the session.
- **Contents**: YAML files named `<participant_id>.yaml`.
- **Data Included**:
  - participant_id: Identifier of the participant.
  - session_date: Date of the session.
  - rankings: List of rankings and ratings for each coffee.
- **Example File**: sessions/2023-10-15/rankings/participant_jane_smith.yaml
