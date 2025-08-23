// enhanced-tracker.js - Enhanced email tracking with WhatsApp-like read receipts
require('dotenv').config();
const express = require('express');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const sqlite3 = require('sqlite3').verbose();
const config = require('./config');
const googleSheetsService = require('./services/googleSheets');

const app = express();
app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: false }));
app.use(express.json()); // For API endpoints

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Enhanced database schema
const db = new sqlite3.Database(path.join(__dirname, 'mail-tracker.db'), (err) => {
  if (err) {
    console.error('Error opening SQLite database:', err);
  } else {
    console.log('Connected to SQLite database.');
    
    // Enhanced pixels table with campaign support
    db.run(`
      CREATE TABLE IF NOT EXISTS pixels (
        id TEXT PRIMARY KEY,
        name TEXT,
        recipientEmail TEXT,
        campaignId TEXT,
        campaignName TEXT,
        createdAt TEXT,
        status TEXT DEFAULT 'sent'
      )
    `);
    
    // Enhanced logs table
    db.run(`
      CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pixelId TEXT,
        time TEXT,
        ip TEXT,
        userAgent TEXT,
        readType TEXT DEFAULT 'first_read'
      )
    `);
    
    // Campaigns table for bulk email management
    db.run(`
      CREATE TABLE IF NOT EXISTS campaigns (
        id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        totalEmails INTEGER DEFAULT 0,
        sentEmails INTEGER DEFAULT 0,
        openedEmails INTEGER DEFAULT 0,
        createdAt TEXT,
        status TEXT DEFAULT 'active'
      )
    `);
    
    // Add new columns if they don't exist (for existing databases)
    const addColumns = [
      'ALTER TABLE pixels ADD COLUMN campaignId TEXT',
      'ALTER TABLE pixels ADD COLUMN campaignName TEXT', 
      'ALTER TABLE pixels ADD COLUMN status TEXT DEFAULT "sent"',
      'ALTER TABLE logs ADD COLUMN readType TEXT DEFAULT "first_read"'
    ];
    
    addColumns.forEach(sql => {
      db.run(sql, (err) => {
        if (err && !err.message.includes('duplicate column name')) {
          console.error('Error adding column:', err);
        }
      });
    });
  }
});

// Initialize Google Sheets service
googleSheetsService.initialize();

// Middleware for dynamic baseUrl
app.use((req, res, next) => {
  const protocol = req.protocol;
  const host = req.get('host');
  res.locals.baseUrl = `${protocol}://${host}`;
  next();
});

// Helper function to get read receipt status
function getReadReceiptStatus(openCount) {
  if (openCount === 0) return { status: 'sent', ticks: '✓', color: '#999', description: 'Delivered' };
  if (openCount === 1) return { status: 'read', ticks: '✓✓', color: '#4CAF50', description: 'Read' };
  return { status: 'multiple_reads', ticks: '✓✓✓', color: '#2196F3', description: `Read ${openCount} times` };
}

