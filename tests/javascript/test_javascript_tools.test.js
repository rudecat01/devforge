const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const { parseEnvFile, validateEnv } = require('../../tools/javascript/env_validator.js');
const { testEndpoint } = require('../../tools/javascript/api_tester.js');

test('parseEnvFile parses key-value pairs correctly', () => {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'devforge-test-'));
  const envFile = path.join(tmpDir, '.env');
  fs.writeFileSync(envFile, 'PORT=3000\n# Comment\nAPP_NAME="DevForge App"\nDEBUG=true\n');

  const parsed = parseEnvFile(envFile);
  assert.strictEqual(parsed.PORT, '3000');
  assert.strictEqual(parsed.APP_NAME, 'DevForge App');
  assert.strictEqual(parsed.DEBUG, 'true');

  fs.rmSync(tmpDir, { recursive: true, force: true });
});

test('validateEnv identifies missing and empty variables', () => {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'devforge-test-'));
  const actualPath = path.join(tmpDir, '.env');
  const examplePath = path.join(tmpDir, '.env.example');

  fs.writeFileSync(examplePath, 'API_KEY=\nDB_HOST=\nPORT=\n');
  fs.writeFileSync(actualPath, 'API_KEY=secret123\nDB_HOST=\n');

  const result = validateEnv(actualPath, examplePath);
  assert.strictEqual(result.valid, false);
  assert.deepStrictEqual(result.missingKeys, ['PORT']);
  assert.deepStrictEqual(result.emptyKeys, ['DB_HOST']);

  fs.rmSync(tmpDir, { recursive: true, force: true });
});

test('testEndpoint returns structured error on invalid network domain', async () => {
  const result = await testEndpoint({
    url: 'http://non-existent-domain-devforge-test-xyz.local',
    maxLatencyMs: 1000
  });

  assert.strictEqual(result.passed, false);
  assert.strictEqual(result.errors.length > 0, true);
});
