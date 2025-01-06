# Movie Recommendation System

## Overview

A movie recommendation system using Neo4j, content-based filtering, and collaborative filtering.

## Features

- Imports movie and ratings data into Neo4j.
- Content-based and collaborative filtering for recommendations.
- Fallback mechanism to ensure recommendations for every user.

## Project Structure

- `data/`: Contains datasets (cleaned and original).
- `src/`: Python scripts for data preprocessing, Neo4j import, and recommendation logic.
- `queries/`: Cypher queries for setting up the Neo4j graph.

## Prerequisites

- Python 3.8+
- Neo4j Desktop with GDS plugin installed.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Kalze1/movie-recommendation-system.git
   ```
