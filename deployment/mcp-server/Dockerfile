FROM node:22-alpine

WORKDIR /app

RUN npm init -y && npm install @cyanheads/pubmed-mcp-server@2.3.4

ENV MCP_TRANSPORT_TYPE=http
ENV MCP_HTTP_PORT=8080
ENV MCP_HTTP_HOST=0.0.0.0
ENV MCP_LOG_LEVEL=info

EXPOSE 8080

CMD ["npx", "@cyanheads/pubmed-mcp-server"]
