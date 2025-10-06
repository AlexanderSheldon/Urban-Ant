import json
import os # Used here just for demonstration file paths

def geojsonl_to_geojson(input_filepath, output_filepath):
    """
    Converts a GEOJSONL file to a standard GeoJSON FeatureCollection.
    """
    features = []
    
    # 1. Read and parse each line
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # Skip empty lines or lines with only whitespace
                if not line.strip():
                    continue
                
                try:
                    # Parse the JSON object from the line
                    obj = json.loads(line)
                    
                    # Ensure the object is a Feature. 
                    # If it's a Geometry, wrap it in a Feature.
                    if obj.get('type') == 'Feature':
                        features.append(obj)
                    elif obj.get('type') in ['Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString', 'MultiPolygon', 'GeometryCollection']:
                        # Create a minimal Feature object
                        features.append({
                            "type": "Feature",
                            "geometry": obj,
                            "properties": {} # Add empty properties for compliance
                        })
                    else:
                        print(f"Warning: Skipped line with unknown GeoJSON type: {obj.get('type', 'No type field')}")
                        
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line: {line.strip()}. Error: {e}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        return
    
    # 2. Construct the final FeatureCollection
    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # 3. Write the final object to the standard GeoJSON file
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            # Use indent=2 for human-readable output, remove for minimal file size
            json.dump(feature_collection, f, indent=2)
            
        print(f"Conversion successful! Wrote {len(features)} features to {output_filepath}")
        
    except IOError as e:
        print(f"Error writing to output file: {e}")

# Example Usage (assuming 'input.geojsonl' exists)
# geojsonl_to_geojson('input.geojsonl', 'output.geojson')

