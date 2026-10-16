"""Audit local raw -> v1 and restore two source columns without resplitting.

Run: python src/preprocessing/repair_input_v2.py --project-root <repository>
No download, training, target analysis or modification of v1 files.
"""
from pathlib import Path
import argparse
import hashlib
import io
import json
import re
import unicodedata
import numpy as np
import pandas as pd


def normalize_location_frame(X):
    result = X.copy()
    def normalize(value):
        if pd.isna(value):
            return value
        value = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', str(value))).strip().rstrip('.').strip()
        assert value, 'Empty location after normalization'
        return value
    for column in ['City', 'District']:
        result[column] = result[column].map(normalize)
    return result


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_once(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        assert path.read_bytes() == payload, f'Refusing to overwrite changed file: {path}'
    else:
        temporary = path.with_suffix(path.suffix + '.tmp')
        temporary.write_bytes(payload)
        temporary.replace(path)


def repair(root):
    root = Path(root)
    raw_path = root / 'data/vietnam_housing_dataset.csv'
    v1_path = root / 'data/_v1.csv'
    old = root / 'data/processed/splits_v1'
    dest = root / 'data/processed/splits_v2'
    report_dir = root / 'reports/me/input_audit_v2'
    source_paths = [raw_path, v1_path, *sorted(old.glob('*.csv'))]
    before = {str(p.relative_to(root)): sha(p) for p in source_paths}
    raw, v1 = pd.read_csv(raw_path), pd.read_csv(v1_path)
    assert len(raw) == len(v1) == 30229 and raw.duplicated().sum() == 0
    reconstructed = raw.copy()
    parts = raw.Address.str.split(',')
    reconstructed['City'] = parts.map(lambda p: p[-1].strip() if isinstance(p, list) and len(p) else np.nan)
    reconstructed['District'] = parts.map(lambda p: p[-2].strip() if isinstance(p, list) and len(p) >= 2 else np.nan)
    reconstructed = reconstructed.drop(columns='Address')
    replay = reconstructed.copy()
    for column, fallback in [('Frontage', 0), ('Access Road', 2.0)]:
        replay[column] = replay.groupby('District')[column].transform(lambda s: s.fillna(s.median())).fillna(fallback)
    # Reproduce CSV round-trip, including empty City -> NaN.
    replay = pd.read_csv(io.StringIO(replay[v1.columns].to_csv(index=False)))
    pd.testing.assert_frame_equal(replay, v1, check_dtype=False, rtol=1e-12, atol=1e-12)
    corrected = v1.copy()
    audit = []
    for column in ['Frontage', 'Access Road']:
        corrected[column] = raw[column]
        observed_changed = raw[column].notna() & ~raw[column].eq(v1[column])
        audit.append({'column': column, 'missing_raw': int(raw[column].isna().sum()),
                      'missing_v1': int(v1[column].isna().sum()),
                      'observed_values_restored': int(observed_changed.sum()),
                      'observed_restored_row_ids': raw.index[observed_changed].tolist()})
    untouched = [c for c in v1 if c not in ['Frontage', 'Access Road']]
    pd.testing.assert_frame_equal(corrected[untouched], v1[untouched])
    membership = pd.read_csv(old / 'split_manifest.csv')
    assert membership.row_id.is_unique and set(membership.row_id) == set(range(len(raw)))
    split_report = []
    for name in ['train', 'validation', 'calibration', 'test']:
        saved = pd.read_csv(old / f'{name}.csv')
        ids = saved.row_id.to_numpy()
        assert saved.row_id.is_unique
        assert set(ids) == set(membership.loc[membership.split.eq(name), 'row_id'])
        pd.testing.assert_frame_equal(saved.drop(columns='row_id').reset_index(drop=True),
                                      v1.iloc[ids].reset_index(drop=True), check_dtype=False, rtol=1e-12, atol=1e-12)
        repaired = saved.copy()
        for column in ['Frontage', 'Access Road']:
            repaired[column] = raw.iloc[ids][column].to_numpy()
        pd.testing.assert_frame_equal(repaired[['row_id', *untouched]], saved[['row_id', *untouched]])
        payload = repaired.to_csv(index=False).encode('utf-8-sig')
        write_once(dest / f'{name}.csv', payload)
        pd.testing.assert_frame_equal(pd.read_csv(dest / f'{name}.csv'), repaired, check_dtype=False, rtol=1e-12, atol=1e-12)
        split_report.append({'split': name, 'rows': len(saved), 'row_id_order_preserved': True})
    write_once(dest / 'split_manifest.csv', (old / 'split_manifest.csv').read_bytes())
    assert before == {str(p.relative_to(root)): sha(p) for p in source_paths}
    result = {'status': 'confirmed_pre_split_imputation', 'rows': len(raw),
              'evidence': 'Full cleaning formula replay matches all 13 v1 columns after CSV round-trip.',
              'provenance_limit': 'Export cell names data_estate_house_VN.csv; file rename to _v1.csv is not documented.',
              'audit': audit, 'splits': split_report, 'source_sha256': before,
              'corrected_sha256': {str(p.relative_to(root)): sha(p) for p in sorted(dest.glob('*.csv'))},
              'heldout_access': 'Calibration/test used only for row identity and mechanical repair, not EDA or scoring.'}
    payload = json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8')
    write_once(dest / 'repair_manifest.json', payload)
    write_once(report_dir / 'audit.json', payload)
    print(json.dumps({'audit': audit, 'splits': split_report}, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-root', type=Path, default=Path(__file__).resolve().parents[2])
    repair(parser.parse_args().project_root)
