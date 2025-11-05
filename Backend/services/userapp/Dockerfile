FROM fastapi:python-pgsql

ENV PYTHONUNBUFFERED=1

# Copy folder app
COPY . /app

RUN pip install structlog orjson
RUN pip install minio
RUN pip install starlette
RUN pip install openpyxl
RUN pip install pycryptodome

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./prestart.sh /prestart.sh
RUN chmod +x /prestart.sh

EXPOSE 80
CMD ["/start.sh"]