FROM node:22-alpine AS build
WORKDIR /src
COPY package.json package-lock.json* ./
RUN npm install
COPY frontend ./frontend
RUN npm run build
FROM nginx:alpine
COPY --from=build /src/frontend/dist /usr/share/nginx/html
EXPOSE 80
