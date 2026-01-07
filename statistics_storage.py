"""
Statistics Storage Module
Handles saving and loading algorithm statistics to/from JSON file
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
import csv


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

    def append_to_csv(self, stat_entry: Dict[str, Any], output_file: str = 'statistics_log.csv') -> None:
        """
        Append a single statistics entry to a CSV file. Creates the CSV with a header
        if it doesn't exist yet. If the CSV already exists, it will respect the
        existing header and only write values for those columns (missing keys will
        be written as empty strings).

        Args:
            stat_entry: A single statistics dict to append (as produced by save_statistics).
            output_file: Path to CSV file to append to.
        """
        # Ensure directory exists for the output file
        out_dir = os.path.dirname(output_file)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        # Flatten nested 'environment' dict into top-level keys (prefix 'env_')
        entry = {}
        for k, v in stat_entry.items():
            if k == 'environment' and isinstance(v, dict):
                for ek, ev in v.items():
                    entry[f'env_{ek}'] = ev
            else:
                entry[k] = v

        # Normalize values to strings for CSV safety
        for k in list(entry.keys()):
            val = entry[k]
            if isinstance(val, (dict, list)):
                entry[k] = json.dumps(val)
            else:
                entry[k] = '' if val is None else str(val)

        # If file doesn't exist or is empty, create header from keys of this entry
        if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
            fieldnames = sorted(entry.keys())
            with open(output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(entry)
            return

        # Otherwise, read existing header using DictReader to get canonical fieldnames
        with open(output_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or sorted(entry.keys())

        # Align row to existing header (missing keys will be empty)
        row = {k: entry.get(k, '') for k in fieldnames}
        with open(output_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(row)