// Enhanced dashboard route with campaign support, pagination, and search
app.get('/', (req, res) => {
  const campaignId = req.query.campaign;
  const search = req.query.search || '';
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 20;
  const offset = (page - 1) * limit;
  
  let pixelQuery = 'SELECT * FROM pixels WHERE 1=1';
  let countQuery = 'SELECT COUNT(*) as total FROM pixels WHERE 1=1';
  let queryParams = [];
  let countParams = [];
  
  if (campaignId) {
    pixelQuery += ' AND campaignId = ?';
    countQuery += ' AND campaignId = ?';
    queryParams.push(campaignId);
    countParams.push(campaignId);
  }
  
  if (search) {
    pixelQuery += ' AND (recipientEmail LIKE ? OR name LIKE ? OR campaignName LIKE ?)';
    countQuery += ' AND (recipientEmail LIKE ? OR name LIKE ? OR campaignName LIKE ?)';
    const searchParam = `%${search}%`;
    queryParams.push(searchParam, searchParam, searchParam);
    countParams.push(searchParam, searchParam, searchParam);
  }
  
  pixelQuery += ' ORDER BY createdAt DESC LIMIT ? OFFSET ?';
  queryParams.push(limit, offset);
  
  // Get total count for pagination
  db.get(countQuery, countParams, (countErr, countResult) => {
    if (countErr) {
      return res.status(500).send('Error counting pixels.');
    }
    
    const totalPixels = countResult.total;
    const totalPages = Math.ceil(totalPixels / limit);
    
    db.all(pixelQuery, queryParams, (err, pixels) => {
      if (err) {
        return res.status(500).send('Error querying pixels.');
      }

      // Get campaigns for dropdown
      db.all('SELECT * FROM campaigns ORDER BY createdAt DESC', [], (campaignErr, campaigns) => {
        if (campaignErr) {
          console.error('Error querying campaigns:', campaignErr);
        }

        // Get stats for each pixel
        const pixelPromises = pixels.map(pixel => {
          return new Promise((resolve) => {
            const logQuery = 'SELECT COUNT(*) as count, MIN(time) as firstOpen, MAX(time) as lastOpen FROM logs WHERE pixelId = ?';
            db.get(logQuery, [pixel.id], (logErr, stats) => {
              if (logErr) {
                resolve({ ...pixel, openCount: 0, readReceipt: getReadReceiptStatus(0) });
              } else {
                const openCount = stats.count || 0;
                resolve({
                  ...pixel,
                  openCount,
                  readReceipt: getReadReceiptStatus(openCount),
                  firstOpen: stats.firstOpen,
                  lastOpen: stats.lastOpen
                });
              }
            });
          });
        });

        Promise.all(pixelPromises).then(pixelsWithStats => {
          res.render('enhanced-index', { 
            pixels: pixelsWithStats, 
            campaigns: campaigns || [],
            selectedCampaign: campaignId,
            search: search,
            pagination: {
              currentPage: page,
              totalPages: totalPages,
              totalPixels: totalPixels,
              limit: limit,
              hasNext: page < totalPages,
              hasPrev: page > 1
            }
          });
        });
      });
    });
  });
});

// Create campaign endpoint
app.post('/create-campaign', (req, res) => {
  const { name, description } = req.body;
  const campaignId = uuidv4();
  const createdAt = new Date().toISOString();

  const insertCampaign = 'INSERT INTO campaigns (id, name, description, createdAt) VALUES (?, ?, ?, ?)';
  db.run(insertCampaign, [campaignId, name, description, createdAt], (err) => {
    if (err) {
      console.error('Error creating campaign:', err);
      return res.status(500).json({ error: 'Error creating campaign' });
    }
    res.json({ success: true, campaignId });
  });
});

