FROM node:20-slim

WORKDIR /app

COPY package.json ./
RUN cat package.json
RUN rm -f package-lock.json yarn.lock pnpm-lock.yaml
RUN npm install
RUN npm install next@14.0.4
RUN npm list next || true
COPY . .

CMD ["npm", "run", "dev"]
