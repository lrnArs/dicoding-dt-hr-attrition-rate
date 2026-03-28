import pandas as pd
import numpy as np
import joblib
import sys
import argparse
import warnings
warnings.filterwarnings('ignore')

def load_artifacts(model_path='model_employee.pkl',
                   scaler_path='scaler_employee.pkl',
                   le_target_path='label_encoder_target.pkl',
                   le_cat_path='label_encoder_employee.pkl',
                   num_cols_path='numerical_cols_employee.pkl',
                   cat_cols_path='categorical_cols_employee.pkl'):
    """Load all pre-trained objects."""
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    le_target = joblib.load(le_target_path)
    le_cat = joblib.load(le_cat_path)          # dict: {col: LabelEncoder}
    num_cols = joblib.load(num_cols_path)
    cat_cols = joblib.load(cat_cols_path)
    return model, scaler, le_target, le_cat, num_cols, cat_cols

def preprocess(df, model, le_cat, num_cols, cat_cols, scaler):
    """
    Apply the exact preprocessing used during training:
    - Drop columns that were removed (EmployeeCount, EmployeeId, Over18, StandardHours)
    - Drop target column 'Attrition' if present (it is not a feature)
    - Keep only the columns the model expects (from model.feature_names_in_)
    - Encode categorical columns using saved LabelEncoders
    - Reorder columns to match model.feature_names_in_
    - Scale all features using the saved scaler
    """
    # Step 1: Drop columns that were removed in the notebook
    drop_cols = ['EmployeeCount', 'EmployeeId', 'Over18', 'StandardHours']
    for col in drop_cols:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    # Step 2: Drop target column if present (it is not a feature)
    if 'Attrition' in df.columns:
        df.drop(columns=['Attrition'], inplace=True)

    # Step 3: Get the list of features the model expects (order matters)
    expected_features = model.feature_names_in_

    # Step 4: Check that all expected features are present
    missing = [col for col in expected_features if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in input data: {missing}")

    # Step 5: Keep only the columns the model expects (in any order)
    df = df[expected_features].copy()

    # Step 6: Encode categorical columns using the saved encoders
    for col in cat_cols:
        if col in df.columns:
            encoder = le_cat.get(col)
            if encoder is None:
                raise ValueError(f"No saved encoder found for column '{col}'. "
                                 f"Make sure label_encoder_employee.pkl contains a dictionary with all categorical columns.")
            # Transform: handle unseen categories by mapping to the first known class
            known_classes = set(encoder.classes_)
            # Replace unknown values with the first known class
            mask = ~df[col].isin(known_classes)
            if mask.any():
                print(f"Warning: Column '{col}' contains unseen categories: {df.loc[mask, col].unique()}")
                df.loc[mask, col] = encoder.classes_[0]
            df[col] = encoder.transform(df[col])

    # Step 7: Reorder columns to exactly match the model's training order
    df = df[expected_features]

    # Step 8: Apply the saved scaler (it was fit on all features after encoding)
    df_scaled = scaler.transform(df)

    # Return as DataFrame with same column names
    return pd.DataFrame(df_scaled, columns=expected_features)

def main():
    parser = argparse.ArgumentParser(description='Predict employee attrition using trained model.')
    parser.add_argument('input_csv', help='Path to input CSV file with employee data')
    parser.add_argument('--output', '-o', help='Output CSV file for predictions (optional)')
    args = parser.parse_args()

    # Load artifacts
    try:
        model, scaler, le_target, le_cat, num_cols, cat_cols = load_artifacts()
    except Exception as e:
        print(f"Error loading artifacts: {e}")
        sys.exit(1)

    # Read input data
    try:
        df_input = pd.read_csv(args.input_csv)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    # Preprocess
    try:
        df_processed = preprocess(df_input.copy(), model, le_cat, num_cols, cat_cols, scaler)
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        sys.exit(1)

    # Predict
    predictions = model.predict(df_processed)
    probabilities = model.predict_proba(df_processed)[:, 1]  # probability of Attrition=Yes

    # Decode predictions
    try:
        pred_labels = le_target.inverse_transform(predictions)
    except:
        pred_labels = predictions

    # Add predictions to original dataframe
    df_input['Predicted_Attrition'] = pred_labels
    df_input['Probability_Attrition'] = probabilities

    # Output
    if args.output:
        df_input.to_csv(args.output, index=False)
        print(f"Predictions saved to {args.output}")
    else:
        print(df_input[['Predicted_Attrition', 'Probability_Attrition']].head(10))

if __name__ == "__main__":
    main()