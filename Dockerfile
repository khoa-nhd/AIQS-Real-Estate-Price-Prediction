# Container image of the Streamlit app in app/, for any Docker host (Render, Railway, Fly.io,
# Hugging Face Spaces, Google Cloud Run...). Build and run from the repository root:
#   docker build -t aiqs-house-price .
#   docker run -p 8501:8501 aiqs-house-price
# Python must be 3.14: the model pickle holds Python 3.14 bytecode (see app/README.md).
FROM python:3.14-slim

# LightGBM and XGBoost need the OpenMP runtime, which the slim image does not include.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /srv
COPY app/requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

# Only the files the app reads at run time.
COPY app/ app/
COPY models/candidates/final_v3_group_2026-10-26/ models/candidates/final_v3_group_2026-10-26/
COPY data/vietnam_housing_dataset.csv data/
COPY data/processed/splits_v3/train.csv data/processed/splits_v3/
COPY experiments/group_split/test_evaluation.json experiments/group_split/prediction_interval.json \
     experiments/group_split/cv_summary.csv experiments/group_split/
COPY experiments/model_comparison_cv/recovered_model_cv_summary.csv \
     experiments/model_comparison_cv/recovered_model_cv_folds.csv \
     experiments/model_comparison_cv/

RUN useradd --create-home --uid 1000 app
USER app

# Hosts that assign the port (Render, Cloud Run, Railway) pass it in $PORT.
ENV PORT=8501
EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s \
    CMD python -c "import os, urllib.request as r; r.urlopen('http://127.0.0.1:%s/_stcore/health' % os.environ['PORT'])"
CMD ["sh", "-c", "exec streamlit run app/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false"]
