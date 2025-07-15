const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const { createProxyMiddleware } = require('http-proxy-middleware');
const backendApiUrl = process.env.BACKEND_API_URL || 'http://localhost:8000';

// Serve static files from static directory
app.use('/static', express.static(path.join(__dirname, 'static')));

// Serve static files from public directory
app.use('/public', express.static(path.join(__dirname, 'public')));


app.use('/api/log', createProxyMiddleware({
  target: backendApiUrl,
  changeOrigin: true
}))

// Set up template engine for Jinja2 templates
app.set('view engine', 'html');
app.set('views', path.join(__dirname, 'templates'));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'frontend' });
});

// Serve templates as static HTML files
app.get('/RAG_Chat', (req, res) => {
  res.sendFile(path.join(__dirname, 'templates', 'RAG_Chat.html'));
});

app.get('/pdf_question_generator', (req, res) => {
  res.sendFile(path.join(__dirname, 'templates', 'pdf_question_generator.html'));
});

app.get('/csv_question_generator', (req, res) => {
  res.sendFile(path.join(__dirname, 'templates', 'csv_question_generator.html'));
});

app.get('/document-chunking', (req, res) => {
  res.sendFile(path.join(__dirname, 'templates', 'document-chunking.html'));
});

app.get('/node_editor', (req, res) => {
  res.sendFile(path.join(__dirname, 'templates', 'node_editor.html'));
});

// Catch all route for other static files
app.get('*', (req, res) => {
  res.status(404).send('Page not found');
});

app.listen(PORT, () => {
  console.log(`Frontend server running on port ${PORT}`);
  console.log(`Health check available at http://localhost:${PORT}/health`);
}); 