// Optimized bulk pixel creation for campaigns
app.post('/create-bulk', async (req, res) => {
  const { campaignId, campaignName, emails } = req.body;
  
  if (!emails || !Array.isArray(emails)) {
    return res.status(400).json({ error: 'Emails array is required' });
  }

  if (emails.length === 0) {
    return res.status(400).json({ error: 'No emails provided' });
  }

  const startTime = Date.now();
  
  const createdPixels = [];
  const createdAt = new Date().toISOString();
  const baseUrl = `${req.protocol}://${req.get('host')}`;

  try {
    // Prepare all data upfront
    const pixelData = [];
    emails.forEach(email => {
      const pixelId = uuidv4();
      const pixelName = `${campaignName || 'Campaign'} - ${email}`;
      
      createdPixels.push({
        pixelId,
        email,
        trackingUrl: `${baseUrl}/tracker/${pixelId}.svg`
      });
      
      pixelData.push([pixelId, pixelName, email, campaignId, campaignName, createdAt, 'sent']);
    });

    // Ultra-fast single-transaction batch insert
    await new Promise((resolve, reject) => {
      const insertSQL = 'INSERT INTO pixels (id, name, recipientEmail, campaignId, campaignName, createdAt, status) VALUES (?, ?, ?, ?, ?, ?, ?)';
      
      db.serialize(() => {
        db.run('BEGIN IMMEDIATE TRANSACTION');
        
        const stmt = db.prepare(insertSQL);
        
        // Insert all at once
        pixelData.forEach(data => stmt.run(data));
        
        stmt.finalize((err) => {
          if (err) {
            db.run('ROLLBACK');
            reject(err);
            return;
          }
          
          db.run('COMMIT', (commitErr) => {
            if (commitErr) {
              reject(commitErr);
            } else {
              resolve();
            }
          });
        });
      });
    });

    // Update campaign stats immediately
    if (campaignId) {
      await new Promise((resolve) => {
        db.run('UPDATE campaigns SET totalEmails = ?, sentEmails = ? WHERE id = ?', 
               [emails.length, emails.length, campaignId], resolve);
      });
    }

    const dbTime = Date.now() - startTime;

    // Respond immediately to user
    res.json({ 
      success: true, 
      created: createdPixels.length,
      pixels: createdPixels,
      dbTime: dbTime
    });

    // Update Google Sheets in background
    if (googleSheetsService.initialized) {
      // Update Google Sheets asynchronously in background
      setTimeout(async () => {
        try {
          const batchSize = 25;
          let processedCount = 0;
          
          for (let i = 0; i < createdPixels.length; i += batchSize) {
            const batch = createdPixels.slice(i, i + batchSize);
            
            // Process batch with error handling
            for (const pixel of batch) {
              try {
                await googleSheetsService.updatePixelData({
                  pixelId: pixel.pixelId,
                  name: `${campaignName || 'Campaign'} - ${pixel.email}`,
                  recipientEmail: pixel.email,
                  status: 'Sent',
                  openCount: 0,
                  createdDate: new Date(createdAt).toLocaleDateString(),
                  campaignName: campaignName || 'Default'
                });
                processedCount++;
              } catch (error) {
                console.error(`Error updating Google Sheets for ${pixel.email}:`, error.message);
              }
            }
            
            // Delay between batches to avoid rate limiting
            if (i + batchSize < createdPixels.length) {
              await new Promise(resolve => setTimeout(resolve, 100));
            }
          }
        } catch (error) {
          console.error('Error in Google Sheets background update:', error);
        }
      }, 100);
    }

  } catch (error) {
    res.status(500).json({ error: 'Error creating bulk pixels: ' + error.message });
  }
});

// Enhanced tracker route with read type detection - now supports SVG
app.get('/tracker/:id.svg', (req, res) => {
  const pixelId = req.params.id;

  // Check if pixel exists
  const selectPixel = 'SELECT * FROM pixels WHERE id = ?';
  db.get(selectPixel, [pixelId], (err, pixel) => {
    if (err) {
      console.error('Error looking up pixel:', err);
      return res.status(500).send('Error retrieving pixel.');
    }
    if (!pixel) {
      return res.status(404).send('Pixel not found');
    }

    // Get previous opens to determine read type
    const selectPreviousLogs = 'SELECT COUNT(*) as count FROM logs WHERE pixelId = ?';
    db.get(selectPreviousLogs, [pixelId], (countErr, countResult) => {
      if (countErr) {
        console.error('Error counting previous opens:', countErr);
      }

      const previousOpens = countResult ? countResult.count : 0;
      let readType = 'first_read';
      
      if (previousOpens === 1) readType = 'second_read';
      else if (previousOpens > 1) readType = 'multiple_read';

      // Log open event with read type
      const time = new Date().toISOString();
      const ip = req.ip;
      const userAgent = req.headers['user-agent'] || '';

      const insertLog = 'INSERT INTO logs (pixelId, time, ip, userAgent, readType) VALUES (?, ?, ?, ?, ?)';
      db.run(insertLog, [pixelId, time, ip, userAgent, readType], async (logErr) => {
        if (logErr) {
          console.error('Error inserting log:', logErr);
        }

        // Update pixel status
        const newStatus = previousOpens === 0 ? 'opened' : 'multiple_opens';
        db.run('UPDATE pixels SET status = ? WHERE id = ?', [newStatus, pixelId]);

        // Update campaign stats if applicable
        if (pixel.campaignId && previousOpens === 0) {
          db.run('UPDATE campaigns SET openedEmails = openedEmails + 1 WHERE id = ?', [pixel.campaignId]);
        }

        // Update Google Sheets with enhanced tracking data
        try {
          const selectAllLogs = 'SELECT * FROM logs WHERE pixelId = ? ORDER BY time ASC';
          db.all(selectAllLogs, [pixelId], async (logsErr, logs) => {
            if (!logsErr && logs.length > 0) {
              const firstOpened = new Date(logs[0].time).toLocaleString();
              const lastOpened = new Date(logs[logs.length - 1].time).toLocaleString();
              const readReceipt = getReadReceiptStatus(logs.length);
              
              await googleSheetsService.updatePixelData({
                pixelId,
                name: pixel.name,
                recipientEmail: pixel.recipientEmail || 'Unknown',
                status: `${readReceipt.ticks} ${readReceipt.description}`,
                firstOpened,
                lastOpened,
                openCount: logs.length,
                createdDate: new Date(pixel.createdAt).toLocaleDateString(),
                campaignName: pixel.campaignName || 'Default'
              });
            }
          });
        } catch (error) {
          console.error('Error updating Google Sheets:', error);
        }

        // Send SVG pixel image
        res.sendFile(path.join(__dirname, 'public', 'images', 'pixel.svg'), (fsErr) => {
          if (fsErr) {
            console.error('Error sending pixel.svg:', fsErr);
            res.status(fsErr.status || 500).end();
          }
        });
      });
    });
  });
});

