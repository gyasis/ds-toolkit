#!/usr/bin/env node
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import { program } from 'commander';
import snowflake from 'snowflake-sdk';
import inquirer from 'inquirer';
import { getAllAccounts, createPackage, decryptData, setSecurePermissions, getCrossPlatformKeyDir } from './utils.js';

// Modify the key directory handling to support multiple accounts
function getKeyPaths(account = 'default') {
  const BASE_KEY_DIR = getCrossPlatformKeyDir();
  const accountKeyDir = path.join(BASE_KEY_DIR, account);
  return {
    keyDir: accountKeyDir,
    privateKeyPath: path.join(accountKeyDir, 'private_key.pem'),
    publicKeyPath: path.join(accountKeyDir, 'public_key.pem')
  };
}

function ensureKeyDir(account = 'default') {
  const { keyDir } = getKeyPaths(account);
  if (!fs.existsSync(keyDir)) {
    fs.mkdirSync(keyDir, { recursive: true, mode: 0o700 });
  }
}

function generateKeys(account = 'default') {
  ensureKeyDir(account);
  const { privateKeyPath, publicKeyPath } = getKeyPaths(account);
  
  const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: 4096,
    publicKeyEncoding: { type: 'spki', format: 'pem' },
    privateKeyEncoding: { type: 'pkcs8', format: 'pem' }
  });

  fs.writeFileSync(privateKeyPath, privateKey, { mode: 0o600 });
  const snowflakePublic = publicKey
    .replace(/-----BEGIN PUBLIC KEY-----/g, '')
    .replace(/-----END PUBLIC KEY-----/g, '')
    .replace(/\n/g, '');
  
  fs.writeFileSync(publicKeyPath, snowflakePublic);
  return snowflakePublic;
}

function createEnvFile() {
  const envContent = `# Snowflake Connection Parameters
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USERNAME=your_username
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_ROLE=your_role

# Key Paths
PRIVATE_KEY_PATH=${PRIVATE_KEY_PATH}
PUBLIC_KEY_PATH=${PUBLIC_KEY_PATH}
`;

  const envPath = path.join(process.cwd(), '.env');
  fs.writeFileSync(envPath, envContent, { mode: 0o600 });
  return envPath;
}

function getKeyAge(keyPath) {
  try {
    const stats = fs.statSync(keyPath);
    const ageInDays = (Date.now() - stats.mtime.getTime()) / (1000 * 60 * 60 * 24);
    return ageInDays;
  } catch (error) {
    return null; // Key doesn't exist
  }
}

program
  .name('skm')
  .description('Snowflake Key Manager - A CLI tool for managing Snowflake key pairs')
  .version('1.0.0');

program
  .command('generate')
  .description('Generate new key pair')
  .argument('[account]', 'Snowflake account name (default: "default")')
  .action((account) => {
    const publicKey = generateKeys(account);
    console.log(`Keys generated for account "${account || 'default'}" in ~/.pem_1/${account || 'default'}`);
    console.log('\nSnowflake SQL:');
    console.log(`ALTER USER ${account || 'default'} SET RSA_PUBLIC_KEY = '${publicKey}';`);
  });

program
  .command('rotate')
  .description('Manually rotate keys (only if older than 90 days or --force flag is used)')
  .argument('[account]', 'Snowflake account name (default: "default")')
  .option('-f, --force', 'Force key rotation regardless of age')
  .action((account, options) => {
    const { privateKeyPath, keyDir } = getKeyPaths(account);
    const keyAge = getKeyAge(privateKeyPath);
    
    if (!fs.existsSync(privateKeyPath)) {
      console.log(`No existing keys found for account "${account || 'default'}". Use "skm generate ${account || ''}" to create new keys.`);
      return;
    }

    if (!options.force && keyAge && keyAge < 90) {
      console.log(`Current keys for account "${account || 'default'}" are only ${Math.round(keyAge)} days old.`);
      console.log('Keys should only be rotated after 90 days for security best practices.');
      console.log('Use --force flag to override this check if necessary.');
      return;
    }

    const timestamp = Date.now();
    const backupPath = path.join(keyDir, `private_key_${timestamp}.pem.bak`);
    
    fs.copyFileSync(privateKeyPath, backupPath);
    const publicKey = generateKeys(account);
    
    console.log(`Keys rotated for account "${account || 'default'}"! Old key backed up to:`, backupPath);
    console.log('\nUpdate Snowflake with new public key:');
    console.log(`ALTER USER ${account || 'default'} SET RSA_PUBLIC_KEY = '${publicKey}';`);
  });

