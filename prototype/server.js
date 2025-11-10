// YSenseAI Attribution Engine v0.1-pilot
// Minimal Working Prototype for Academic Validation
// Apache 2.0 License - Alton Lee Wei Bin

const express = require('express');
const crypto = require('crypto');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
app.use(express.json());
app.use(cors({
    origin: '*',
    methods: ['GET', 'POST', 'PATCH'],
    credentials: true
}));

// Serve the index.html file
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// In-memory storage (with persistence)
const attributions = new Map();
const creators = new Map();
const consents = new Map();

// Z Protocol Consent Levels
const Z_PROTOCOL = {
  PUBLIC: 'public',        // Freely usable
  PERSONAL: 'personal',    // Personal use only  
  CULTURAL: 'cultural',    // Cultural sensitivity required
  SACRED: 'sacred',        // Restricted access
  THERAPEUTIC: 'therapeutic' // Mental health context
};

// Data persistence functions
function saveData() {
  try {
    const data = {
      creators: Array.from(creators.entries()),
      attributions: Array.from(attributions.entries()),
      timestamp: new Date().toISOString()
    };
    fs.writeFileSync('ysense-data.json', JSON.stringify(data, null, 2));
    console.log('Data saved successfully');
  } catch (error) {
    console.error('Error saving data:', error);
  }
}

function loadData() {
  try {
    if (fs.existsSync('ysense-data.json')) {
      const data = JSON.parse(fs.readFileSync('ysense-data.json', 'utf8'));
      creators.clear();
      attributions.clear();
      data.creators.forEach(([id, creator]) => creators.set(id, creator));
      data.attributions.forEach(([id, attr]) => attributions.set(id, attr));
      console.log(`Loaded ${creators.size} creators, ${attributions.size} attributions`);
    }
  } catch (error) {
    console.log('No existing data found, starting fresh');
  }
}

// Load data on startup
loadData();

// Generate unique IDs
function generateId() {
  return crypto.randomBytes(16).toString('hex');
}

// Hash content for integrity
function hashContent(content) {
  return crypto.createHash('sha256').update(content).digest('hex');
}

// Create attribution record
function createAttribution(data) {
  const attribution = {
    id: generateId(),
    contentHash: hashContent(data.content),
    creatorId: data.creatorId,
    timestamp: new Date().toISOString(),
    metadata: {
      title: data.title || 'Untitled',
      description: data.description || '',
      contentType: data.contentType || 'text',
      language: data.language || 'en',
      culturalContext: data.culturalContext || null
    },
    consent: {
      level: data.consentLevel || Z_PROTOCOL.PERSONAL,
      allowAI: data.allowAI || false,
      allowCommercial: data.allowCommercial || false,
      attribution: data.attributionRequired !== false,
      expiry: data.consentExpiry || null
    },
    verification: {
      version: 'z-protocol-v0.1',
      signature: null,
      witnesses: []
    },
    stats: {
      views: 0,
      uses: 0,
      revenue: 0
    }
  };
  
  return attribution;
}

// API status endpoint
app.get('/api/status', (req, res) => {
  res.json({
    service: 'YSenseAI Attribution Engine',
    version: '0.1-pilot',
    status: 'operational',
    protocol: 'Z Protocol v0.1',
    documentation: 'https://github.com/Creator35LWB/YSenseAI-AI-Attribution-Infrastructure'
  });
});

// Register creator (with duplicate check)
app.post('/api/creators', (req, res) => {
  const { name, email, culturalAffiliation } = req.body;
  
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email required' });
  }
  
  // Check if email already exists
  const existingCreator = Array.from(creators.values())
    .find(c => c.email.toLowerCase() === email.toLowerCase());
  
  if (existingCreator) {
    // Return existing creator ID instead of creating duplicate
    return res.status(200).json({
      message: 'Creator already registered',
      creatorId: existingCreator.id,
      profile: existingCreator,
      existing: true
    });
  }
  
  // Create new creator only if email doesn't exist
  const creator = {
    id: generateId(),
    name,
    email: email.toLowerCase(),
    culturalAffiliation: culturalAffiliation || null,
    registered: new Date().toISOString(),
    stats: {
      contributions: 0,
      totalRevenue: 0
    }
  };
  
  creators.set(creator.id, creator);
  saveData(); // Save after adding creator
  
  res.status(201).json({
    message: 'Creator registered',
    creatorId: creator.id,
    profile: creator,
    existing: false
  });
});

// Create attribution
app.post('/api/attributions', (req, res) => {
  const { creatorId, content, title, consentLevel, allowAI, allowCommercial } = req.body;
  
  if (!creatorId || !content) {
    return res.status(400).json({ error: 'Creator ID and content required' });
  }
  
  if (!creators.has(creatorId)) {
    return res.status(404).json({ error: 'Creator not found' });
  }
  
  const attribution = createAttribution(req.body);
  attributions.set(attribution.id, attribution);
  
  // Update creator stats
  const creator = creators.get(creatorId);
  creator.stats.contributions++;
  
  saveData(); // Save after adding attribution
  
  res.status(201).json({
    message: 'Attribution created',
    attributionId: attribution.id,
    contentHash: attribution.contentHash,
    timestamp: attribution.timestamp,
    consent: attribution.consent
  });
});

