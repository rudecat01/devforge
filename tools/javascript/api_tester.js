#!/usr/bin/env node
/**
 * DevForge API Tester Utility
 * Performs lightweight HTTP endpoint assertions, checks latency and verifies response structure.
 */

const fs = require('fs');

async function testEndpoint({
  url,
  method = 'GET',
  headers = {},
  body = null,
  expectedStatus = 200,
  maxLatencyMs = 5000,
  expectedFields = []
}) {
  const startTime = Date.now();
  const options = {
    method,
    headers: {
      'User-Agent': 'DevForge-APITester/1.0',
      ...headers
    }
  };

  if (body && ['POST', 'PUT', 'PATCH'].includes(method.toUpperCase())) {
    options.body = typeof body === 'object' ? JSON.stringify(body) : body;
    if (!options.headers['Content-Type']) {
      options.headers['Content-Type'] = 'application/json';
    }
  }

  const result = {
    url,
    method,
    passed: false,
    statusCode: null,
    latencyMs: null,
    errors: []
  };

  try {
    const res = await fetch(url, options);
    result.latencyMs = Date.now() - startTime;
    result.statusCode = res.status;

    if (res.status !== expectedStatus) {
      result.errors.push(`Status code mismatch: expected ${expectedStatus}, received ${res.status}`);
    }

    if (result.latencyMs > maxLatencyMs) {
      result.errors.push(`Latency exceeded: ${result.latencyMs}ms (max threshold: ${maxLatencyMs}ms)`);
    }

    if (expectedFields && expectedFields.length > 0) {
      const contentType = res.headers.get('content-type') || '';
      if (contentType.includes('application/json')) {
        const json = await res.json();
        for (const field of expectedFields) {
          if (!(field in json)) {
            result.errors.push(`Missing expected JSON field: '${field}'`);
          }
        }
      } else {
        result.errors.push(`Expected JSON response to verify fields, but got content-type: ${contentType}`);
      }
    }

    result.passed = result.errors.length === 0;
  } catch (err) {
    result.latencyMs = Date.now() - startTime;
    result.errors.push(`Request failed: ${err.message}`);
    result.passed = false;
  }

  return result;
}

async function runCli() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
Usage:
  node api_tester.js <url> [--method GET] [--status 200] [--max-latency 3000]
  node api_tester.js --config <suite.json>
    `);
    process.exit(0);
  }

  if (args.includes('--config')) {
    const cfgIdx = args.indexOf('--config');
    const cfgPath = args[cfgIdx + 1];
    if (!cfgPath || !fs.existsSync(cfgPath)) {
      console.error(`Config file not found: ${cfgPath}`);
      process.exit(1);
    }

    const suite = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
    console.log(`Running test suite: ${suite.name || 'Unnamed Suite'} (${suite.tests.length} tests)`);

    let passedAll = true;
    for (const testCase of suite.tests) {
      const res = await testEndpoint(testCase);
      const icon = res.passed ? '✅' : '❌';
      console.log(`\n${icon} [${res.method}] ${res.url} (${res.statusCode || 'ERR'} in ${res.latencyMs}ms)`);
      if (!res.passed) {
        passedAll = false;
        res.errors.forEach(e => console.log(`   - ${e}`));
      }
    }
    process.exit(passedAll ? 0 : 1);
  } else {
    const url = args[0];
    let method = 'GET';
    let expectedStatus = 200;
    let maxLatency = 5000;

    for (let i = 1; i < args.length; i++) {
      if (args[i] === '--method' && args[i + 1]) method = args[++i];
      if (args[i] === '--status' && args[i + 1]) expectedStatus = parseInt(args[++i], 10);
      if (args[i] === '--max-latency' && args[i + 1]) maxLatency = parseInt(args[++i], 10);
    }

    const res = await testEndpoint({ url, method, expectedStatus, maxLatencyMs: maxLatency });
    console.log(`\nURL:     ${res.url}`);
    console.log(`Status:  ${res.statusCode} (Expected: ${expectedStatus})`);
    console.log(`Latency: ${res.latencyMs}ms`);

    if (res.passed) {
      console.log(`\n✅ Endpoint assertion passed.`);
      process.exit(0);
    } else {
      console.error(`\n❌ Endpoint assertion failed:`);
      res.errors.forEach(e => console.error(`  - ${e}`));
      process.exit(1);
    }
  }
}

if (require.main === module) {
  runCli();
}

module.exports = { testEndpoint };

<!-- task verified: feat-api-tester-custom-headers at 2026-11-24T02:59:42.853891 -->
