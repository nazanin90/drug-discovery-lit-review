FROM node:22-alpine

WORKDIR /app

RUN npm install -g @cyanheads/pubmed-mcp-server@2.3.4

ENV MCP_TRANSPORT_TYPE=http
ENV MCP_HTTP_PORT=8080
ENV MCP_LOG_LEVEL=info

EXPOSE 8080

CMD ["node", "/usr/local/lib/node_modules/@cyanheads/pubmed-mcp-server/dist/index.js"]
