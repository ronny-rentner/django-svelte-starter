import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Function to download an icon as SVG
async function downloadIcon(fullIconName, outputDir) {
    const url = `https://api.iconify.design/${fullIconName}.svg`;

    try {
        // Fetch the SVG data
        const response = await fetch(url);

        // Check if the request was successful
        if (!response.ok) {
            throw new Error(`Failed to fetch ${fullIconName}: ${response.statusText}`);
        }

        const svgData = await response.text();

        // Ensure the output directory exists
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        // Replace colon with hyphen for the filename
        const fileName = fullIconName + '.svg';
        const filePath = path.join(outputDir, fileName);

        // Write the SVG file
        fs.writeFileSync(filePath, svgData);
        console.log(`Downloaded ${fullIconName} to ${filePath}`);
    } catch (error) {
        console.error(`Failed to download ${fullIconName}: ${error.message}`);
    }
}

// Utility to handle file paths correctly in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Get the full icon name from the command-line argument
const [fullIconName] = process.argv.slice(2);

// Ensure the icon name is provided
if (!fullIconName) {
    console.error('Usage: node download-icon.js <iconSet:iconName>');
    process.exit(1);
}

// Specify the output directory
const outputDir = path.join(__dirname, 'downloaded-icons');

// Download the specified icon
downloadIcon(fullIconName, outputDir);
