FROM node:22-bullseye

WORKDIR /app

COPY frontend-ui/package.json frontend-ui/package-lock.json /app/
RUN npm ci --legacy-peer-deps

COPY frontend-ui /app

EXPOSE 4200

CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--port", "4200", "--configuration", "docker"]
