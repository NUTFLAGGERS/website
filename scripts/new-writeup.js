import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function ask(question, defaultValue = '') {
  return new Promise((resolve) => {
    const promptText = defaultValue ? `${question} (${defaultValue}): ` : `${question}: `;
    rl.question(promptText, (answer) => {
      resolve(answer.trim() || defaultValue);
    });
  });
}

async function main() {
  console.log('\n--- 🚩 NUTFLAGGERS Writeup Creator ---\n');

  const today = new Date().toISOString().split('T')[0];
  const title = await ask('CTF Event Title', 'SekaiCTF 2026');
  const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
  const pubDate = await ask('Publication Date (YYYY-MM-DD)', today);
  const place = await ask('Placement / Rank (optional)', 'top 10');
  const score = await ask('Total Score / Points (optional)', '3500 pts');
  const tagsInput = await ask('Categories / Tags (comma separated)', 'web, pwn, crypto');
  const tags = tagsInput.split(',').map(t => t.trim()).filter(Boolean);

  const content = `---
title: "${title}"
pubDate: "${pubDate}"
place: "${place}"
score: "${score}"
tags: [${tags.map(t => `"${t}"`).join(', ')}]
challenges:
  - name: "Example Challenge 1"
    category: "${tags[0] || 'web'}"
    points: "200 pts"
---

# ${title} Writeup

Writeup overview and highlights for ${title}.

## Challenge 1 Name (${tags[0] || 'web'})

Detailed explanation of your solve script and solution.

\`\`\`python
# Solve script
import requests

print("Flag captured!")
\`\`\`
`;

  const targetDir = path.join(process.cwd(), 'src', 'content', 'writeups');
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  const targetPath = path.join(targetDir, `${slug}.md`);
  fs.writeFileSync(targetPath, content, 'utf8');

  console.log(`\n✅ Writeup template created successfully!`);
  console.log(`📁 File location: src/content/writeups/${slug}.md\n`);
  rl.close();
}

main().catch((err) => {
  console.error(err);
  rl.close();
});