// Delete single pixel endpoint - Optimized for speed
app.delete('/pixel/:id', async (req, res) => {
  const pixelId = req.params.id;
  
  try {
    // Delete from database first (fast operation)
    await new Promise((resolve, reject) => {
      db.serialize(() => {
        db.run('BEGIN TRANSACTION');
        db.run('DELETE FROM logs WHERE pixelId = ?', [pixelId]);
        db.run('DELETE FROM pixels WHERE id = ?', [pixelId]);
        db.run('COMMIT', (err) => {
          if (err) {
            db.run('ROLLBACK');
            reject(err);
          } else {
            resolve();
          }
        });
      });
    });
    
    // Respond immediately to user
    res.json({ success: true, message: 'Pixel deleted successfully' });
    
    // Delete from Google Sheets asynchronously (non-blocking)
    setImmediate(async () => {
      try {
        await googleSheetsService.deletePixelData(pixelId);
      } catch (error) {
        console.error('Error deleting from Google Sheets (async):', error);
      }
    });
    
  } catch (error) {
    console.error('Error in delete operation:', error);
    res.status(500).json({ error: 'Error deleting pixel' });
  }
});

// Bulk delete pixels endpoint - Optimized for speed
app.delete('/pixels/bulk', async (req, res) => {
  const { pixelIds } = req.body;
  
  if (!pixelIds || !Array.isArray(pixelIds)) {
    return res.status(400).json({ error: 'pixelIds array is required' });
  }
  
  try {
    // Create placeholders for IN clause
    const placeholders = pixelIds.map(() => '?').join(',');
    
    // Delete from database in batch (fast operation)
    await new Promise((resolve, reject) => {
      db.serialize(() => {
        db.run('BEGIN TRANSACTION');
        db.run(`DELETE FROM logs WHERE pixelId IN (${placeholders})`, pixelIds);
        db.run(`DELETE FROM pixels WHERE id IN (${placeholders})`, pixelIds);
        db.run('COMMIT', (err) => {
          if (err) {
            db.run('ROLLBACK');
            reject(err);
          } else {
            resolve();
          }
        });
      });
    });
    
    // Respond immediately to user
    res.json({ 
      success: true, 
      message: `Successfully deleted ${pixelIds.length} pixels`,
      deletedCount: pixelIds.length
    });
    
    // Delete from Google Sheets asynchronously using batch operation (non-blocking)
    setImmediate(async () => {
      try {
        await googleSheetsService.deleteBulkPixelData(pixelIds);
      } catch (error) {
        console.error('Error bulk deleting from Google Sheets (async):', error);
      }
    });
    
  } catch (error) {
    console.error('Error in bulk delete operation:', error);
    res.status(500).json({ error: 'Error performing bulk delete' });
  }
});

