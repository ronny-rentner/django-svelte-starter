import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Recreate __dirname and __filename in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths to your files
const buildInfoPath = path.resolve(__dirname, '../src/build-info.json');
const packageJsonPath = path.resolve(__dirname, '../package.json');

// Update build-info.json and package.json version
async function updateBuildInfo() {
  let buildInfo;

  // Check if the build-info.json file exists
  if (fs.existsSync(buildInfoPath)) {
    // If it exists, read and parse the existing data
    const data = await fs.promises.readFile(buildInfoPath, 'utf-8');
    buildInfo = JSON.parse(data);
  } else {
    // If it doesn't exist, create an initial structure
    buildInfo = {
      buildNumber: 0,
      lastBuildTimestamp: '',
    };
  }

  // Increment the build number
  buildInfo.buildNumber += 1;

  // Update the build timestamp
  buildInfo.lastBuildTimestamp = new Date().toISOString().substr(0, 19);

  // Write the updated information back to the file
  await fs.promises.writeFile(buildInfoPath, JSON.stringify(buildInfo, null, 2));

  // Update package.json version
  await updatePackageVersion(buildInfo.buildNumber);
}

async function updatePackageVersion(buildNumber) {
  const packageJsonData = await fs.promises.readFile(packageJsonPath, 'utf-8');
  const packageJson = JSON.parse(packageJsonData);

  // Update the version field
  const baseVersion = '1'; // You can change the base version as needed
  packageJson.version = `${baseVersion}.${buildNumber}`;

  // Write back to package.json
  await fs.promises.writeFile(packageJsonPath, JSON.stringify(packageJson, null, 2));

  console.log(`Updated package.json version to ${packageJson.version} for next build.\n`);
}

// Execute the function
updateBuildInfo().catch((error) => {
  console.error('Error updating build info:', error);
  process.exit(1);
});