program
  .command('show-public')
  .description('Show current public key')
  .argument('[account]', 'Snowflake account name (default: "default")')
  .action((account) => {
    const { publicKeyPath } = getKeyPaths(account);
    if (fs.existsSync(publicKeyPath)) {
      console.log(fs.readFileSync(publicKeyPath, 'utf8'));
    } else {
      console.log(`No public key found for account "${account || 'default'}". Run "skm generate ${account || ''}" first.`);
    }
  });

program
  .command('init-env')
  .description('Create a new .env file with Snowflake configuration template')
  .action(() => {
    try {
      const envPath = createEnvFile();
      console.log('✅ Created .env file at:', envPath);
      console.log('\nPlease update the file with your Snowflake credentials.');
      console.log('Make sure to keep this file secure and never commit it to version control.');
    } catch (error) {
      console.error('❌ Error creating .env file:', error.message);
      process.exit(1);
    }
  });

program
  .command('key-paths')
  .description('Show the paths of the private and public key files')
  .argument('[account]', 'Snowflake account name (default: "default")')
  .action((account) => {
    const { privateKeyPath, publicKeyPath, keyDir } = getKeyPaths(account);
    console.log({
      privateKeyPath,
      publicKeyPath,
      keyDirectory: keyDir
    });
  });

// Add a new command to check key age
program
  .command('key-age')
  .description('Check the age of current keys')
  .action(() => {
    const keyAge = getKeyAge(PRIVATE_KEY_PATH);
    
    if (!keyAge) {
      console.log('No existing keys found. Use "skm generate" to create new keys.');
      return;
    }

    const daysLeft = 90 - keyAge;
    console.log(`Current keys are ${Math.round(keyAge)} days old.`);
    
    if (daysLeft > 0) {
      console.log(`Recommended rotation in ${Math.round(daysLeft)} days.`);
    } else {
      console.log('Keys are due for rotation. Please run "skm rotate" to generate new keys.');
    }
  });

program
  .command('list-accounts')
  .description('List all accounts with key pairs')
  .action(() => {
    const accounts = getAllAccounts();
    
    if (accounts.length === 0) {
      console.log('No accounts found. Generate keys for an account using "skm generate <account>"');
      return;
    }

    console.log('Accounts with key pairs:');
    accounts.forEach(account => {
      const { privateKeyPath } = getKeyPaths(account);
      const keyAge = getKeyAge(privateKeyPath);
      console.log(`- ${account} (${Math.round(keyAge)} days old)`);
    });
  });

program
  .command('mirror-all')
  .description('Export or import all account keys as encrypted package')
  .argument('[direction]', 'Direction: export or import')
  .option('-o, --output <path>', 'Output file path for export')
  .option('-i, --input <path>', 'Input file path for import')
  .option('-f, --force', 'Overwrite existing keys on import')
  .action(async (direction, options) => {
    try {
      if (!direction) {
        const { selectedDirection } = await inquirer.prompt([
          {
            type: 'list',
            name: 'selectedDirection',
            message: 'Select transfer direction:',
            choices: ['export', 'import']
          }
        ]);
        direction = selectedDirection;
      }

      if (direction === 'export') {
        await handleMirrorExport(options);
      } else if (direction === 'import') {
        await handleMirrorImport(options);
      } else {
        console.log('Invalid direction. Use "export" or "import".');
        process.exit(1);
      }
    } catch (error) {
      console.error('❌ Mirror operation failed:', error.message);
      process.exit(1);
    }
  });

