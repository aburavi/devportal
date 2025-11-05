FROM fastapi:python-pgsql

# Copy folder app
COPY ./services/userapp /app

COPY ./services/userapp/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./services/userapp/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./services/userapp/prestart.sh /prestart.sh
RUN chmod +x /prestart.sh

EXPOSE 80

CMD ["/start.sh"]
