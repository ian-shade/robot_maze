"""
Statistics Storage Module
Handles saving and loading algorithm statistics to/from JSON file
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List


class StatisticsStorage:
    """Manages persistent storage of algorithm run statistics"""

    def __init__(self, storage_file='statistics_history.json'):
        """
        Initialize the storage manager

        Args:
            storage_file: Path to JSON file for storing statistics
        """
        self.storage_file = storage_file
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the storage file if it doesn't exist"""
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump([], f)

    def save_statistics(self, algorithm: str, result: Dict[str, Any],
                       environment_info: Dict[str, Any] = None) -> None:
        """
        Save algorithm statistics to storage

        Args:
            algorithm: Name of the algorithm (e.g., 'BFS-Graph')
            result: Result dictionary from algorithm execution
            environment_info: Optional environment metadata (grid size, etc.)
        """
        # Load existing statistics
        statistics = self.load_all_statistics()

        # Create a serializable copy of result (exclude non-serializable objects)
        stat_entry = {
            'timestamp': datetime.now().isoformat(),
            'algorithm': algorithm,
            'success': result.get('success', False),
            'time': result.get('time', 0),
            'cost': result.get('cost', 0),
            'path_length': result.get('path_length', 0),
            'movement_time': result.get('movement_time', 0),
            'nodes_expanded': result.get('nodes_expanded', 0),
            'max_frontier_size': result.get('max_frontier_size', 0),
        }

        # Add heuristic if present (for A* algorithms)
        if 'heuristic' in result:
            stat_entry['heuristic'] = result['heuristic']

        # Add environment info if provided
        if environment_info:
            stat_entry['environment'] = environment_info

        # Append new entry
        statistics.append(stat_entry)

        # Save to file
        with open(self.storage_file, 'w') as f:
            json.dump(statistics, f, indent=2)

    def load_all_statistics(self) -> List[Dict[str, Any]]:
        """
        Load all statistics from storage

        Returns:
            List of all stored statistics entries
        """
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def get_statistics_by_algorithm(self, algorithm: str) -> List[Dict[str, Any]]:
        """
        Get all statistics for a specific algorithm

        Args:
            algorithm: Name of the algorithm

        Returns:
            List of statistics entries for the specified algorithm
        """
        all_stats = self.load_all_statistics()
        return [s for s in all_stats if s.get('algorithm') == algorithm]

    def get_recent_statistics(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most recent statistics entries

        Args:
            count: Number of recent entries to retrieve

        Returns:
            List of recent statistics entries
        """
        all_stats = self.load_all_statistics()
        return all_stats[-count:] if len(all_stats) > count else all_stats

    def clear_statistics(self) -> None:
        """Clear all statistics from storage"""
        with open(self.storage_file, 'w') as f:
            json.dump([], f)

    def export_to_csv(self, output_file: str = 'statistics_export.csv') -> None:
        """
        Export statistics to CSV format

        Args:
            output_file: Path to output CSV file
        """
        import csv

        all_stats = self.load_all_statistics()
        if not all_stats:
            return

        # Get all possible keys from all entries
        fieldnames = set()
        for stat in all_stats:
            fieldnames.update(stat.keys())

        fieldnames = sorted(fieldnames)

        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_stats)
