// scan-project.js
const fs = require('fs').promises;
const path = require('path');

// Files and directories to ignore
const IGNORE_LIST = [
    'node_modules',
    '.git',
    '.next',
    '__pycache__',
    'chrome_user_data',
    'package-lock.json',
    'yarn.lock',
    '.env',
    'project-files.txt'
];

async function generateStructure(dir, prefix = '') {
    let structure = '';
    const items = await fs.readdir(dir);

    for (const item of items) {
        if (IGNORE_LIST.some(ignored => item.includes(ignored))) {
            continue;
        }

        const fullPath = path.join(dir, item);
        const stat = await fs.stat(fullPath);

        if (stat.isDirectory()) {
            structure += `${prefix}📁 ${item}/\n`;
            structure += await generateStructure(fullPath, prefix + '  ');
        } else {
            structure += `${prefix}📄 ${item}\n`;
        }
    }

    return structure;
}

async function scanDirectory(dir) {
    let results = {};

    try {
        const items = await fs.readdir(dir);

        for (const item of items) {
            if (IGNORE_LIST.some(ignored => item.includes(ignored))) {
                continue;
            }

            const fullPath = path.join(dir, item);
            const stat = await fs.stat(fullPath);

            if (stat.isDirectory()) {
                const subResults = await scanDirectory(fullPath);
                results = { ...results, ...subResults };
            } else {
                try {
                    const content = await fs.readFile(fullPath, 'utf8');
                    results[fullPath] = content;
                } catch (error) {
                    console.error(`Error reading file ${fullPath}:`, error);
                }
            }
        }
    } catch (error) {
        console.error(`Error scanning directory ${dir}:`, error);
    }

    return results;
}

async function generateProjectSummary() {
    try {
        // Generate structure
        console.log('Generating project structure...');
        const frontendStructure = await generateStructure('./frontend');
        const backendStructure = await generateStructure('./backend');

        // Scan files
        console.log('Scanning files...');
        const frontendFiles = await scanDirectory('./frontend');
        const backendFiles = await scanDirectory('./backend');

        // Generate summaries
        let summary = '# Project Structure\n\n';
        summary += '## Frontend Structure:\n```\n';
        summary += frontendStructure;
        summary += '```\n\n';
        summary += '## Backend Structure:\n```\n';
        summary += backendStructure;
        summary += '```\n\n';
        
        summary += '# File Contents\n\n';
        
        // Add frontend files
        summary += '## Frontend Files\n\n';
        for (const [file, content] of Object.entries(frontendFiles)) {
            summary += `----------------------------------------------------------------------------------\n`;
            summary += `// ${file}\n${content}\n\n`;
        }

        // Add backend files
        summary += '## Backend Files\n\n';
        for (const [file, content] of Object.entries(backendFiles)) {
            summary += `----------------------------------------------------------------------------------\n`;
            summary += `// ${file}\n${content}\n\n`;
        }

        // Write to root directory
        await fs.writeFile('project-files.txt', summary);

        console.log('\nProject summary generated successfully!');
        console.log('Summary file: ./project-files.txt');

    } catch (error) {
        console.error('Error generating project summary:', error);
    }
}

generateProjectSummary();