program
  .command('mirror-account')
  .description('Export or import single account keys as encrypted package')
  .argument('<account>', 'Account name to export/import')
  .argument('[direction]', 'Direction: export or import')
  .option('-o, --output <path>', 'Output file path for export')
  .option('-i, --input <path>', 'Input file path for import')
  .option('-f, --force', 'Overwrite existing keys on import')
  .action(async (account, direction, options) => {
    try {
      if (!direction) {
        const { selectedDirection } = await inquirer.prompt([
          {
            type: 'list',
            name: 'selectedDirection',
            message: 'Select transfer direction:',
            choices: ['export', 'import']
          }
        ]);
        direction = selectedDirection;
      }

      if (direction === 'export') {
        await handleMirrorAccountExport(account, options);
      } else if (direction === 'import') {
        await handleMirrorAccountImport(account, options);
      } else {
        console.log('Invalid direction. Use "export" or "import".');
        process.exit(1);
      }
    } catch (error) {
      console.error('❌ Mirror account operation failed:', error.message);
      process.exit(1);
    }
  });

async function handleMirrorAccountExport(account, options) {
  const { privateKeyPath, publicKeyPath } = getKeyPaths(account);
  
  if (!fs.existsSync(privateKeyPath)) {
    console.log(`❌ No keys found for account "${account}". Generate keys first using "skm generate ${account}"`);
    return;
  }

  console.log(`Exporting keys for account: ${account}`);

  const { password } = await inquirer.prompt([
    {
      type: 'password',
      name: 'password',
      message: '🔐 Enter encryption password:',
      mask: '*',
      validate: input => input.length >= 8 || 'Password must be at least 8 characters'
    }
  ]);

  const { confirmPassword } = await inquirer.prompt([
    {
      type: 'password',
      name: 'confirmPassword',
      message: '🔐 Confirm encryption password:',
      mask: '*',
      validate: input => input === password || 'Passwords do not match'
    }
  ]);

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const defaultOutput = `skm-${account}-${timestamp}.skm`;
  
  let outputPath = options.output;
  if (!outputPath) {
    const { selectedOutput } = await inquirer.prompt([
      {
        type: 'input',
        name: 'selectedOutput',
        message: '📁 Output file path:',
        default: defaultOutput
      }
    ]);
    outputPath = selectedOutput;
  }

  console.log('🔒 Encrypting keys...');
  const encryptedPackage = createPackage([account], password);
  
  fs.writeFileSync(outputPath, JSON.stringify(encryptedPackage, null, 2));
  setSecurePermissions(outputPath);
  
  console.log(`✅ Exported account "${account}" to: ${outputPath}`);
  console.log('🔐 Keep this file and password secure!');
}

async function handleMirrorAccountImport(account, options) {
  let inputPath = options.input;
  if (!inputPath) {
    const { selectedInput } = await inquirer.prompt([
      {
        type: 'input',
        name: 'selectedInput',
        message: '📁 Package file path:',
        validate: input => fs.existsSync(input) || 'File does not exist'
      }
    ]);
    inputPath = selectedInput;
  }

  if (!fs.existsSync(inputPath)) {
    console.log('❌ Package file not found:', inputPath);
    return;
  }

  const { password } = await inquirer.prompt([
    {
      type: 'password',
      name: 'password',
      message: '🔐 Enter decryption password:',
      mask: '*'
    }
  ]);

  console.log('🔓 Decrypting package...');
  
  try {
    const encryptedData = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
    const packageData = decryptData(encryptedData, password);
    
    if (!packageData.accounts[account]) {
      console.log(`❌ Account "${account}" not found in package file`);
      console.log(`📦 Available accounts: ${Object.keys(packageData.accounts).join(', ')}`);
      return;
    }

    console.log(`📦 Package contains account: ${account}`);
    console.log(`📅 Created: ${packageData.timestamp}`);
    console.log(`💻 Platform: ${packageData.platform_created}`);
    
    const { privateKeyPath } = getKeyPaths(account);
    const accountExists = fs.existsSync(privateKeyPath);

    if (accountExists && !options.force) {
      console.log(`⚠️  Account "${account}" already exists`);
      const { confirmOverwrite } = await inquirer.prompt([
        {
          type: 'confirm',
          name: 'confirmOverwrite',
          message: 'Overwrite existing keys?',
          default: false
        }
      ]);
      
      if (!confirmOverwrite) {
        console.log('Import cancelled');
        return;
      }
    }

    const { keyDir, publicKeyPath } = getKeyPaths(account);
    const accountData = packageData.accounts[account];
    
    if (!fs.existsSync(keyDir)) {
      fs.mkdirSync(keyDir, { recursive: true, mode: 0o700 });
    }
    
    fs.writeFileSync(privateKeyPath, accountData.private_key);
    fs.writeFileSync(publicKeyPath, accountData.public_key);
    
    setSecurePermissions(privateKeyPath, true);
    setSecurePermissions(publicKeyPath, false);
    
    console.log(`✅ Successfully imported account: ${account}`);
    
  } catch (error) {
    if (error.message.includes('bad decrypt')) {
      console.log('❌ Invalid password or corrupted package file');
    } else {
      console.log('❌ Failed to decrypt package:', error.message);
    }
    process.exit(1);
  }
}