// Delete campaign and all its pixels
app.delete('/campaign/:id', async (req, res) => {
  const campaignId = req.params.id;
  
  try {
    // Get all pixels in the campaign
    db.all('SELECT id FROM pixels WHERE campaignId = ?', [campaignId], async (err, pixels) => {
      if (err) {
        return res.status(500).json({ error: 'Error fetching campaign pixels' });
      }
      
      // Delete all pixels and their logs
      for (const pixel of pixels) {
        try {
          await googleSheetsService.deletePixelData(pixel.id);
          await new Promise((resolve) => {
            db.run('DELETE FROM logs WHERE pixelId = ?', [pixel.id], resolve);
          });
        } catch (error) {
          console.error(`Error deleting pixel ${pixel.id}:`, error);
        }
      }
      
      // Delete all pixels in campaign
      db.run('DELETE FROM pixels WHERE campaignId = ?', [campaignId], (pixelErr) => {
        if (pixelErr) {
          return res.status(500).json({ error: 'Error deleting campaign pixels' });
        }
        
        // Delete campaign
        db.run('DELETE FROM campaigns WHERE id = ?', [campaignId], (campaignErr) => {
          if (campaignErr) {
            return res.status(500).json({ error: 'Error deleting campaign' });
          }
          
          res.json({ 
            success: true, 
            message: 'Campaign and all associated pixels deleted successfully',
            deletedPixels: pixels.length
          });
        });
      });
    });
  } catch (error) {
    console.error('Error deleting campaign:', error);
    res.status(500).json({ error: 'Error deleting campaign' });
  }
});



// Campaign analytics endpoint
app.get('/campaign/:id/analytics', (req, res) => {
  const campaignId = req.params.id;
  
  const campaignQuery = 'SELECT * FROM campaigns WHERE id = ?';
  db.get(campaignQuery, [campaignId], (err, campaign) => {
    if (err || !campaign) {
      return res.status(404).json({ error: 'Campaign not found' });
    }

    const pixelsQuery = `
      SELECT p.*, 
             COUNT(l.id) as openCount,
             MIN(l.time) as firstOpen,
             MAX(l.time) as lastOpen
      FROM pixels p 
      LEFT JOIN logs l ON p.id = l.pixelId 
      WHERE p.campaignId = ? 
      GROUP BY p.id
      ORDER BY p.createdAt DESC
    `;
    
    db.all(pixelsQuery, [campaignId], (pixelsErr, pixels) => {
      if (pixelsErr) {
        return res.status(500).json({ error: 'Error fetching campaign data' });
      }

      const analytics = {
        campaign,
        totalEmails: pixels.length,
        openedEmails: pixels.filter(p => p.openCount > 0).length,
        unopenedEmails: pixels.filter(p => p.openCount === 0).length,
        multipleReads: pixels.filter(p => p.openCount > 1).length,
        openRate: pixels.length > 0 ? ((pixels.filter(p => p.openCount > 0).length / pixels.length) * 100).toFixed(2) : 0,
        pixels: pixels.map(p => ({
          ...p,
          readReceipt: getReadReceiptStatus(p.openCount)
        }))
      };

      res.json(analytics);
    });
  });
});

// Enhanced logs route
app.get('/logs/:id', (req, res) => {
  const pixelId = req.params.id;

  const selectPixel = 'SELECT * FROM pixels WHERE id = ?';
  db.get(selectPixel, [pixelId], (err, pixel) => {
    if (err) {
      console.error('Error retrieving pixel:', err);
      return res.status(500).send('Error retrieving pixel.');
    }
    if (!pixel) {
      return res.status(404).send('Pixel not found');
    }

    const selectLogs = 'SELECT * FROM logs WHERE pixelId = ? ORDER BY time DESC';
    db.all(selectLogs, [pixelId], (logsErr, logs) => {
      if (logsErr) {
        console.error('Error retrieving logs:', logsErr);
        return res.status(500).send('Error retrieving logs.');
      }
      
      const readReceipt = getReadReceiptStatus(logs.length);
      res.render('enhanced-logs', { pixel, logs, readReceipt });
    });
  });
});

// Start server
const PORT = process.env.PORT || config.server.port;
app.listen(PORT, () => {
  console.log(`Enhanced Mail Tracker running on port ${PORT}`);
  console.log('Features: WhatsApp-like read receipts, bulk campaigns, advanced analytics');
});