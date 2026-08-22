.PHONY: setup validate pipeline test lint ui clean
setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
validate:
	python scripts/validate_data.py
pipeline:
	python scripts/run_pipeline.py
test:
	pytest -q
lint:
	ruff check .
ui:
	streamlit run app.py
clean:
	rm -rf data/output/* .pytest_cache __pycache__
	touch data/output/.gitkeep
