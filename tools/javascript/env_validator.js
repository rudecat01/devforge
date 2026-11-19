#!/usr/bin/env node
/**
 * DevForge Environment Validator
 * Validates .env files against .env.example or schema rules, checking for missing or malformed keys.
 */

const fs = require('fs');
const path = require('path');

function parseEnvFile(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }
  const content = fs.readFileSync(filePath, 'utf-8');
  const env = {};
  const lines = content.split('\n');

  for (let line of lines) {
    line = line.trim();
    if (!line || line.startsWith('#')) continue;

    const eqIdx = line.indexOf('=');
    if (eqIdx === -1) continue;

    const key = line.slice(0, eqIdx).trim();
    let val = line.slice(eqIdx + 1).trim();

    // Strip surrounding quotes
    if (
      (val.startsWith('"') && val.endsWith('"')) ||
      (val.startsWith("'") && val.endsWith("'"))
    ) {
      val = val.slice(1, -1);
    }

    env[key] = val;
  }
  return env;
}

function validateEnv(envPath, examplePath) {
  const actualEnv = parseEnvFile(envPath);
  const templateEnv = parseEnvFile(examplePath);

  const missingKeys = [];
  const emptyKeys = [];
  const extraKeys = [];

  for (const key of Object.keys(templateEnv)) {
    if (!(key in actualEnv)) {
      missingKeys.push(key);
    } else if (!actualEnv[key] && actualEnv[key] !== '0' && actualEnv[key] !== 'false') {
      emptyKeys.push(key);
    }
  }

  for (const key of Object.keys(actualEnv)) {
    if (!(key in templateEnv)) {
      extraKeys.push(key);
    }
  }

  return {
    valid: missingKeys.length === 0,
    missingKeys,
    emptyKeys,
    extraKeys,
    totalExpected: Object.keys(templateEnv).length,
    totalConfigured: Object.keys(actualEnv).length
  };
}

function runCli() {
  const args = process.argv.slice(2);
  let envFile = '.env';
  let exampleFile = '.env.example';

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--env' && args[i + 1]) {
      envFile = args[++i];
    } else if (args[i] === '--example' && args[i + 1]) {
      exampleFile = args[++i];
    } else if (args[i] === '--help' || args[i] === '-h') {
      console.log('Usage: node env_validator.js [--env .env] [--example .env.example]');
      process.exit(0);
    }
  }

  try {
    const result = validateEnv(envFile, exampleFile);

    console.log(`\n=== DevForge Environment Validation ===`);
    console.log(`Target:   ${path.resolve(envFile)}`);
    console.log(`Template: ${path.resolve(exampleFile)}\n`);

    if (result.missingKeys.length > 0) {
      console.error(`❌ Missing required variables (${result.missingKeys.length}):`);
      result.missingKeys.forEach(k => console.error(`   - ${k}`));
    }

    if (result.emptyKeys.length > 0) {
      console.warn(`⚠️  Variables with empty values (${result.emptyKeys.length}):`);
      result.emptyKeys.forEach(k => console.warn(`   - ${k}`));
    }

    if (result.extraKeys.length > 0) {
      console.log(`ℹ️  Extra variables not in template (${result.extraKeys.length}):`);
      result.extraKeys.forEach(k => console.log(`   - ${k}`));
    }

    if (result.valid) {
      console.log(`\n✅ All required environment variables are defined (${result.totalConfigured}/${result.totalExpected}).`);
      process.exit(0);
    } else {
      console.error(`\n❌ Validation failed: Missing required environment variables.`);
      process.exit(1);
    }
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  runCli();
}

module.exports = { parseEnvFile, validateEnv };
