const fetch = require('node-fetch');

const enforcePolicy = async (req, res, next) => {
  const opaUrl = process.env.OPA_URL;
  if (!opaUrl) {
    return res.status(500).send('OPA_URL not configured');
  }

  // This is a mock input. A real implementation would construct this from the request.
  const input = {
    action: "register_template",
    actor: {
      principal_id: req.headers['x-principal-id'], // Example header
      roles: (req.headers['x-roles'] || '').split(','), // Example header
    },
    template: req.body,
  };

  try {
    const response = await fetch(opaUrl, {
      method: 'POST',
      body: JSON.stringify({ input }),
      headers: { 'Content-Type': 'application/json' },
    });
    const decision = await response.json();
    if (decision.result && decision.result.allow) {
      next();
    } else {
      res.status(403).json({ message: 'Forbidden by policy', reasons: decision.result ? decision.result.reasons : [] });
    }
  } catch (err) {
    console.error('Error querying OPA:', err);
    res.status(500).send('Internal Server Error');
  }
};

module.exports = enforcePolicy;
