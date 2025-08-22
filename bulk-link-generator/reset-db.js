#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

const dbPath = path.join(__dirname, 'mail-tracker.db');

console.log('🔄 Resetting Mail Tracker Database...\n');

// Delete existing database
if (fs.existsSync(dbPath)) {
  fs.unlinkSync(dbPath);
  console.log('✅ Deleted existing database');
}

// Create new database with correct schema
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('❌ Error creating database:', err);
    process.exit(1);
  } else {
    console.log('✅ Created new database');
    
    // Create pixels table with recipientEmail column
    db.run(`
      CREATE TABLE pixels (
        id TEXT PRIMARY KEY,
        name TEXT,
        recipientEmail TEXT,
        createdAt TEXT
      )
    `, (err) => {
      if (err) {
        console.error('❌ Error creating pixels table:', err);
      } else {
        console.log('✅ Created pixels table');
      }
    });

    // Create logs table
    db.run(`
      CREATE TABLE logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pixelId TEXT,
        time TEXT,
        ip TEXT,
        userAgent TEXT
      )
    `, (err) => {
      if (err) {
        console.error('❌ Error creating logs table:', err);
      } else {
        console.log('✅ Created logs table');
      }
      
      db.close((err) => {
        if (err) {
          console.error('❌ Error closing database:', err);
        } else {
          console.log('\n🎉 Database reset complete!');
          console.log('You can now start your application with: npm start');
        }
      });
    });
  }
});