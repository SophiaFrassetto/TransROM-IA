const fs = require('fs');
const path = require('path');

// Read recent Git changes
const getRecentChanges = () => {
    // Implement logic to detect features/changes
    return {
        features: [
            {
                name: "Automatic Translation System",
                description: "Integration with DeepL API for text translation"
            }
        ]
    };
};

// Update READMEs
const updateReadme = () => {
    const changes = getRecentChanges();

    // Update main README
    let mainReadme = fs.readFileSync('README.md', 'utf-8');

    changes.features.forEach(feat => {
        const entry = `\n- ${new Date().toISOString()} ${feat.name}: ${feat.description}`;

        if (!mainReadme.includes(feat.name)) {
            mainReadme = mainReadme.replace('## Features\n', `## Features\n${entry}`);
        }
    });

    fs.writeFileSync('README.md', mainReadme);

    console.log('READMEs updated with latest changes!');
};

updateReadme();