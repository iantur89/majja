import pandas as pd
import random
import datetime

# Load the provided CSV
input_file_path = './Exercises v1 - exercises.csv'
exercises_df = pd.read_csv(input_file_path)

# Create a list of exercises for each category
push_chest_exercises = exercises_df[exercises_df['Push (Chest)'] == 1]
pull_back_exercises = exercises_df[exercises_df['Pull (Back)'] == 1]
shoulders_exercises = exercises_df[exercises_df['Shoulders'] == 1]
push_quads_exercises = exercises_df[exercises_df['Push (Quads)'] == 1]
pull_hamstrings_exercises = exercises_df[exercises_df['Pull (Hamstrings)'] == 1]
calves_exercises = exercises_df[exercises_df['Calves'] == 1]
core_exercises = exercises_df[exercises_df['Core'] == 1]
cardio_exercises = exercises_df[exercises_df['Cardio'] == 1]

# Define aerobic and anaerobic exercises
aerobic_exercises = exercises_df[exercises_df['Aerobic'] == 1]
anaerobic_exercises = exercises_df[exercises_df['Anaerobic'] == 1]

# Function to generate a workout
def generate_workout(workout_id):
    while True:
        workout = [
            push_chest_exercises.sample(1),
            pull_back_exercises.sample(1),
            shoulders_exercises.sample(1),
            push_quads_exercises.sample(1),
            pull_hamstrings_exercises.sample(1),
            calves_exercises.sample(1),
            core_exercises.sample(1),
            cardio_exercises.sample(1)
        ]
        workout_df = pd.concat(workout)
        
        # Ensure the workout has exactly 8 exercises
        if len(workout_df) != 8:
            continue
        
        # Ensure at least 5 exercises are aerobic
        aerobic_count = sum(workout_df['Aerobic'] == 1)
        if aerobic_count < 5:
            num_needed = 5 - aerobic_count
            anaerobic_to_replace = workout_df[workout_df['Anaerobic'] == 1].sample(num_needed)
            new_aerobics = aerobic_exercises.sample(num_needed)
            
            workout_df.update(new_aerobics)
            workout_df.drop(anaerobic_to_replace.index, inplace=True)
            workout_df = pd.concat([workout_df, new_aerobics])
        
        # Ensure anaerobic exercises are not contiguous
        workout_df = workout_df.sample(frac=1).reset_index(drop=True)
        while True:
            anaerobic_indices = workout_df[workout_df['Anaerobic'] == 1].index
            if all(abs(anaerobic_indices[i] - anaerobic_indices[i-1]) > 1 for i in range(1, len(anaerobic_indices))):
                break
            workout_df = workout_df.sample(frac=1).reset_index(drop=True)

        # Ensure no duplicate equipment (e.g., "KB", "Med Ball", "Band")
        equipment_keywords = ["KB", "Med Ball", "Band"]
        contains_duplicate_equipment = any(
            workout_df['Ex Name'].str.contains(keyword).sum() > 1 for keyword in equipment_keywords
        )
        if not contains_duplicate_equipment:
            break

    # Add workout ID
    workout_df.insert(0, 'Workout_ID', workout_id)
    
    # Create targets column
    target_columns = ['Push (Chest)', 'Pull (Back)', 'Shoulders', 'Push (Quads)', 'Pull (Hamstrings)', 'Calves', 'Core', 'Cardio']
    workout_df['targets'] = workout_df.apply(lambda row: ', '.join([col for col in target_columns if row[col] == 1]), axis=1)
    
    # Create tags column
    tag_columns = ['Anaerobic', 'Aerobic', 'Plyometric', 'Strength', 'isolation', 'compound']
    workout_df['tags'] = workout_df.apply(lambda row: ', '.join([col for col in tag_columns if row[col] == 1]), axis=1)
    
    # Drop unnecessary columns
    workout_df = workout_df[['Workout_ID', 'Ex Name', 'Description', 'targets', 'tags']]

    return workout_df

# Generate 20 unique workouts
workouts = []
for i in range(20):
    workout_df = generate_workout(i + 1)
    workout_df['Workout Day'] = i + 1
    workouts.append(workout_df)

# Concatenate all workouts into one DataFrame
final_workouts_df = pd.concat(workouts)

# Save the final DataFrame to a new CSV with a timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
output_file_path = f'workouts_{timestamp}.csv'
final_workouts_df.to_csv(output_file_path, index=False)

# Display the generated workouts DataFrame
print(final_workouts_df)
