/**
 * encrypt-pages.mjs
 *
 * Post-build script. Encrypts the <main> content of all HTML files under
 * dist/writeups/ and dist/resources/ using AES-256-GCM + PBKDF2.
 *
 * The password is read from the SITE_PASSWORD environment variable.
 * Without the correct password, the ciphertext stored in the HTML
 * cannot be read — even with DevTools or disabled JavaScript.
 *
 * Usage:
 *   SITE_PASSWORD="your-secret" node scripts/encrypt-pages.mjs
 *
 * In GitHub Actions, set SITE_PASSWORD as a repository secret and
 * pass it via env: in the workflow step.
 */

import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { pbkdf2Sync, randomBytes, createCipheriv } from 'node:crypto';

// ── Config ────────────────────────────────────────────────────────────────────

const PASSWORD = process.env.SITE_PASSWORD;
if (!PASSWORD) {
  console.error('[encrypt] ✖  SITE_PASSWORD env var is not set.');
  console.error('[encrypt]    Run: SITE_PASSWORD="your-secret" node scripts/encrypt-pages.mjs');
  process.exit(1);
}

const DIST_DIR = resolve('dist');

// Directories relative to dist/ whose HTML files should be encrypted
const PROTECTED_DIRS = ['writeups', 'resources'];

const PBKDF2_ITERATIONS = 200_000;

// ── Crypto helpers ─────────────────────────────────────────────────────────────

/**
 * Encrypt a UTF-8 string using AES-256-GCM with a PBKDF2-derived key.
 * Returns hex/base64 encoded components to embed in the page.
 */
function encryptContent(plaintext, password) {
  const salt    = randomBytes(32);   // 256-bit salt
  const iv      = randomBytes(12);   // 96-bit IV for GCM
  const key     = pbkdf2Sync(password, salt, PBKDF2_ITERATIONS, 32, 'sha256');

  const cipher  = createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([
    cipher.update(plaintext, 'utf8'),
    cipher.final(),
  ]);
  const authTag = cipher.getAuthTag(); // 128-bit authentication tag

  return {
    salt:       salt.toString('hex'),
    iv:         iv.toString('hex'),
    ciphertext: encrypted.toString('base64'),
    authTag:    authTag.toString('hex'),
  };
}

// ── Gate HTML builder ─────────────────────────────────────────────────────────

/**
 * Build the replacement <main> block containing the encrypted blob and
 * the self-contained decryption UI + Web Crypto script.
 */
