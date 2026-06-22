import numpy as np
from sklearn.cluster import KMeans
from geopy.distance import geodesic

class RouteOptimizer:
    @staticmethod
    def optimize_route(students_data):
        """
        Optimize student pickup sequence using K-means clustering
        
        Input: List of students with id, name, lat, lng
        Output: Optimized order of students
        """
        
        if not students_data:
            return []
        
        # Extract coordinates
        coordinates = np.array([
            [student['lat'], student['lng']] 
            for student in students_data
        ])
        
        # If only 1 or 2 students, no need to optimize
        if len(students_data) <= 2:
            return students_data
        
        # Determine number of clusters (stops to consolidate)
        n_clusters = max(1, len(students_data) // 2)
        
        try:
            # K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            kmeans.fit(coordinates)
            
            # Get cluster labels
            labels = kmeans.labels_
            
            # Group students by cluster
            clustered_students = {}
            for idx, label in enumerate(labels):
                if label not in clustered_students:
                    clustered_students[label] = []
                clustered_students[label].append(students_data[idx])
            
            # Order clusters by distance from origin
            ordered_students = []
            visited_clusters = set()
            current_lat, current_lng = 13.0827, 80.2707  # Starting point (Main Road)
            
            while len(visited_clusters) < len(clustered_students):
                # Find nearest unvisited cluster
                min_distance = float('inf')
                nearest_cluster = None
                
                for cluster_id, students in clustered_students.items():
                    if cluster_id in visited_clusters:
                        continue
                    
                    # Get cluster center
                    cluster_center = (students[0]['lat'], students[0]['lng'])
                    distance = geodesic(
                        (current_lat, current_lng),
                        cluster_center
                    ).km
                    
                    if distance < min_distance:
                        min_distance = distance
                        nearest_cluster = cluster_id
                
                if nearest_cluster is not None:
                    visited_clusters.add(nearest_cluster)
                    ordered_students.extend(clustered_students[nearest_cluster])
                    
                    # Update current location
                    if clustered_students[nearest_cluster]:
                        last_student = clustered_students[nearest_cluster][-1]
                        current_lat = last_student['lat']
                        current_lng = last_student['lng']
            
            return ordered_students
            
        except Exception as e:
            print(f"Error in optimization: {e}")
            return students_data
    
    @staticmethod
    def calculate_distance(lat1, lng1, lat2, lng2):
        """Calculate distance between two points"""
        return geodesic((lat1, lng1), (lat2, lng2)).km
    
    @staticmethod
    def calculate_total_distance(students_list):
        """Calculate total route distance"""
        if len(students_list) < 2:
            return 0
        
        total_distance = 0
        # Start from main road
        current_lat, current_lng = 13.0827, 80.2707
        
        for student in students_list:
            distance = RouteOptimizer.calculate_distance(
                current_lat, current_lng,
                student['lat'], student['lng']
            )
            total_distance += distance
            current_lat = student['lat']
            current_lng = student['lng']
        
        return round(total_distance, 2)