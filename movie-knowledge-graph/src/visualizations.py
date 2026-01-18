"""
Movie Knowledge Graph Visualizations

This module provides visualization utilities for the movie knowledge graph.
It generates various charts and graph visualizations for analysis and documentation.

Visualizations included:
- Genre distribution (bar chart, pie chart)
- Director analysis (productivity, ratings)
- Knowledge graph network visualization
- Rating distributions
- Timeline visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import networkx as nx
from pathlib import Path
from typing import Optional, Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure default style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11


class MovieVisualizer:
    """
    Visualization utilities for the Movie Knowledge Graph.
    
    This class provides methods to create various visualizations
    from the movie dataset and knowledge graph structures.
    """
    
    def __init__(self, output_dir: str = "output/visualizations"):
        """
        Initialize the visualizer.
        
        Args:
            output_dir: Directory to save generated visualizations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Visualizer initialized. Output directory: {self.output_dir}")
    
    def plot_genre_distribution(self, df: pd.DataFrame, save: bool = True) -> plt.Figure:
        """
        Create genre distribution visualizations (bar chart and pie chart).
        
        Args:
            df: DataFrame with 'genres' column (pipe-separated)
            save: Whether to save the figure to disk
            
        Returns:
            matplotlib Figure object
        """
        # Extract all genres
        all_genres = []
        for genres_str in df['genres']:
            if pd.notna(genres_str):
                all_genres.extend(genres_str.split('|'))
        
        genre_counts = pd.Series(all_genres).value_counts()
        
        # Create figure with two subplots
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Bar chart
        colors = plt.cm.Set3(np.linspace(0, 1, len(genre_counts)))
        genre_counts.plot(kind='bar', ax=axes[0], color=colors, edgecolor='black')
        axes[0].set_title('Movies by Genre', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Genre', fontsize=12)
        axes[0].set_ylabel('Number of Movies', fontsize=12)
        axes[0].tick_params(axis='x', rotation=45)
        
        # Add value labels
        for i, v in enumerate(genre_counts.values):
            axes[0].text(i, v + 0.1, str(v), ha='center', fontweight='bold')
        
        # Pie chart
        colors_pie = plt.cm.Pastel1(np.linspace(0, 1, len(genre_counts)))
        axes[1].pie(genre_counts.values, labels=genre_counts.index, autopct='%1.1f%%',
                   colors=colors_pie, startangle=90, explode=[0.02]*len(genre_counts))
        axes[1].set_title('Genre Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'genre_distribution.png'
            fig.savefig(filepath, dpi=150, bbox_inches='tight')
            logger.info(f"Saved genre distribution to {filepath}")
        
        return fig
    
    def plot_director_analysis(self, df: pd.DataFrame, save: bool = True) -> plt.Figure:
        """
        Create director analysis visualizations.
        
        Args:
            df: DataFrame with 'director', 'rating', 'title' columns
            save: Whether to save the figure to disk
            
        Returns:
            matplotlib Figure object
        """
        # Aggregate director statistics
        director_stats = df.groupby('director').agg({
            'title': 'count',
            'rating': 'mean'
        }).round(2)
        director_stats.columns = ['movie_count', 'avg_rating']
        director_stats = director_stats.sort_values('movie_count', ascending=True)
        
        # Create figure
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Movies per director (horizontal bar)
        colors1 = plt.cm.Set2(np.linspace(0, 1, len(director_stats)))
        director_stats['movie_count'].plot(kind='barh', ax=axes[0], color=colors1, edgecolor='black')
        axes[0].set_title('Movies per Director', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Number of Movies', fontsize=12)
        axes[0].set_ylabel('Director', fontsize=12)
        
        for i, v in enumerate(director_stats['movie_count'].values):
            axes[0].text(v + 0.05, i, str(v), va='center', fontweight='bold')
        
        # Average rating by director
        colors2 = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(director_stats)))
        director_stats['avg_rating'].plot(kind='barh', ax=axes[1], color=colors2, edgecolor='black')
        axes[1].set_title('Average Rating by Director', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Average Rating', fontsize=12)
        axes[1].set_ylabel('')
        
        for i, v in enumerate(director_stats['avg_rating'].values):
            axes[1].text(v + 0.02, i, f'{v:.1f}', va='center', fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'director_analysis.png'
            fig.savefig(filepath, dpi=150, bbox_inches='tight')
            logger.info(f"Saved director analysis to {filepath}")
        
        return fig
    
    def plot_knowledge_graph(self, df: pd.DataFrame, save: bool = True) -> plt.Figure:
        """
        Create a network visualization of the knowledge graph.
        
        Args:
            df: DataFrame with movie data
            save: Whether to save the figure to disk
            
        Returns:
            matplotlib Figure object
        """
        # Build NetworkX graph
        G = nx.Graph()
        
        for _, row in df.iterrows():
            movie_title = row['title']
            director_name = row['director']
            
            # Add nodes
            G.add_node(movie_title, node_type='movie', year=row['year'], rating=row['rating'])
            G.add_node(director_name, node_type='director')
            
            # Add directed_by edge
            G.add_edge(movie_title, director_name, relationship='DIRECTED_BY')
            
            # Add genre nodes and edges
            if pd.notna(row['genres']):
                for genre in row['genres'].split('|'):
                    G.add_node(genre, node_type='genre')
                    G.add_edge(movie_title, genre, relationship='HAS_GENRE')
        
        # Create figure
        fig, ax = plt.subplots(figsize=(16, 12))
        
        # Layout
        pos = nx.spring_layout(G, k=2.5, iterations=50, seed=42)
        
        # Define colors and sizes by node type
        node_colors = []
        node_sizes = []
        for node in G.nodes():
            node_data = G.nodes[node]
            if node_data.get('node_type') == 'movie':
                node_colors.append('#3498db')  # Blue
                node_sizes.append(2000)
            elif node_data.get('node_type') == 'director':
                node_colors.append('#e74c3c')  # Red
                node_sizes.append(2500)
            else:  # Genre
                node_colors.append('#2ecc71')  # Green
                node_sizes.append(1500)
        
        # Draw
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9, ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5, width=1.5, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold', ax=ax)
        
        # Legend
        movie_patch = mpatches.Patch(color='#3498db', label='Movies')
        director_patch = mpatches.Patch(color='#e74c3c', label='Directors')
        genre_patch = mpatches.Patch(color='#2ecc71', label='Genres')
        ax.legend(handles=[movie_patch, director_patch, genre_patch],
                 loc='upper left', fontsize=12, framealpha=0.9)
        
        ax.set_title('Movie Knowledge Graph Visualization', fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'knowledge_graph.png'
            fig.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
            logger.info(f"Saved knowledge graph to {filepath}")
        
        return fig
    
    def plot_rating_distribution(self, df: pd.DataFrame, save: bool = True) -> plt.Figure:
        """
        Create rating distribution visualization.
        
        Args:
            df: DataFrame with 'rating' column
            save: Whether to save the figure to disk
            
        Returns:
            matplotlib Figure object
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        axes[0].hist(df['rating'], bins=10, color='#3498db', edgecolor='black', alpha=0.7)
        axes[0].axvline(df['rating'].mean(), color='red', linestyle='--', linewidth=2, 
                       label=f"Mean: {df['rating'].mean():.2f}")
        axes[0].set_title('Rating Distribution', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Rating', fontsize=12)
        axes[0].set_ylabel('Frequency', fontsize=12)
        axes[0].legend()
        
        # Box plot by director
        df_sorted = df.sort_values('rating', ascending=False)
        sns.boxplot(data=df_sorted, x='director', y='rating', ax=axes[1], palette='Set2')
        axes[1].set_title('Rating by Director', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Director', fontsize=12)
        axes[1].set_ylabel('Rating', fontsize=12)
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'rating_distribution.png'
            fig.savefig(filepath, dpi=150, bbox_inches='tight')
            logger.info(f"Saved rating distribution to {filepath}")
        
        return fig
    
    def plot_timeline(self, df: pd.DataFrame, save: bool = True) -> plt.Figure:
        """
        Create a timeline visualization of movies.
        
        Args:
            df: DataFrame with 'year', 'title', 'rating' columns
            save: Whether to save the figure to disk
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Sort by year
        df_sorted = df.sort_values('year')
        
        years = df_sorted['year'].values
        titles = df_sorted['title'].values
        ratings = df_sorted['rating'].values
        
        # Scatter plot with size based on rating
        sizes = [(r - 8) * 500 + 200 for r in ratings]
        colors = plt.cm.viridis(np.linspace(0, 1, len(years)))
        
        scatter = ax.scatter(years, [1]*len(years), s=sizes, c=colors, alpha=0.7, edgecolors='black')
        
        # Add movie titles
        for i, (year, title, rating) in enumerate(zip(years, titles, ratings)):
            y_offset = 15 if i % 2 == 0 else -25
            ax.annotate(f'{title}\n({rating})', (year, 1),
                       textcoords="offset points", xytext=(0, y_offset),
                       ha='center', fontsize=9, fontweight='bold')
        
        ax.set_xlabel('Year', fontsize=12)
        ax.set_title('Movie Timeline (size = rating)', fontsize=14, fontweight='bold')
        ax.set_yticks([])
        ax.set_xlim(df['year'].min() - 2, df['year'].max() + 2)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'movie_timeline.png'
            fig.savefig(filepath, dpi=150, bbox_inches='tight')
            logger.info(f"Saved timeline to {filepath}")
        
        return fig
    
    def generate_all_visualizations(self, df: pd.DataFrame) -> Dict[str, plt.Figure]:
        """
        Generate all available visualizations.
        
        Args:
            df: DataFrame with movie data
            
        Returns:
            Dictionary of figure names to Figure objects
        """
        logger.info("Generating all visualizations...")
        
        figures = {
            'genre_distribution': self.plot_genre_distribution(df),
            'director_analysis': self.plot_director_analysis(df),
            'knowledge_graph': self.plot_knowledge_graph(df),
            'rating_distribution': self.plot_rating_distribution(df),
            'movie_timeline': self.plot_timeline(df)
        }
        
        logger.info(f"Generated {len(figures)} visualizations in {self.output_dir}")
        return figures


# Example usage
if __name__ == "__main__":
    # Load sample data
    df = pd.read_csv("../data/raw/movies.csv")
    
    # Create visualizer and generate all charts
    visualizer = MovieVisualizer()
    visualizer.generate_all_visualizations(df)
    
    print("\n✅ All visualizations generated!")
    print(f"📁 Check the 'output/visualizations/' directory for results")
