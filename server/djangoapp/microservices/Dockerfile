FROM python:3.9.18-slim-bookworm


WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV NLTK_DATA=/usr/local/share/nltk_data
RUN python3 -m nltk.downloader -d /usr/local/share/nltk_data vader_lexicon
COPY . .
RUN ls
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
