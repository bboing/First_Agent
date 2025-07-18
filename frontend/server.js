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


// 로그 API 직접 구현 (프록시 대신)
app.get('/api/log', async (req, res) => {
  try {
    console.log('Log API called, fetching from backend:', backendApiUrl + '/log');
    const backendResponse = await fetch(`${backendApiUrl}/log`);
    
    if (!backendResponse.ok) {
      console.error('Backend log API error:', backendResponse.status, backendResponse.statusText);
      return res.status(backendResponse.status).json({ 
        error: 'Backend log API error', 
        status: backendResponse.status 
      });
    }
    
    const data = await backendResponse.json();
    console.log('Log data received, length:', JSON.stringify(data).length);
    res.json(data);
  } catch (error) {
    console.error('Error fetching logs:', error.message);
    res.status(500).json({ error: 'Error fetching logs', message: error.message });
  }
});

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

app.post('/process-pdf', upload.array('files'), async (req, res) => {
    try {
        if (!req.files || req.files.length === 0) {
            return res.status(400).send({ error: 'No files uploaded.' });
        }

        const formData = new FormData();
        
        // 모든 파일을 FormData에 추가
        for (const file of req.files) {
            const blob = new Blob([file.buffer], { type: file.mimetype });
            formData.append('files', blob, file.originalname);
        }

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

// RAG 챗봇 API 프록시
app.post('/chat', async (req, res) => {
    try {
        const backendResponse = await fetch(`${backendApiUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(req.body)
        });
        const data = await backendResponse.json();
        res.json(data);
    } catch (error) {
        console.error('Error in chat API:', error);
        res.status(500).send({ error: 'Error in chat API' });
    }
});

// 컬렉션 관리 API 프록시
app.get('/api/collections', async (req, res) => {
    try {
        const backendResponse = await fetch(`${backendApiUrl}/api/collections`);
        const data = await backendResponse.json();
        res.json(data);
    } catch (error) {
        console.error('Error fetching collections:', error);
        res.status(500).send({ error: 'Error fetching collections' });
    }
});

app.get('/api/collections/info', async (req, res) => {
    try {
        const backendResponse = await fetch(`${backendApiUrl}/api/collections/info`);
        const data = await backendResponse.json();
        res.json(data);
    } catch (error) {
        console.error('Error fetching collections info:', error);
        res.status(500).send({ error: 'Error fetching collections info' });
    }
});

app.delete('/api/collections/:collectionName', async (req, res) => {
    try {
        const { collectionName } = req.params;
        const backendResponse = await fetch(`${backendApiUrl}/api/collections/${collectionName}`, {
            method: 'DELETE'
        });
        const data = await backendResponse.json();
        res.json(data);
    } catch (error) {
        console.error('Error deleting collection:', error);
        res.status(500).send({ error: 'Error deleting collection' });
    }
});

app.delete('/api/collections', async (req, res) => {
    try {
        const backendResponse = await fetch(`${backendApiUrl}/api/collections`, {
            method: 'DELETE'
        });
        const data = await backendResponse.json();
        res.json(data);
    } catch (error) {
        console.error('Error deleting all collections:', error);
        res.status(500).send({ error: 'Error deleting all collections' });
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