function buildGate(encData) {
  const json = JSON.stringify(encData);
  const iterations = PBKDF2_ITERATIONS;

  return `
  <!-- encrypted-gate -->

  <div id="gate-container">
    <div class="gate-prompt">
      <div class="gate-label">── members only</div>
      <div class="gate-input-row">
        <span class="gate-prefix">~/0xflag $&nbsp;</span>
        <input
          id="gate-input"
          type="password"
          autocomplete="current-password"
          autocapitalize="none"
          spellcheck="false"
          placeholder="enter password"
          aria-label="Member password"
        />
      </div>
      <div id="gate-error" class="gate-error" aria-live="polite"></div>
      <div class="gate-hint">press <kbd>enter</kbd> to unlock</div>
    </div>
  </div>

  <!-- encrypted payload — unreadable without the correct password -->
  <script id="enc-data" type="application/json">${json}</script>

  <div id="decrypted-content" style="display:none"></div>

  <style>
    #gate-container {
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 40vh;
      padding: 48px 0;
    }
    .gate-prompt {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .gate-label {
      color: var(--section-header);
      font-size: 13px;
      letter-spacing: 0.05em;
      font-weight: 500;
      margin-bottom: 4px;
    }
    .gate-input-row {
      display: flex;
      align-items: center;
      border-bottom: 1px solid var(--border-focus);
      padding-bottom: 6px;
    }
    .gate-prefix {
      color: var(--link);
      white-space: nowrap;
      font-size: 14px;
      user-select: none;
    }
    #gate-input {
      background: transparent;
      border: none;
      outline: none;
      color: var(--fg);
      font-family: 'Fira Code', monospace;
      font-size: 14px;
      width: 240px;
      caret-color: var(--link);
      letter-spacing: 0.04em;
    }
    #gate-input::placeholder {
      color: var(--dim);
      opacity: 0.5;
    }
    .gate-error {
      font-size: 12px;
      color: #e38888;
      min-height: 16px;
      letter-spacing: 0.03em;
    }
    .gate-hint {
      color: var(--dim);
      font-size: 12px;
    }
    .gate-hint kbd {
      font-family: inherit;
      border: 1px solid var(--border-focus);
      border-radius: 2px;
      padding: 0 4px;
      font-size: 11px;
    }
    #gate-container.unlocking .gate-prefix {
      color: var(--link);
      opacity: 0.6;
    }
    @keyframes gate-fade-out {
      from { opacity: 1; }
      to   { opacity: 0; transform: translateY(-6px); }
    }
    #gate-container.fade-out {
      animation: gate-fade-out 0.3s ease forwards;
    }
  </style>

  <script type="module">
    const SESSION_KEY = 'nf_pw';
    const ITERATIONS  = ${iterations};

    const enc  = JSON.parse(document.getElementById('enc-data').textContent);
    const gate = document.getElementById('gate-container');
    const input = document.getElementById('gate-input');
    const error = document.getElementById('gate-error');
    const content = document.getElementById('decrypted-content');

    // ── Crypto helpers ────────────────────────────────────────────────────────

    function hexToBytes(hex) {
      const arr = new Uint8Array(hex.length / 2);
      for (let i = 0; i < hex.length; i += 2)
        arr[i / 2] = parseInt(hex.slice(i, i + 2), 16);
      return arr;
    }

    function b64ToBytes(b64) {
      const binary = atob(b64);
      const arr = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) arr[i] = binary.charCodeAt(i);
      return arr;
    }

    async function deriveKey(password, saltBytes) {
      const enc = new TextEncoder();
      const raw = await crypto.subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveKey']);
      return crypto.subtle.deriveKey(
        { name: 'PBKDF2', salt: saltBytes, iterations: ITERATIONS, hash: 'SHA-256' },
        raw,
        { name: 'AES-GCM', length: 256 },
        false,
        ['decrypt']
      );
    }

    async function tryDecrypt(password) {
      try {
        const saltBytes    = hexToBytes(enc.salt);
        const ivBytes      = hexToBytes(enc.iv);
        const authTagBytes = hexToBytes(enc.authTag);
        const ctBytes      = b64ToBytes(enc.ciphertext);

        // GCM expects ciphertext + authTag concatenated
        const combined = new Uint8Array(ctBytes.length + authTagBytes.length);
        combined.set(ctBytes);
        combined.set(authTagBytes, ctBytes.length);

        const key       = await deriveKey(password, saltBytes);
        const plainBuf  = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: ivBytes }, key, combined);
        return new TextDecoder().decode(plainBuf);
      } catch {
        return null; // Wrong password → GCM auth tag mismatch
      }
    }

    // ── Unlock ────────────────────────────────────────────────────────────────

    function showContent(html) {
      gate.classList.add('fade-out');
      gate.addEventListener('animationend', () => {
        gate.style.display = 'none';
        content.innerHTML = html;
        content.style.display = '';
        // Re-run any inline scripts inside decrypted content
        content.querySelectorAll('script').forEach(old => {
          const s = document.createElement('script');
          if (old.type) s.type = old.type;
          s.textContent = old.textContent;
          old.replaceWith(s);
        });
      }, { once: true });
    }

    async function attempt(password) {
      gate.classList.add('unlocking');
      error.textContent = '';
      input.disabled = true;

      const result = await tryDecrypt(password);

      if (result !== null) {
        sessionStorage.setItem(SESSION_KEY, password);
        showContent(result);
      } else {
        gate.classList.remove('unlocking');
        input.disabled = false;
        input.value = '';
        error.textContent = '[access denied] — incorrect password';
        input.focus();
      }
    }

    // ── Auto-unlock if session has cached password ─────────────────────────

    const cached = sessionStorage.getItem(SESSION_KEY);
    if (cached) {
      attempt(cached);
    } else {
      input.focus();
    }

    // ── Event listeners ───────────────────────────────────────────────────────

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') attempt(input.value);
    });
  </script>
`;
}


// ── File processing ───────────────────────────────────────────────────────────

/**
 * Recursively collect all .html files under a directory.
 */
function collectHtmlFiles(dir) {
  const results = [];
  try {
    for (const entry of readdirSync(dir)) {
      const full = join(dir, entry);
      if (statSync(full).isDirectory()) {
        results.push(...collectHtmlFiles(full));
      } else if (entry.endsWith('.html')) {
        results.push(full);
      }
    }
  } catch {
    // Directory doesn't exist — skip silently
  }
  return results;
}

/**
 * Encrypt the <main>…</main> block in a single HTML file in-place.
 */
function processFile(filePath) {
  const html = readFileSync(filePath, 'utf8');

  // Match the outermost <main>...</main> block, capturing:
  //   group 1: opening tag  e.g. "<main>" or "<main class="...">"
  //   group 2: inner content (greedy — gets everything to the LAST </main>)
  //   group 3: closing tag  "</main>"
  const mainRe = /(<main(?:\s[^>]*)?>)([\s\S]*)(<\/main>)/i;
  const match  = html.match(mainRe);

  if (!match) {
    console.warn(`[encrypt] ⚠  No <main> found in ${filePath} — skipping`);
    return;
  }

  const openTag   = match[1]; // "<main>"
  const closeTag  = match[3]; // "</main>"
  const fullMain  = match[0]; // entire <main>...</main> — this is what we encrypt

  const encData   = encryptContent(fullMain, PASSWORD);
  const gateInner = buildGate(encData);

  // Use function form of replace() to prevent JS from interpreting special
  // replacement sequences like $& (full match) or $` (pre-match string).
  // The gate template contains "$&nbsp;" in the prefix span which would
  // otherwise be treated as $& = "insert full matched substring", injecting
  // the entire writeup content into the gate HTML.
  const result = html.replace(mainRe, () => `${openTag}${gateInner}${closeTag}`);

  writeFileSync(filePath, result, 'utf8');
  console.log(`[encrypt] ✔  ${filePath}`);
}

// ── Main ──────────────────────────────────────────────────────────────────────

let total = 0;
for (const dir of PROTECTED_DIRS) {
  const files = collectHtmlFiles(join(DIST_DIR, dir));
  for (const file of files) {
    processFile(file);
    total++;
  }
}

console.log(`[encrypt] Done — ${total} file(s) encrypted.`);