async function handleMirrorExport(options) {
  const accounts = getAllAccounts();
  
  if (accounts.length === 0) {
    console.log('No accounts found to export. Generate keys first using "skm generate <account>"');
    return;
  }

  console.log(`Found ${accounts.length} account(s): ${accounts.join(', ')}`);

  const { password } = await inquirer.prompt([
    {
      type: 'password',
      name: 'password',
      message: '🔐 Enter encryption password:',
      mask: '*',
      validate: input => input.length >= 8 || 'Password must be at least 8 characters'
    }
  ]);

  const { confirmPassword } = await inquirer.prompt([
    {
      type: 'password',
      name: 'confirmPassword',
      message: '🔐 Confirm encryption password:',
      mask: '*',
      validate: input => input === password || 'Passwords do not match'
    }
  ]);

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const defaultOutput = `skm-backup-${timestamp}.skm`;
  
  let outputPath = options.output;
  if (!outputPath) {
    const { selectedOutput } = await inquirer.prompt([
      {
        type: 'input',
        name: 'selectedOutput',
        message: '📁 Output file path:',
        default: defaultOutput
      }
    ]);
    outputPath = selectedOutput;
  }

  console.log('🔒 Encrypting keys...');
  const encryptedPackage = createPackage(accounts, password);
  
  fs.writeFileSync(outputPath, JSON.stringify(encryptedPackage, null, 2));
  setSecurePermissions(outputPath);
  
  console.log(`✅ Exported ${accounts.length} account(s) to: ${outputPath}`);
  console.log('🔐 Keep this file and password secure!');
}

