# start_api:
# 	uvicorn app:app --reload

start_streamlit:
	streamlit run app.py

install_requirements:
	pip install -r requirements.txt
