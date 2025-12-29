import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import haversine_distances

def calculate_distance(df, center_coords):
    df_radiands = np.radians(df[['latitude', 'longitude']])
    center_radiands = np.radians([center_coords])
    distance_matrix = haversine_distances(df_radiands, center_radiands)
    return (distance_matrix.flatten() * 6371).round(2) # Convert to KM, multiply by Earth's radius

cph = pd.read_csv('copenhagen_listings.csv')
cph_center = [55.6761, 12.5683] #Radhuspladsen
cph['distance_to_center_km'] = calculate_distance(cph, cph_center)
cph['city'] = 'Copenhagen'

cph_fixes = {
    'sterbro': 'Østerbro',
    'Nrrebro': 'Nørrebro',
    'Amager st': 'Amager Øst',
    'Vanlse': 'Vanløse',
    'Brnshj-Husum': 'Brønshøj-Husum'
}
cph['neighbourhood_cleansed'] = cph['neighbourhood_cleansed'].replace(cph_fixes)

oslo = pd.read_csv('oslo_listings.csv')
oslo_center = [59.9139, 10.7522] # Oslo central station
oslo['distance_to_center_km'] = calculate_distance(oslo, oslo_center)
oslo['city'] = 'Oslo'

merged_df = pd.concat([cph, oslo], ignore_index=True)

# Oslo = NOK, Copenhagen = DKK
merged_df['price'] = merged_df['price'].replace(r'[\$,]', '', regex=True).astype(float)
merged_df = merged_df.rename(columns={'price': 'price_local'})

merged_df['id'] = pd.to_numeric(merged_df['id'], errors='coerce')
merged_df = merged_df.dropna(subset=['id', 'neighbourhood_cleansed'])

merged_df = merged_df.reset_index(drop=True)
merged_df.to_csv('merged.csv', index=False)