// Verify attribution
app.get('/api/attributions/verify/:hash', (req, res) => {
  const { hash } = req.params;
  
  const attribution = Array.from(attributions.values())
    .find(a => a.contentHash === hash);
  
  if (!attribution) {
    return res.status(404).json({ 
      verified: false,
      error: 'No attribution found for this content' 
    });
  }
  
  const creator = creators.get(attribution.creatorId);
  
  res.json({
    verified: true,
    attribution: {
      id: attribution.id,
      creator: creator.name,
      timestamp: attribution.timestamp,
      consent: attribution.consent,
      metadata: attribution.metadata
    }
  });
});

// Get attribution by ID
app.get('/api/attributions/:id', (req, res) => {
  const attribution = attributions.get(req.params.id);
  
  if (!attribution) {
    return res.status(404).json({ error: 'Attribution not found' });
  }
  
  // Increment view count
  attribution.stats.views++;
  saveData();
  
  const creator = creators.get(attribution.creatorId);
  
  res.json({
    attribution,
    creator: {
      name: creator.name,
      culturalAffiliation: creator.culturalAffiliation
    }
  });
});

// Update consent
app.patch('/api/attributions/:id/consent', (req, res) => {
  const attribution = attributions.get(req.params.id);
  
  if (!attribution) {
    return res.status(404).json({ error: 'Attribution not found' });
  }
  
  const { level, allowAI, allowCommercial } = req.body;
  
  if (level) attribution.consent.level = level;
  if (typeof allowAI === 'boolean') attribution.consent.allowAI = allowAI;
  if (typeof allowCommercial === 'boolean') attribution.consent.allowCommercial = allowCommercial;
  
  attribution.consent.updated = new Date().toISOString();
  saveData();
  
  res.json({
    message: 'Consent updated',
    consent: attribution.consent
  });
});

// Track usage (for AI training)
app.post('/api/attributions/:id/usage', (req, res) => {
  const attribution = attributions.get(req.params.id);
  
  if (!attribution) {
    return res.status(404).json({ error: 'Attribution not found' });
  }
  
  if (!attribution.consent.allowAI) {
    return res.status(403).json({ 
      error: 'AI usage not permitted for this content' 
    });
  }
  
  const { purpose, organization, model } = req.body;
  
  const usage = {
    id: generateId(),
    attributionId: req.params.id,
    timestamp: new Date().toISOString(),
    purpose: purpose || 'training',
    organization: organization || 'unknown',
    model: model || 'unknown'
  };
  
  attribution.stats.uses++;
  saveData();
  
  res.json({
    message: 'Usage tracked',
    usageId: usage.id,
    attribution: {
      required: attribution.consent.attribution,
      creator: creators.get(attribution.creatorId).name,
      terms: attribution.consent
    }
  });
});

// Get statistics
app.get('/api/stats', (req, res) => {
  res.json({
    totalCreators: creators.size,
    totalAttributions: attributions.size,
    totalViews: Array.from(attributions.values())
      .reduce((sum, a) => sum + a.stats.views, 0),
    totalUses: Array.from(attributions.values())
      .reduce((sum, a) => sum + a.stats.uses, 0),
    consentBreakdown: {
      public: Array.from(attributions.values())
        .filter(a => a.consent.level === Z_PROTOCOL.PUBLIC).length,
      personal: Array.from(attributions.values())
        .filter(a => a.consent.level === Z_PROTOCOL.PERSONAL).length,
      cultural: Array.from(attributions.values())
        .filter(a => a.consent.level === Z_PROTOCOL.CULTURAL).length
    }
  });
});

// Five-Layer Perception Toolkit endpoint
app.post('/api/perception', (req, res) => {
  const { creatorId, layers } = req.body;
  
  if (!creatorId || !layers) {
    return res.status(400).json({ error: 'Creator ID and layers required' });
  }
  
  const perception = {
    id: generateId(),
    creatorId,
    timestamp: new Date().toISOString(),
    layers: {
      narrative: layers.narrative || null,
      somatic: layers.somatic || null,
      attention: layers.attention || null,
      synesthetic: layers.synesthetic || null,
      temporal: layers.temporal || null
    },
    analysis: {
      completeness: Object.values(layers).filter(l => l !== null).length / 5,
      culturalRelevance: layers.narrative?.includes('cultural') || false,
      aiReadiness: Object.values(layers).filter(l => l !== null).length >= 3
    }
  };
  
  res.json({
    message: 'Perception data captured',
    perceptionId: perception.id,
    analysis: perception.analysis
  });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════╗
║   YSenseAI Attribution Engine v0.1       ║
║   Z Protocol Implementation (Pilot)    ║
║                                        ║
║   Status: RUNNING                      ║
║   Port: ${PORT}                            ║
║   DOI: 10.5281/zenodo.17072168       ║
╚════════════════════════════════════════╝
  
API Endpoints:
- POST /api/creators           Register creator
- POST /api/attributions       Create attribution  
- GET  /api/attributions/:id   Get attribution
- GET  /api/attributions/verify/:hash  Verify content
- PATCH /api/attributions/:id/consent  Update consent
- POST /api/attributions/:id/usage     Track usage
- POST /api/perception         Five-Layer data
- GET  /api/stats             Platform statistics

Open browser at: http://localhost:${PORT}
  `);
});
