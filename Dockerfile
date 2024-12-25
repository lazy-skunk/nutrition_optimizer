FROM python:3.12

WORKDIR /app

RUN apt-get update \
 && apt-get install -y \
    git \
    curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
 && apt-get install -y nodejs

RUN npm install -g typescript

RUN pip install --upgrade pip
COPY pyproject.toml .
RUN pip install .[dev]

COPY . .

ENTRYPOINT ["bash"]