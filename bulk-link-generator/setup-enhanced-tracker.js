#!/usr/bin/env node
/**
 * Enhanced Mail Tracker Setup Script
 * Sets up WhatsApp-style read receipts for bulk email campaigns
 */

const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

console.log('🚀 Setting up Enhanced Mail Tracker with WhatsApp-style Read Receipts...\n');

// Create necessary directories
const dirs = ['public/images', 'views', 'services'];
dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`✅ Created directory: ${dir}`);
    }
});

// Create 1x1 transparent pixel if it doesn't exist
const pixelPath = path.join('public', 'images', 'pixel.svg');
if (!fs.existsSync(pixelPath)) {
    // Create a 1x1 transparent PNG (base64 encoded)
    const transparentPixel = Buffer.from(
        'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==',
        'base64'
    );
    fs.writeFileSync(pixelPath, transparentPixel);
    console.log('✅ Created transparent tracking pixel');
}

// Initialize enhanced database
const dbPath = path.join(__dirname, 'mail-tracker.db');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('❌ Error opening database:', err);
        process.exit(1);
    }
    
    console.log('✅ Connected to SQLite database');
    
    // Create enhanced tables
    const tables = [
        `CREATE TABLE IF NOT EXISTS pixels (
            id TEXT PRIMARY KEY,
            name TEXT,
            recipientEmail TEXT,
            campaignId TEXT,
            campaignName TEXT,
            createdAt TEXT,
            status TEXT DEFAULT 'sent'
        )`,
        `CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pixelId TEXT,
            time TEXT,
            ip TEXT,
            userAgent TEXT,
            readType TEXT DEFAULT 'first_read'
        )`,
        `CREATE TABLE IF NOT EXISTS campaigns (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            totalEmails INTEGER DEFAULT 0,
            sentEmails INTEGER DEFAULT 0,
            openedEmails INTEGER DEFAULT 0,
            createdAt TEXT,
            status TEXT DEFAULT 'active'
        )`
    ];
    
    let completed = 0;
    tables.forEach((sql, index) => {
        db.run(sql, (err) => {
            if (err) {
                console.error(`❌ Error creating table ${index + 1}:`, err);
            } else {
                console.log(`✅ Created/verified table ${index + 1}/3`);
            }
            
            completed++;
            if (completed === tables.length) {
                // Add new columns to existing tables if they don't exist
                const alterQueries = [
                    'ALTER TABLE pixels ADD COLUMN campaignId TEXT',
                    'ALTER TABLE pixels ADD COLUMN campaignName TEXT',
                    'ALTER TABLE pixels ADD COLUMN status TEXT DEFAULT "sent"',
                    'ALTER TABLE logs ADD COLUMN readType TEXT DEFAULT "first_read"'
                ];
                
                let alterCompleted = 0;
                alterQueries.forEach(sql => {
                    db.run(sql, (err) => {
                        if (err && !err.message.includes('duplicate column name')) {
                            console.error('❌ Error adding column:', err);
                        }
                        alterCompleted++;
                        if (alterCompleted === alterQueries.length) {
                            finishSetup();
                        }
                    });
                });
            }
        });
    });
});

function finishSetup() {
    db.close();
    
    console.log('\n🎉 Enhanced Mail Tracker setup completed!\n');
    
    console.log('📋 Next Steps:');
    console.log('1. Install dependencies: npm install');
    console.log('2. Configure Google Sheets (optional):');
    console.log('   - Follow GOOGLE_SHEETS_SETUP.md');
    console.log('   - Set GOOGLE_SHEETS_ID in config.js');
    console.log('3. Start the enhanced tracker: node enhanced-tracker.js');
    console.log('4. Use the Python script for bulk emails: python python-email-sender.py --help');
    
    console.log('\n🔥 Features Available:');
    console.log('✓ Single tick: Email delivered');
    console.log('✓✓ Double tick: Email opened (read)');
    console.log('✓✓✓ Triple tick: Multiple opens (re-read)');
    console.log('📊 Campaign management');
    console.log('📈 Real-time analytics');
    console.log('📋 Google Sheets integration');
    console.log('🐍 Python bulk email script');
    
    console.log('\n🌐 Access your dashboard at: http://localhost:3300');
}