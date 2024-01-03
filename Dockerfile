FROM python:3.12

WORKDIR /app

ADD requirements.txt ./

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "uber_pickups.py"]

ADD *.py ./