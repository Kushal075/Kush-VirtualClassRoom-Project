// server.js

const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// SQLite database setup
const dbPath = path.resolve(__dirname, 'blood-donation.db');
const db = new sqlite3.Database(dbPath);

// Middleware setup
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'register.html'));
});

app.get('/search', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'search.html'));
});

app.get('/success', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'success.html'));
});

// Register donor endpoint
app.post('/register', (req, res) => {
    const { firstName, lastName, email, phone, bloodGroup, country, state, city, district } = req.body;
    const query = `INSERT INTO donors (firstName, lastName, email, phone, bloodGroup, country, state, city, district) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`;
    db.run(query, [firstName, lastName, email, phone, bloodGroup, country, state, city, district], (err) => {
        if (err) {
            console.error(err.message);
            res.json({ success: false });
        } else {
            res.redirect('/success');
        }
    });
});

// Search donors endpoint
app.post('/search', (req, res) => {
    const { country, state, city, district } = req.body;
    const query = `SELECT * FROM donors WHERE country = ? AND state = ? AND city = ? AND district = ?`;
    db.all(query, [country, state, city, district], (err, rows) => {
        if (err) {
            console.error(err.message);
            res.json([]);
        } else {
            res.json(rows);
        }
    });
});

// Create donors table if not exists
db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY,
        firstName TEXT,
        lastName TEXT,
        email TEXT,
        phone TEXT,
        bloodGroup TEXT,
        country TEXT,
        state TEXT,
        city TEXT,
        district TEXT
    )`);
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
