FROM python:3.8
RUN pip install flask
RUN pip install flask-mysql
RUN mkdir templates
RUN mkdir static
COPY sistema_veterinaria.py /app.py
COPY templates/*  /templates/
COPY static/*  /static/
RUN chmod -R a+rwx static
RUN chmod -R a+rwx templates
CMD ["python","app.py"]