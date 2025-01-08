# **Movie Recommendation System**

A movie recommendation system using **collaborative filtering** and **content-based filtering** techniques. It leverages **Neo4j** graph databases for efficient data storage and querying. The system recommends movies based on user preferences, ratings, and metadata.

## **File Structure**

```plaintext
movie-recommendation-system/
│
├── data/               # Contains movie metadata and ratings CSV files
├── src/                # Source code
│   ├── recommendation.py          # Main application logic
│   ├── preprocessing.py         # For preprocssing the data
│   ├── import_to_neo4j.py     # To import the data to neo4j database
│
├── requirements.txt    # Dependencies
└── README.md           # Project overview
```

## **Installation**

Follow these steps to set up the project:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Kalze1/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. **Install Dependencies**  
   Make sure you have Python installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Neo4j**

   - Download and install Neo4j from [neo4j.com](https://neo4j.com).
   - Start the Neo4j server and set up credentials.
   - Download the data (movies_metadata.csv and rating_small.csv) from https://www.kaggle.com/code/rounakbanik/movie-recommender-systems/input?select=movies_metadata.csv and include them in movie-recommendation-system/data

4. **Run the Application**

   ```bash
   python src/preprocessing.py
   python src/import_to_neo4j.py
   python src/recommendation.py

   ```

## **Features**

- **Collaborative Filtering**: Recommends movies based on user-user or item-item similarities.
- **Content-Based Filtering**: Recommends movies based on movie metadata (e.g., genres, directors, cast).
- **Neo4j Graph Database**: Efficient querying of user-movie relationships.

## **Usage**

- Add your data in the `data/` directory (e.g., movie metadata and user ratings).
- Start the application to generate personalized movie recommendations.
- Modify `src/reocmmendation.py` to customize recommendation logic.

Enjoy exploring personalized movie recommendations! 🎬✨
