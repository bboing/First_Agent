const express = require('express');
const path = require('path');

const app = express();
const multer = require('multer');
const upload = multer();

const PORT = process.env.PORT || 3000;
const { createProxyMiddleware } = require('http-proxy-middleware');
const backendApiUrl = process.env.BACKEND_API_URL || 'http://localhost:8000';

// Serve static files from static directory
app.use('/static', express.static(path.join(__dirname, 'static')));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));



// API 프록시 설정 (모든 라우트보다 위에 위치해야 함)
app.use('/api', createProxyMiddleware({
  target: backendApiUrl,
  changeOrigin: true,
  pathRewrite: { '^/api': '' }
}))

// Serve static files from public directory
app.use('/public', express.static(path.join(__dirname, 'public')));

// Set up template engine for Jinja2 templates
app.set('view engine', 'html');
app.set('views', path.join(__dirname, 'templates'));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'frontend' });
});

app.get('/get-business-department', async (req, res) => {
  try {
    const backendResponse = await fetch(`${backendApiUrl}/get-business-department`);
    const data = await backendResponse.json();
    res.json(data);
  } catch (error) {
    console.error('Error fetching business department:', error);
    res.status(500).send('Error fetching business data');
  }
});


app.post('/uploadfiles/pdf', upload.fields([{ name: 'file1' }, { name: 'file2' }]), (req, res) => {
  try {
      const project_id = req.body.project_id;
      const file1 = req.files[file1] ? req.files[file1][0] : null;
      const file2 = req.files[file2] ? req.files[file2][0] : null;

      if (!file1 || !file2 || !project_id) {
        return res.status(400).send({ error: 'Missing file1, file2, or project_id' });
      }

      const formData = new FormData();
      formData.append('project_id', project_id);
      formData.append('file1', file1.buffer, { filename: file1.originalname, contentType: file1.mimetype });
      formData.append('file2', file2.buffer, { filename: file2.originalname, contentType: file2.mimetype });

      const backendResponse = fetch(`${backendApiUrl}/uploadfiles/pdf`, {
      method: 'POST',
      body: formData
    });
      const data = backendResponse.json();
      res.json(data);
  } catch (error) {
    console.error('Error uploading files:', error);
    res.status(500).send('Error uploading files');
  }
});

app.post('/uploadfiles/sentence', upload.fields([{ name: 'file1' }, { name: 'file2' }]), (req, res) => {
  try {
    const { field_business, user_type, Constraints, project_id } = req.body;
    const file1 = req.files[file1] ? req.files[file1][0] : null;
    const file2 = req.files[file2] ? req.files[file2][0] : null;

    if (!file1 || !file2 || !project_id) {
      return res.status(400).send({ error: 'Missing file1, file2, or project_id' });
    }

    const formData = new FormData();
    formData.append('field_business', field_business);
    formData.append('user_type', user_type);
    formData.append('Constraints', Constraints);
    formData.append('project_id', project_id);
    formData.append('file1', file1.buffer, { filename: file1.originalname, contentType: file1.mimetype });
    formData.append('file2', file2.buffer, { filename: file2.originalname, contentType: file2.mimetype });

    const backendResponse = fetch(`${backendApiUrl}/uploadfiles/sentence`, {
      method: 'POST',
      body: formData
    });
    const data = backendResponse.json();
    res.json(data);
  } catch (error) {
    console.error('Error uploading files:', error);
    res.status(500).send('Error uploading files');
  }
});

app.post('/process-pdf', upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).send({ error: 'No file uploaded.' });
        }

        const formData = new FormData();
        const blob = new Blob([req.file.buffer], { type: req.file.mimetype });
        formData.append('file', blob, req.file.originalname);

        const backendResponse = await fetch(`${backendApiUrl}/process-pdf`, {
            method: 'POST',
            body: formData,
        });

        if (!backendResponse.ok) {
            const errorText = await backendResponse.text();
            console.error('Backend error:', errorText);
            return res.status(backendResponse.status).send({ error: `Backend error: ${errorText}` });
        }

        const data = await backendResponse.json();
        res.json(data);
    } catch (error) {
        console.error('Error processing PDF:', error);
        res.status(500).send({ error: 'Error processing PDF' });
    }
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