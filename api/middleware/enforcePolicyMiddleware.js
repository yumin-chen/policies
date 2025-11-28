const fetch = require('node-fetch');
const { z } = require('zod');

// Define the schema for the template
const TemplateSchema = z.object({
  id: z.string(),
  provenance: z.object({
    created_by: z.string(),
  }),
  bindings: z.array(z.object({
    role: z.string(),
    principal: z.string(),
  })),
  lifecycle: z.object({
    transitions: z.array(z.array(z.string())),
  }),
  spec: z.object({
    kind: z.string(),
    exec: z.string().optional(),
  }),
});

const enforcePolicy = async (req, res, next) => {
  // 1. Validate input schema first
  const validationResult = TemplateSchema.safeParse(req.body);
  if (!validationResult.success) {
    return res.status(400).json({
      error: 'Invalid template schema',
      issues: validationResult.error.errors,
    });
  }

  // 2. Query OPA for a decision
  const opaUrl = process.env.OPA_URL;
  if (!opaUrl) {
    return res.status(500).send('OPA_URL not configured');
  }

  const input = {
    action: 'register_template',
    actor: {
      principal_id: req.headers['x-principal-id'] || 'anonymous',
      roles: (req.headers['x-roles'] || '').split(',').filter(Boolean),
    },
    template: validationResult.data,
  };

  try {
    const response = await fetch(opaUrl, {
      method: 'POST',
      body: JSON.stringify({ input }),
      headers: { 'Content-Type': 'application/json' },
    });
    const decision = await response.json();

    if (decision.result && typeof decision.result.allow === 'boolean' && Array.isArray(decision.result.reasons)) {
        if (decision.result.allow) {
            next();
        } else {
            res.status(403).json({ message: 'Forbidden by policy', reasons: decision.result.reasons });
        }
    } else {
        throw new Error('Invalid OPA decision schema');
    }
  } catch (err) {
    console.error('Error querying OPA:', err);
    res.status(500).send('Internal Server Error');
  }
};

module.exports = enforcePolicy;
