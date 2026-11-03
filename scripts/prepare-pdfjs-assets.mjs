import { cp, mkdir } from 'node:fs/promises';
const root = new URL('../', import.meta.url);
const pdfjs = new URL('../node_modules/pdfjs-dist/', import.meta.url);
for (const directory of ['cmaps', 'standard_fonts', 'wasm', 'iccs']) {
  const target = new URL(`public/pdfjs/${directory}/`, root);
  await mkdir(target, { recursive: true });
  await cp(new URL(directory, pdfjs), target, { recursive: true });
}
await cp(new URL('LICENSE', pdfjs), new URL('public/pdfjs/LICENSE', root));
