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
  console.log('\n--- 🚩 NUTFLAGGERS Post / Writeup Creator ---\n');

  const today = new Date().toISOString().split('T')[0];
  const title = await ask('Post / Writeup Title', 'Example Challenge Walkthrough');
  const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
  const pubDate = await ask('Publication Date (YYYY-MM-DD)', today);
  const event = await ask('CTF Event Name (optional)', 'SekaiCTF 2026');
  const author = await ask('Author Handle (optional)', 'w4ve');
  const score = await ask('Challenge Points / Total Score (optional)', '500 pts');
  const tagsInput = await ask('Categories / Tags (comma separated)', 'web, pwn');
  const tags = tagsInput.split(',').map(t => t.trim()).filter(Boolean);
  const description = await ask('Summary / Short Description', 'Comprehensive walkthrough and technical analysis.');

  const frontmatterLines = [
    '---',
    `title: "${title}"`,
    `pubDate: "${pubDate}"`,
  ];

  if (event) frontmatterLines.push(`event: "${event}"`);
  if (author) frontmatterLines.push(`author: "${author}"`);
  if (score) frontmatterLines.push(`score: "${score}"`);
  if (description) frontmatterLines.push(`description: "${description}"`);
  frontmatterLines.push(`tags: [${tags.map(t => `"${t}"`).join(', ')}]`);
  frontmatterLines.push('---');

  const content = `${frontmatterLines.join('\n')}

# ${title}

${description}

## Executive Summary

Brief overview of the target, difficulty, and high-level exploit chain.

## Vulnerability Analysis

Detailed technical walk-through of the target application or binary.

### Root Cause
Explanation of the underlying bug (e.g. memory corruption, injection, logic flaw).

## Exploitation & Solution

Step-by-step walkthrough detailing how the primitive was constructed and executed.

\`\`\`python
# Solve script payload
import requests

def main():
    print("[+] Executing solve script...")
    # Add exploit logic here

if __name__ == "__main__":
    main()
\`\`\`

## Flag & Conclusion

**Flag**: \`nutflaggers{example_flag_here}\`

Key takeaways or mitigations learned from this challenge.
`;

  const targetDir = path.join(process.cwd(), 'src', 'content', 'writeups');
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  const targetPath = path.join(targetDir, `${slug}.md`);
  fs.writeFileSync(targetPath, content, 'utf8');

  console.log(`\n✅ Post / Writeup template created successfully!`);
  console.log(`📁 File location: src/content/writeups/${slug}.md\n`);
  rl.close();
}

main().catch((err) => {
  console.error(err);
  rl.close();
});
