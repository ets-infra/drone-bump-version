FROM python:3.11.3-bullseye

COPY bump_version.py /plugin_script/bump_version.py
COPY requirements.txt /plugin_script/requirements.txt
RUN python -m pip install -r /plugin_script/requirements.txt
CMD ["python", "/plugin_script/bump_version.py"]
