FROM python:3.13-slim-trixie
ENV PYTHONUNBUFFERED=1

EXPOSE 80
LABEL maintainer="martas@imm.cz"

WORKDIR /app
COPY ./pyproject.toml ./README.md .
RUN pip install --break-system-packages -e .  
COPY ./assets /app/assets
COPY ./main.py /app/main.py
CMD ["python", "main.py"]