async function handleMirrorImport(options) {
  let inputPath = options.input;
  if (!inputPath) {
    const { selectedInput } = await inquirer.prompt([
      {
        type: 'input',
        name: 'selectedInput',
        message: '📁 Package file path:',
        validate: input => fs.existsSync(input) || 'File does not exist'
      }
    ]);
    inputPath = selectedInput;
  }

  if (!fs.existsSync(inputPath)) {
    console.log('❌ Package file not found:', inputPath);
    return;
  }

  const { password } = await inquirer.prompt([
    {
      type: 'password',
      name: 'password',
      message: '🔐 Enter decryption password:',
      mask: '*'
    }
  ]);

  console.log('🔓 Decrypting package...');
  
  try {
    const encryptedData = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
    const packageData = decryptData(encryptedData, password);
    
    console.log(`📦 Package contains ${Object.keys(packageData.accounts).length} account(s)`);
    console.log(`📅 Created: ${packageData.timestamp}`);
    console.log(`💻 Platform: ${packageData.platform_created}`);
    
    const accountNames = Object.keys(packageData.accounts);
    const existingAccounts = accountNames.filter(account => {
      const { privateKeyPath } = getKeyPaths(account);
      return fs.existsSync(privateKeyPath);
    });

    if (existingAccounts.length > 0 && !options.force) {
      console.log(`⚠️  Existing accounts found: ${existingAccounts.join(', ')}`);
      const { confirmOverwrite } = await inquirer.prompt([
        {
          type: 'confirm',
          name: 'confirmOverwrite',
          message: 'Overwrite existing keys?',
          default: false
        }
      ]);
      
      if (!confirmOverwrite) {
        console.log('Import cancelled');
        return;
      }
    }

    let importedCount = 0;
    for (const [account, accountData] of Object.entries(packageData.accounts)) {
      const { keyDir, privateKeyPath, publicKeyPath } = getKeyPaths(account);
      
      if (!fs.existsSync(keyDir)) {
        fs.mkdirSync(keyDir, { recursive: true, mode: 0o700 });
      }
      
      fs.writeFileSync(privateKeyPath, accountData.private_key);
      fs.writeFileSync(publicKeyPath, accountData.public_key);
      
      setSecurePermissions(privateKeyPath, true);
      setSecurePermissions(publicKeyPath, false);
      
      importedCount++;
      console.log(`✅ Imported: ${account}`);
    }

    console.log(`🎉 Successfully imported ${importedCount} account(s)`);
    
  } catch (error) {
    if (error.message.includes('bad decrypt')) {
      console.log('❌ Invalid password or corrupted package file');
    } else {
      console.log('❌ Failed to decrypt package:', error.message);
    }
    process.exit(1);
  }
}

// Add help examples
program.on('--help', () => {
  console.log('');
  console.log('Commands:');
  console.log('  generate [account]     Generate new key pair for specified account');
  console.log('  rotate [account]       Rotate keys with backup for specified account');
  console.log('                         Options:');
  console.log('                         -f, --force    Force rotation regardless of key age');
  console.log('  show-public [account]  Show current public key for specified account');
  console.log('  list-accounts         List all accounts with key pairs');
  console.log('  mirror-all [direction] Export or import all account keys as encrypted package');
  console.log('                         Options:');
  console.log('                         -o, --output   Output file path for export');
  console.log('                         -i, --input    Input file path for import');
  console.log('                         -f, --force    Overwrite existing keys on import');
  console.log('  mirror-account <account> [direction] Export or import single account keys as encrypted package');
  console.log('                         Options:');
  console.log('                         -o, --output   Output file path for export');
  console.log('                         -i, --input    Input file path for import');
  console.log('                         -f, --force    Overwrite existing keys on import');
  console.log('  init-env              Create new .env configuration');
  console.log('  key-paths             Show key file locations');
  console.log('  key-age [account]     Check age of current keys and rotation schedule');
  console.log('');
  console.log('Examples:');
  console.log('  $ skm generate prod           # Generate new key pair for prod account');
  console.log('  $ skm rotate dev             # Rotate keys for dev account');
  console.log('  $ skm rotate prod --force    # Force key rotation for prod account');
  console.log('  $ skm key-age test          # Check key age for test account');
  console.log('  $ skm list-accounts         # List all accounts with keys');
  console.log('  $ skm show-public prod      # Show public key for prod account');
  console.log('  $ skm mirror-all export     # Export all accounts to encrypted package');
  console.log('  $ skm mirror-all import     # Import accounts from encrypted package');
  console.log('  $ skm mirror-all export -o backup.skm  # Export to specific file');
  console.log('  $ skm mirror-all import -i backup.skm  # Import from specific file');
  console.log('  $ skm mirror-account prod export  # Export prod account only');
  console.log('  $ skm mirror-account dev import   # Import dev account only');
  console.log('  $ skm mirror-account prod export -o prod-backup.skm  # Export prod to specific file');
  console.log('  $ skm mirror-account dev import -i dev-backup.skm    # Import dev from specific file');
  console.log('');
  console.log('For more information, visit: https://github.com/yourusername/snowflake-key-manager');
});

program.parse(process.argv);