import argparse
import os
import json
from datetime import datetime

import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

try:
    from joblib import dump, load
except Exception:
    from sklearn.externals.joblib import dump, load

from sentiment.models import SentimentModel, load_data


def compute_metrics(y_true, y_pred):
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision_macro': precision_score(y_true, y_pred, average='macro', zero_division=0),
        'recall_macro': recall_score(y_true, y_pred, average='macro', zero_division=0),
        'f1_macro': f1_score(y_true, y_pred, average='macro', zero_division=0),
    }
    return metrics


def per_language_breakdown(df, pred_col='predicted'):
    results = {}
    if 'language' not in df.columns:
        return results
    for lang, group in df.groupby('language'):
        yt = group['sentiment']
        yp = group[pred_col]
        results[lang] = compute_metrics(yt, yp)
    return results


def main():
    parser = argparse.ArgumentParser(description='Evaluate sentiment model on a labeled CSV.')
    parser.add_argument('--test-csv', help='Labeled CSV with columns `headline` and `sentiment`', required=False)
    parser.add_argument('--train-csv', help='Optional training CSV to train a model before evaluating', required=False)
    parser.add_argument('--model-out', help='Path to save trained model (joblib)', required=False)
    parser.add_argument('--model-in', help='Path to load existing model (joblib)', required=False)
    parser.add_argument('--report-out', help='Directory to save evaluation report', default='../reports')
    args = parser.parse_args()

    # ensure report dir
    report_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), args.report_out))
    os.makedirs(report_dir, exist_ok=True)

    model = None
    if args.model_in and os.path.exists(args.model_in):
        print('[*] Loading model from', args.model_in)
        model = load(args.model_in)

    # Load data
    if args.test_csv and os.path.exists(args.test_csv):
        print('[*] Loading test data from', args.test_csv)
        df_test = pd.read_csv(args.test_csv)
        # support common column names
        if 'headline' not in df_test.columns or 'sentiment' not in df_test.columns:
            raise ValueError('test CSV must contain `headline` and `sentiment` columns')
    else:
        print('[!] No test CSV provided or file not found. Exiting.')
        print('Provide `--test-csv path/to/labeled.csv` with columns `headline` and `sentiment`.')
        return

    # If no model available, try to train one
    if model is None:
        if args.train_csv and os.path.exists(args.train_csv):
            print('[*] Training model from', args.train_csv)
            X_train, y_train = load_data(args.train_csv)
            m = SentimentModel()
            m.fit(X_train, y_train)
            model = m
        else:
            # fallback: train on part of test CSV (WARNING printed)
            print('[!] No model or train CSV provided — training on a split of the test CSV (not recommended for final evaluation)')
            X = df_test['headline']
            y = df_test['sentiment']
            X_train, X_holdout, y_train, y_holdout = train_test_split(X, y, test_size=0.3, random_state=42)
            m = SentimentModel()
            m.fit(X_train, y_train)
            model = m

    # Save model if requested
    if args.model_out:
        out_dir = os.path.dirname(args.model_out)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        dump(model, args.model_out)
        print('[*] Saved model to', args.model_out)

    # Run predictions on df_test
    headlines = df_test['headline'].fillna('').astype(str).tolist()
    # SentimentModel.predict expects an iterable
    preds = model.predict(headlines)

    df_test = df_test.copy()
    df_test['predicted'] = preds

    # compute overall metrics
    y_true = df_test['sentiment']
    y_pred = df_test['predicted']
    metrics = compute_metrics(y_true, y_pred)
    report = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'metrics': metrics,
        'classification_report': classification_report(y_true, y_pred, zero_division=0, output_dict=True),
        'confusion_matrix': confusion_matrix(y_true, y_pred).tolist(),
        'per_language': per_language_breakdown(df_test, 'predicted')
    }

    # Save a JSON report
    out_path = os.path.join(report_dir, f'evaluation_{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print('[*] Evaluation saved to', out_path)

    # Save per-sample CSV with predictions
    csv_out = os.path.join(report_dir, f'evaluation_samples_{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}.csv')
    df_test.to_csv(csv_out, index=False)
    print('[*] Predictions saved to', csv_out)

    # Print quick summary
    print('\n=== Summary ===')
    print('Accuracy:', metrics['accuracy'])
    print('Precision (macro):', metrics['precision_macro'])
    print('Recall (macro):', metrics['recall_macro'])
    print('F1 (macro):', metrics['f1_macro'])
    print('Classification report saved in JSON under `classification_report`')


if __name__ == '__main__':
    main()
