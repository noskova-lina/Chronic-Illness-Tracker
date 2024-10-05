import pandas as pd
from database import SessionLocal
import models


# Function to process and insert data
def insert_data_from_csv(file_path: str):
    # Read the CSV file
    df = pd.read_csv(file_path, delimiter=',', low_memory=False)  # Avoids dtype warnings

    # Open a database session
    db = SessionLocal()

    try:
        # Insert data into the database
        for _, row in df.iterrows():
            # Insert User if not exists
            user_id = row['user_id']
            existing_user = db.query(models.User).filter(models.User.user_id == user_id).first()

            if not existing_user:
                user = models.User(
                    user_id=user_id,
                    age=row['age'] if pd.notnull(row['age']) else None,
                    sex=row['sex'] if pd.notnull(row['sex']) else None,
                    country=row['country'] if pd.notnull(row['country']) else None
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            # Parse check-in date with flexible format handling
            try:
                checkin_date = pd.to_datetime(row['checkin_date'], format='%d/%m/%Y', dayfirst=True)
            except ValueError:
                checkin_date = pd.to_datetime(row['checkin_date'], format='%Y-%m-%d')

            # Insert CheckIn if not exists
            existing_checkin = db.query(models.CheckIn).filter(models.CheckIn.user_id == user_id,
                                                               models.CheckIn.date == checkin_date).first()

            if not existing_checkin:
                checkin = models.CheckIn(
                    user_id=user_id,
                    date=checkin_date
                )
                db.add(checkin)
                db.commit()
                db.refresh(checkin)
            else:
                checkin = existing_checkin

            # Insert based on the trackable_type
            trackable_type = row['trackable_type']

            if trackable_type == 'Condition' or trackable_type == 'Symptom':
                # Check if the symptom already exists for this check-in
                existing_symptom = db.query(models.Symptom).filter(models.Symptom.checkin_id == checkin.checkin_id,
                                                                   models.Symptom.symptom_name == row[
                                                                       'trackable_name']).first()

                if not existing_symptom:
                    symptom = models.Symptom(
                        checkin_id=checkin.checkin_id,
                        symptom_name=row['trackable_name'],
                        severity=int(row['trackable_value'])
                    )
                    db.add(symptom)
                    db.commit()

            elif trackable_type == 'Tag':
                # Check if the tag already exists for this check-in
                existing_tag = db.query(models.Tag).filter(models.Tag.checkin_id == checkin.checkin_id,
                                                           models.Tag.tag_name == row['trackable_name']).first()

                if not existing_tag:
                    tag = models.Tag(
                        checkin_id=checkin.checkin_id,
                        tag_name=row['trackable_name']
                    )
                    db.add(tag)
                    db.commit()

            elif trackable_type == 'Treatment':
                # Check if the treatment already exists for this check-in
                existing_treatment = db.query(models.Treatment).filter(
                    models.Treatment.checkin_id == checkin.checkin_id,
                    models.Treatment.treatment_name == row['trackable_name']).first()

                if not existing_treatment:
                    treatment = models.Treatment(
                        checkin_id=checkin.checkin_id,
                        treatment_name=row['trackable_name']
                    )
                    db.add(treatment)
                    db.commit()

            elif trackable_type == 'Weather':
                # Check if the weather entry already exists for this check-in
                existing_weather = db.query(models.Weather).filter(
                    models.Weather.checkin_id == checkin.checkin_id
                ).first()

                # Initialize variables to collect weather data for the current check-in
                description = None
                temperature_min = None
                temperature_max = None
                humidity = None
                pressure = None

                # Weather description is the trackable_name (e.g., 'icon', 'rainy day')
                if row['trackable_name'] == 'icon':
                    description = row['trackable_value']
                elif row['trackable_name'] == 'temperature_min':
                    temperature_min = row['trackable_value']
                elif row['trackable_name'] == 'temperature_max':
                    temperature_max = row['trackable_value']
                elif row['trackable_name'] == 'humidity':
                    humidity = float(row['trackable_value'])
                elif row['trackable_name'] == 'pressure':
                    pressure = float(row['trackable_value'])

                if existing_weather:
                    # Update fields if they are currently None
                    if description and existing_weather.description is None:
                        existing_weather.description = description
                    if temperature_min and temperature_max and existing_weather.temperature is None:
                        existing_weather.temperature = f"{temperature_min}-{temperature_max}"
                    if humidity is not None and existing_weather.humidity is None:
                        existing_weather.humidity = humidity
                    if pressure is not None and existing_weather.pressure is None:
                        existing_weather.pressure = pressure

                else:
                    # Format temperature as "min-max" if both are available
                    if temperature_min and temperature_max:
                        temperature = f"{temperature_min}-{temperature_max}"
                    else:
                        temperature = None

                    # Insert the weather record if it's not a duplicate
                    weather = models.Weather(
                        checkin_id=checkin.checkin_id,
                        description=description,
                        temperature=temperature,
                        humidity=humidity,
                        pressure=pressure
                    )
                    db.add(weather)

                # Commit changes after processing weather data
                db.commit()

        print("Data successfully inserted into the database.")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        # Close the database session
        db.close()


# Main entry point
if __name__ == "__main__":
    # Path to the CSV file
    file_path = "data.csv"

    # Call the function to insert data
    insert_data_from_csv(file_path)
